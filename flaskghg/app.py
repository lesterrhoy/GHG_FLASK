from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from mysql.connector import Error
from statsmodels.tsa.arima.model import ARIMA  # Import ARIMA for forecasting
import numpy as np
import pandas as pd
from io import BytesIO
from openpyxl import Workbook
from fpdf import FPDF
import traceback
from flask import send_file
from flask import request
from datetime import datetime
from flask_bcrypt import Bcrypt
import math
from flask import jsonify
from flask import flash
from decimal import Decimal
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle  # Add this line to import necessary classes
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, r2_score

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a strong secret key in production!

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Empty password as specified
app.config['MYSQL_DB'] = 'ghg_database'

# Helper function to establish MySQL connection
def get_db_connection():
    connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return connection

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Replace with your actual MySQL password if it's not empty
    'database': 'ghg_database'
}


def calculate_accommodation_emission(factor, occupied_rooms, nights_per_room):
    return factor * occupied_rooms * nights_per_room

# Route for root URL, show the homepage first
@app.route('/')
def index():
    return render_template('homepage.html')  # Serve the homepage

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''  # Initialize error message
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Query to check if the username exists
            query = "SELECT * FROM tblsignin WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user and password == user['password']:
                session['loggedIn'] = True
                session['username'] = user['username']
                session['office'] = user['office']
                session['campus'] = user['campus']

                # Redirect based on the office and user role
                office_redirects = {
                    'Central Sustainable Office': 'csd_dashboard',
                    'Sustainable Development Office': 'sdo_dashboard',
                    'Environmental Management Unit': 'emu_dashboard',
                    'External Affair': 'external_dashboard',
                    'Procurement Office': 'procurement_dashboard'
                }
                return redirect(url_for(office_redirects.get(user['office'], 'user_dashboard')))
            else:
                message = "Invalid username or password."

        except mysql.connector.Error as e:
            message = f"Database Error: {e}"

        finally:
            cursor.close()
            conn.close()

    return render_template('login.html', message=message)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    alert_message = ''  # Initialize alert message

    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new-password']
        confirm_password = request.form['confirm-password']

        if new_password != confirm_password:
            alert_message = "Passwords do not match!"
        else:
            try:
                # Connect to the database
                conn = get_db_connection()
                cursor = conn.cursor()

                # Check if the username exists in the database
                query = "SELECT * FROM tblsignin WHERE username = %s"
                cursor.execute(query, (username,))
                user = cursor.fetchone()

                if not user:
                    alert_message = "Username does not exist."
                else:
                    # Update the password in the database (in plaintext)
                    update_query = "UPDATE tblsignin SET password = %s WHERE username = %s"
                    cursor.execute(update_query, (new_password, username))
                    conn.commit()

                    if cursor.rowcount > 0:
                        flash("Password updated successfully!", "success")
                        return redirect(url_for('login'))
                    else:
                        alert_message = "Password update failed. No changes were made."

            except mysql.connector.Error as e:
                alert_message = f"Database Error: {e}"
            except Exception as e:
                alert_message = f"An error occurred: {e}"

            finally:
                cursor.close()
                conn.close()

    return render_template('change_password.html', alert_message=alert_message)


@app.route('/report', methods=['GET'])
def report():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    if 'campus' not in session:
        flash("Campus information is missing from your session. Please select a campus.", "warning")
        return redirect(url_for('select_campus'))  # Redirect to a page where user can select a campus

    # Retrieve selected filters from query parameters
    selected_month = request.args.get('month', '')
    selected_year = request.args.get('year', '')

    results = {
        'electricity': [],
        'water': [],
        'unsegWaste': [],
        'segWaste': [],
        'treatedWater': [],
        'fuelEmissions': []
    }
    pagination_info = {
        'electricity': {'current_page': 1, 'total_pages': 1},
        'water': {'current_page': 1, 'total_pages': 1},
        'unsegWaste': {'current_page': 1, 'total_pages': 1},
        'segWaste': {'current_page': 1, 'total_pages': 1},
        'treatedWater': {'current_page': 1, 'total_pages': 1},
        'fuelEmissions': {'current_page': 1, 'total_pages': 1}
    }
    
    items_per_page = 15  # Number of items per page
    all_data = request.args.get('all_data', 'false').lower() == 'true'

    try:
        conn = get_db_connection()

        def fetch_data_with_filters(table, campus, month_column, year_column, current_page, items_per_page, date_format=None):
            query = f"SELECT * FROM {table} WHERE campus = %s"
            params = [campus]

            # Apply month and year filters if provided
            if selected_month:
                if date_format:
                    query += f" AND MONTH({month_column}) = %s"
                else:
                    query += f" AND {month_column} = %s"
                params.append(selected_month)

            if selected_year:
                if date_format:
                    query += f" AND YEAR({year_column}) = %s"
                else:
                    query += f" AND {year_column} = %s"
                params.append(selected_year)

            # Count total items for pagination
            count_query = f"SELECT COUNT(*) AS count FROM ({query}) AS filtered_query"
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(count_query, tuple(params))
                total_items = cursor.fetchone()['count']
                total_pages = math.ceil(total_items / items_per_page)
                offset = (current_page - 1) * items_per_page
                pagination = {'current_page': current_page, 'total_pages': total_pages}

            # Adjust query for pagination
            if all_data:
                paginated_query = query
            else:
                paginated_query = f"{query} LIMIT %s OFFSET %s"
                params.extend([items_per_page, offset])

            # Fetch paginated results
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(paginated_query, tuple(params))
                data = cursor.fetchall()

            return data, pagination

        # Fetch and paginate data for each table
        current_page = int(request.args.get('electricity_page', 1))
        results['electricity'], pagination_info['electricity'] = fetch_data_with_filters(
            'electricity_consumption', session['campus'], 'month', 'year', current_page, items_per_page
        )

        current_page = int(request.args.get('water_page', 1))
        results['water'], pagination_info['water'] = fetch_data_with_filters(
            'tblwater', session['campus'], 'Date', 'Date', current_page, items_per_page, date_format=True
        )

        current_page = int(request.args.get('unsegWaste_page', 1))
        results['unsegWaste'], pagination_info['unsegWaste'] = fetch_data_with_filters(
            'tblsolidwasteunsegregated', session['campus'], 'Month', 'Year', current_page, items_per_page
        )

        current_page = int(request.args.get('segWaste_page', 1))
        results['segWaste'], pagination_info['segWaste'] = fetch_data_with_filters(
            'tblsolidwastesegregated', session['campus'], 'Month', 'Year', current_page, items_per_page
        )

        current_page = int(request.args.get('treatedWater_page', 1))
        results['treatedWater'], pagination_info['treatedWater'] = fetch_data_with_filters(
            'tbltreatedwater', session['campus'], 'Month', 'Month', current_page, items_per_page
        )

        current_page = int(request.args.get('fuelEmissions_page', 1))
        results['fuelEmissions'], pagination_info['fuelEmissions'] = fetch_data_with_filters(
            'fuel_emissions', session['campus'], 'date', 'date', current_page, items_per_page, date_format=True
        )

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
    finally:
        conn.close()

    # Pass the results dictionary and pagination info to the template
    return render_template('report.html', results=results, pagination_info=pagination_info)



@app.route('/fetch_all_data', methods=['GET'])
def fetch_all_data():
    table = request.args.get('table')
    
    queries = {
        'electricityTable': "SELECT * FROM electricity_consumption",
        'waterTable': "SELECT * FROM tblwater",
        'fuelEmissionsTable': "SELECT * FROM fuel_emissions",
        'treatedWaterTable': "SELECT * FROM tbltreatedwater",
        'segWasteTable': "SELECT * FROM tblsolidwastesegregated",
        'unsegWasteTable': "SELECT * FROM tblsolidwasteunsegregated"
    }
    
    if table not in queries:
        return jsonify({'error': 'Invalid table selected'}), 400
    
    try:
        conn = get_db_connection()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(queries[table])
            data = cursor.fetchall()
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500
    finally:
        conn.close()
    
    return jsonify(data)

from datetime import datetime
from flask import session, redirect, url_for, request, render_template, flash
import mysql.connector
from prophet import Prophet
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd

@app.route('/emu', methods=['GET', 'POST'])
def emu_dashboard():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    campus = session.get('campus', 'default_campus')
    selected_year = int(request.args.get('year', datetime.now().year))
    selected_month = request.args.get('month', None)
    current_year = datetime.now().year

    # Initialize data lists for emissions
    electricity_data = [0] * 12
    fuel_data = [0] * 12
    waste_segregated_data = [0] * 12
    waste_unsegregated_data = [0] * 12
    water_data = [0] * 12
    treated_water_data = [0] * 12

    current_emission_data = {
        "electricity": 0,
        "fuel": 0,
        "waste_segregated": 0,
        "waste_unsegregated": 0,
        "water": 0,
        "treated_water": 0,
    }

    month_to_index = {
        "January": 0, "February": 1, "March": 2, "April": 3, "May": 4, "June": 5,
        "July": 6, "August": 7, "September": 8, "October": 9, "November": 10, "December": 11
    }

    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Could not establish database connection.")

        cursor = conn.cursor(dictionary=True)

        # Queries for other data
        queries = [
            ("SELECT month, kg_co2_per_kwh FROM electricity_consumption WHERE campus = %s AND year = %s ORDER BY month ASC", electricity_data, "electricity"),
            ("SELECT MONTHNAME(date) AS month, total_emission FROM fuel_emissions WHERE campus = %s AND YEAR(date) = %s ORDER BY MONTH(date) ASC", fuel_data, "fuel"),
            ("SELECT Month, SUM(GHGEmissionKGCO2e) AS total_emission FROM tblsolidwastesegregated WHERE Campus = %s AND Year = %s GROUP BY Month ORDER BY FIELD(Month, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')", waste_segregated_data, "waste_segregated"),
            ("SELECT Month, GHGEmissionKGCO2e FROM tblsolidwasteunsegregated WHERE Campus = %s AND Year = %s ORDER BY FIELD(Month, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')", waste_unsegregated_data, "waste_unsegregated"),
            ("SELECT MONTHNAME(Date) AS month, SUM(FactorKGCO2e) AS total_emission FROM tblwater WHERE Campus = %s AND YEAR(Date) = %s GROUP BY MONTHNAME(Date) ORDER BY FIELD(MONTHNAME(Date), 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')", water_data, "water"),
        ]

        for query, data_list, category in queries:
            cursor.execute(query, (campus, selected_year))
            for row in cursor.fetchall():
                month_index = month_to_index.get(row.get('month') or row.get('Month'), -1)
                if month_index != -1:
                    emission_value = row.get('total_emission') or row.get('kg_co2_per_kwh') or row.get('GHGEmissionKGCO2e')
                    if emission_value is not None:
                        data_list[month_index] = float(emission_value)
                        current_emission_data[category] += float(emission_value)

        # Treated Water Data
        treated_water_query = """
            SELECT Month, SUM(FactorKGCO2e) AS total_emission
            FROM tbltreatedwater
            WHERE Campus = %s AND YEAR(CURDATE()) = %s
        """
        params = [campus, selected_year]
        if selected_month:
            treated_water_query += " AND Month = %s"
            params.append(selected_month)

        treated_water_query += """
            GROUP BY Month
            ORDER BY FIELD(Month, 'January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December')
        """

        cursor.execute(treated_water_query, params)
        for row in cursor.fetchall():
            month_index = month_to_index.get(row.get('Month'), -1)
            if month_index != -1:
                treated_value = row.get('total_emission')
                if treated_value is not None:
                    treated_water_data[month_index] = float(treated_value)
                    current_emission_data["treated_water"] += float(treated_value)

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Forecast function using Prophet
    def forecast_prophet(data, periods):
        if all(v == 0 for v in data):
            return [0] * periods, 0

        try:
            df = pd.DataFrame({'ds': pd.date_range(start='2023-01-01', periods=len(data), freq='M'), 'y': data})
            df = df[df['y'] > 0]
            model = Prophet(yearly_seasonality=True)
            model.fit(df)
            future = model.make_future_dataframe(periods=periods, freq='M')
            forecast = model.predict(future)
            return forecast['yhat'][-periods:].tolist(), r2_score(df['y'], model.predict(df)['yhat'])
        except Exception as e:
            flash(f"Forecast Error: {e}", "danger")
            return [0] * periods, 0

    # Forecast data with R² scores using Prophet
    forecast_data = {
        "electricity_forecast": {
            "prophet": {
                "forecast": forecast_prophet(electricity_data, periods=12)[0],
                "r2_score": forecast_prophet(electricity_data, periods=12)[1],
            }
        },
        "fuel_forecast": {
            "prophet": {
                "forecast": forecast_prophet(fuel_data, periods=12)[0],
                "r2_score": forecast_prophet(fuel_data, periods=12)[1],
            }
        },
        "waste_segregated_forecast": {
            "prophet": {
                "forecast": forecast_prophet(waste_segregated_data, periods=12)[0],
                "r2_score": forecast_prophet(waste_segregated_data, periods=12)[1],
            }
        },
        "waste_unsegregated_forecast": {
            "prophet": {
                "forecast": forecast_prophet(waste_unsegregated_data, periods=12)[0],
                "r2_score": forecast_prophet(waste_unsegregated_data, periods=12)[1],
            }
        },
        "water_forecast": {
            "prophet": {
                "forecast": forecast_prophet(water_data, periods=12)[0],
                "r2_score": forecast_prophet(water_data, periods=12)[1],
            }
        },
        "treated_water_forecast": {
            "prophet": {
                "forecast": forecast_prophet(treated_water_data, periods=12)[0],
                "r2_score": forecast_prophet(treated_water_data, periods=12)[1],
            }
        },
    }

    # Print R² scores for validation
    for key, value in forecast_data.items():
        print(f"{key.replace('_forecast', '').title()} Prophet R² Score:", value["prophet"]["r2_score"])

    # Month labels
    def get_month_labels(start_month, start_year, total_months):
        return [f"{(start_month + i) % 12 + 1:02d}/{(start_year + (start_month + i) // 12) % 100:02d}" for i in range(total_months)]

    month_labels = [f"{i:02d}" for i in range(1, 13)]
    labels = get_month_labels(0, selected_year, 12)

    # Render the template with forecast data
    return render_template(
        'emu_index.html',
        electricity_data=electricity_data,
        fuel_data=fuel_data,
        waste_segregated_data=waste_segregated_data,
        waste_unsegregated_data=waste_unsegregated_data,
        water_data=water_data,
        treated_water_data=treated_water_data,
        forecast_data=forecast_data,
        current_emission_data=current_emission_data,
        selected_year=selected_year,
        current_year=current_year,
        labels=labels,
        month_labels=month_labels
    )




# Route for Electricity Consumption
@app.route('/electricity_consumption', methods=['GET', 'POST'])
def electricity_consumption():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Get the logged-in campus from the session
    campus = session.get('campus')

    # Determine the associated campuses based on the logged-in campus
    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        # For any other campus, include only that campus
        associated_campuses = [campus]

    # Set up pagination parameters
    page = request.args.get('page', 1, type=int)  # Get the current page number from the query string
    per_page = 20  # Number of records per page
    offset = (page - 1) * per_page  # Calculate the offset based on the current page

    # Get filter parameters from query string
    selected_month = request.args.get('month', None)
    selected_quarter = request.args.get('quarter', None)
    selected_year = request.args.get('year', None)

    results = {}  # Dictionary to hold calculation results
    if request.method == 'POST':
        # Handle form submission
        campus = request.form.get('campus')
        category = request.form.get('category')
        month = request.form.get('month')
        quarter = request.form.get('quarter')
        year = request.form.get('year')
        prev_reading = float(request.form.get('prevReading'))
        current_reading = float(request.form.get('currentReading'))
        multiplier = float(request.form.get('multiplier'))
        total_amount = float(request.form.get('totalAmount'))

        # Validate input and calculate consumption
        consumption = (current_reading - prev_reading) * multiplier

        if consumption < 0:
            flash("Consumption cannot be negative. Check your readings.", "danger")
            return redirect(url_for('electricity_consumption'))

        price_per_kwh = round(total_amount / consumption, 2) if consumption != 0 else 0
        kg_co2_per_kwh = round(0.7122 * consumption, 2)
        t_co2_per_kwh = round(kg_co2_per_kwh / 1000, 2)

        results = {
            'consumption': consumption,
            'price_per_kwh': price_per_kwh,
            'kg_co2_per_kwh': kg_co2_per_kwh,
            't_co2_per_kwh': t_co2_per_kwh
        }

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert record into electricity_consumption table
            sql = """INSERT INTO electricity_consumption 
                      (campus, category, month, quarter, year, prev_reading, current_reading, multiplier, total_amount, consumption, price_per_kwh, kg_co2_per_kwh, t_co2_per_kwh)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (campus, category, month, quarter, year, prev_reading, current_reading, multiplier, total_amount, consumption, price_per_kwh, kg_co2_per_kwh, t_co2_per_kwh))
            conn.commit()

            flash("Electricity consumption record inserted successfully.", "success")

        except mysql.connector.Error as e:
            flash(f"Database Error: {e}", "danger")

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('electricity_consumption'))

    # Fetch existing data with pagination
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Create the SQL query with dynamic placeholders for associated campuses
        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM electricity_consumption WHERE campus IN ({placeholders})"
        count_sql = f"SELECT COUNT(*) AS total FROM electricity_consumption WHERE campus IN ({placeholders})"
        params = associated_campuses

        if selected_month:
            sql += " AND month = %s"
            count_sql += " AND month = %s"
            params.append(selected_month)

        if selected_quarter:
            sql += " AND quarter = %s"
            count_sql += " AND quarter = %s"
            params.append(selected_quarter)

        if selected_year:
            sql += " AND year = %s"
            count_sql += " AND year = %s"
            params.append(selected_year)

        # Get total records with filters
        cursor.execute(count_sql, params)
        total_records = cursor.fetchone()['total']
        total_pages = (total_records + per_page - 1) // per_page  # Calculate the total number of pages

        # Apply pagination
        sql += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

        # Fetch the filtered records
        cursor.execute(sql, params)
        reports = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        reports = []
        total_pages = 0  # Set total_pages to 0 if there's a database error

    finally:
        cursor.close()
        conn.close()

    # Render the template with the fetched records and pagination information
    return render_template(
        'electricity_consumption.html', 
        reports=reports, 
        current_page=page, 
        total_pages=total_pages, 
        selected_month=selected_month, 
        selected_quarter=selected_quarter, 
        selected_year=selected_year,
        results=results  # Pass the results for calculations
    )

@app.route('/electricity_consumption/all', methods=['GET'])
def electricity_consumption_all():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Get the logged-in campus from the session
    campus = session.get('campus')

    # Determine the associated campuses based on the logged-in campus
    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        # For any other campus, include only that campus
        associated_campuses = [campus]

    selected_month = request.args.get('month', None)
    selected_quarter = request.args.get('quarter', None)
    selected_year = request.args.get('year', None)

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Create the SQL query with placeholders for associated campuses
        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM electricity_consumption WHERE campus IN ({placeholders})"
        params = associated_campuses

        if selected_month:
            sql += " AND month = %s"
            params.append(selected_month)
        if selected_quarter:
            sql += " AND quarter = %s"
            params.append(selected_quarter)
        if selected_year:
            sql += " AND year = %s"
            params.append(selected_year)

        cursor.execute(sql, params)
        all_reports = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        all_reports = []

    finally:
        cursor.close()
        conn.close()

    return jsonify(all_reports)



@app.route('/delete_record/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete the record from the database
        sql = "DELETE FROM electricity_consumption WHERE id = %s"
        cursor.execute(sql, (record_id,))
        conn.commit()

        flash("Record deleted successfully.", "success")
    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('electricity_consumption'))




# Route for Water Consumption
@app.route('/water_consumption', methods=['GET', 'POST'])
def water_consumption():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Get the logged-in campus from the session
    campus = session.get('campus')

    # Determine which campuses to include in the query
    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        # For any other campus, include only that campus
        associated_campuses = [campus]

    # Set up pagination parameters
    current_page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (current_page - 1) * per_page

    selected_year = request.args.get('year')
    selected_category = request.args.get('category')

    if request.method == 'POST':
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Extract form data from POST request
            date = request.form.get('date')
            category = request.form.get('category')
            prev_reading = float(request.form.get('prevReading'))
            current_reading = float(request.form.get('currentReading'))
            consumption = float(request.form.get('consumption'))
            total_amount = float(request.form.get('totalAmount'))

            # Calculate price per liter and CO2 factors
            price_per_liter = total_amount / consumption if consumption > 0 else 0
            kg_co2_per_m3 = consumption * 0.0149
            t_co2_per_m3 = kg_co2_per_m3 / 1000

            # Insert data into the database
            sql = """INSERT INTO tblwater (Campus, Date, Category, PreviousReading, CurrentReading, Consumption, TotalAmount, PricePerLiter, FactorKGCO2e, FactorTCO2e) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (campus, date, category, prev_reading, current_reading, consumption, total_amount, price_per_liter, kg_co2_per_m3, t_co2_per_m3))
            conn.commit()

            flash('Water consumption record inserted successfully!', 'success')

        except mysql.connector.Error as e:
            flash(f"Database Error: {e}", 'danger')

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('water_consumption'))

    # Fetch existing records with optional year and category filtering and pagination
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # SQL query with dynamic conditions based on associated campuses and selected filters
        placeholders = ', '.join(['%s'] * len(associated_campuses))
        base_query = f"SELECT * FROM tblwater WHERE Campus IN ({placeholders})"
        query_params = associated_campuses

        if selected_year:
            base_query += " AND YEAR(Date) = %s"
            query_params.append(selected_year)

        if selected_category:
            base_query += " AND Category = %s"
            query_params.append(selected_category)

        # Count the total records with current filters applied
        count_query = f"SELECT COUNT(*) FROM ({base_query}) as total_count"
        cursor.execute(count_query, query_params)
        total_records = cursor.fetchone()['COUNT(*)']
        total_pages = (total_records + per_page - 1) // per_page

        # Apply pagination
        base_query += " LIMIT %s OFFSET %s"
        query_params.extend([per_page, offset])

        # Fetch the filtered records with pagination
        cursor.execute(base_query, query_params)
        reports = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", 'danger')
        reports = []
        total_pages = 0  # Set total_pages to 0 if there's a database error

    finally:
        cursor.close()
        conn.close()

    return render_template(
        'water_consumption.html',
        reports=reports,
        selected_year=selected_year,
        selected_category=selected_category,
        current_page=current_page,
        total_pages=total_pages
    )


@app.route('/water_consumption/all', methods=['GET'])
def get_water_consumption_data_for_printing():
    if 'loggedIn' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    campus = session.get('campus')
    selected_year = request.args.get('year')
    selected_category = request.args.get('category')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Base SQL query with filtering
        sql = "SELECT * FROM tblwater WHERE Campus = %s"
        params = [campus]

        if selected_year:
            sql += " AND YEAR(Date) = %s"
            params.append(selected_year)
        if selected_category:
            sql += " AND Category = %s"
            params.append(selected_category)

        cursor.execute(sql, params)
        records = cursor.fetchall()

        return jsonify(records)

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



@app.route('/delete_water_record/<int:id>', methods=['DELETE'])
def delete_water_record(id):
    if 'loggedIn' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete the record based on the ID
        cursor.execute("DELETE FROM tblwater WHERE id = %s", (id,))
        conn.commit()

        # Check if any rows were affected (i.e., if the record was deleted)
        if cursor.rowcount == 0:
            return jsonify({'success': False, 'message': 'Record not found'}), 404

    except mysql.connector.Error as e:
        return jsonify({'success': False, 'message': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

    # If successful, return a success message
    return jsonify({'success': True}), 200



@app.route('/treated_water', methods=['GET', 'POST'])
def treated_water():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Get the logged-in campus from the session
    session_campus = session.get('campus')

    # Determine associated campuses for specific campuses
    if session_campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif session_campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [session_campus]

    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page

    selected_month = request.args.get('month', '')

    if request.method == 'POST':
        # Retrieve campus from the form instead of session
        campus = request.form.get('campus')  # Use campus from form input
        month = request.form.get('month')
        treated_volume = request.form.get('treatedVolume')
        reused_volume = request.form.get('reusedVolume')

        try:
            treated_volume = float(treated_volume)
            reused_volume = float(reused_volume)
        except ValueError:
            flash("Please enter valid numeric values for volumes.", "danger")
            return redirect(url_for('treated_water'))

        # Calculations
        effluent_volume = treated_volume - reused_volume
        co2_factor = 0.272  # Example emission factor
        kg_co2_e = effluent_volume * co2_factor
        t_co2_e = kg_co2_e / 1000
        price_per_liter = kg_co2_e

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """INSERT INTO tbltreatedwater 
                     (Campus, Month, TreatedWaterVolume, ReusedTreatedWaterVolume, EffluentVolume, PricePerLiter, FactorKGCO2e, FactorTCO2e) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (campus, month, treated_volume, reused_volume, effluent_volume, price_per_liter, kg_co2_e, t_co2_e))
            conn.commit()
            flash("Treated water record added successfully.", "success")

        except mysql.connector.Error as e:
            flash(f"Database Error: {e}", "danger")

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('treated_water'))

    # Fetch existing records with filtering and pagination
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        placeholders = ', '.join(['%s'] * len(associated_campuses))
        base_query = f"SELECT * FROM tbltreatedwater WHERE Campus IN ({placeholders})"
        count_query = f"SELECT COUNT(*) FROM tbltreatedwater WHERE Campus IN ({placeholders})"
        params = associated_campuses

        if selected_month:
            base_query += " AND Month = %s"
            count_query += " AND Month = %s"
            params.append(selected_month)

        cursor.execute(count_query, tuple(params))
        total_records = cursor.fetchone()['COUNT(*)']
        total_pages = (total_records + per_page - 1) // per_page

        base_query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

        cursor.execute(base_query, tuple(params))
        reports = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        reports = []
        total_pages = 0

    finally:
        cursor.close()
        conn.close()

    return render_template('treated_water.html', reports=reports, current_page=page, total_pages=total_pages, selected_month=selected_month)

@app.route('/treated_water/all', methods=['GET'])
def get_treated_water_data_for_printing():
    if 'loggedIn' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    session_campus = session.get('campus')

    if session_campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif session_campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [session_campus]

    month_filter = request.args.get('month', '')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM tbltreatedwater WHERE Campus IN ({placeholders})"
        params = associated_campuses

        if month_filter:
            sql += " AND Month = %s"
            params.append(month_filter)

        cursor.execute(sql, params)
        records = cursor.fetchall()

        return jsonify(records)

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)})

    finally:
        cursor.close()
        conn.close()


# Route to delete a report
@app.route('/delete_report/<int:id>', methods=['POST'])
def delete_report(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbltreatedwater WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "message": "Record deleted successfully."})

    except mysql.connector.Error as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/emu_fuel', methods=['GET', 'POST'])
def emu_fuel():
    # Ensure user is logged in
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Get the logged-in campus from the session
    user_campus = session.get('campus')

    # Determine associated campuses for specific campuses
    if user_campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif user_campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [user_campus]

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            # Retrieve submitted data from the form
            campus = request.form.get('campus')
            date = request.form.get('date')
            driver = request.form.get('driver')
            type = request.form.get('type')
            vehicle_equipment = request.form.get('vehicle_equipment')
            plate_no = request.form.get('plateNo')
            category = request.form.get('category')
            fuel_type = request.form.get('fuelType')
            item_description = request.form.get('itemDescription')
            transaction_no = request.form.get('transactionNo')
            odometer = request.form.get('odometer')
            quantity_liters = float(request.form.get('quantityLiters'))
            total_amount = float(request.form.get('totalAmount'))

            # Define emission factors and GWP for each fuel type
            emission_factors = {
                "Diesel": {
                    "CO2_factor": 2.556,
                    "NH4_factor": 0.00011,
                    "N2O_factor": 0.000151,
                    "GWP_NH4": 25,
                    "GWP_N2O": 298
                },
                "Gasoline": {
                    "CO2_factor": 2.175,
                    "NH4_factor": 0.00024,
                    "N2O_factor": 0.00058,
                    "GWP_NH4": 25,
                    "GWP_N2O": 298
                }
            }

            # Ensure valid fuel type
            if fuel_type not in emission_factors:
                return jsonify({'success': False, 'message': 'Invalid fuel type selected.'})

            # Fetch the factors for the selected fuel type
            factors = emission_factors[fuel_type]

            # Calculate emissions
            co2_emission = quantity_liters * factors["CO2_factor"]
            nh4_emission = quantity_liters * factors["NH4_factor"] * factors["GWP_NH4"]
            n2o_emission = quantity_liters * factors["N2O_factor"] * factors["GWP_N2O"]
            total_emission = co2_emission + nh4_emission + n2o_emission
            total_emission_t = total_emission / 1000

            # Insert the new record into the database
            insert_query = """
            INSERT INTO fuel_emissions (campus, date, driver, type, vehicle_equipment, plate_no, category, fuel_type, 
                                        item_description, transaction_no, odometer, quantity_liters, total_amount, 
                                        co2_emission, nh4_emission, n2o_emission, total_emission, total_emission_t)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                campus, date, driver, type, vehicle_equipment, plate_no, category, fuel_type,
                item_description, transaction_no, odometer, quantity_liters, total_amount,
                round(co2_emission, 2), round(nh4_emission, 2), round(n2o_emission, 2),
                round(total_emission, 2), round(total_emission_t, 3)
            ))
            conn.commit()

            new_record = {
                'campus': campus,
                'date': date,
                'driver': driver,
                'type': type,
                'vehicle_equipment': vehicle_equipment,
                'plate_no': plate_no,
                'category': category,
                'fuel_type': fuel_type,
                'quantity_liters': quantity_liters,
                'total_amount': total_amount,
                'co2_emission': round(co2_emission, 2),
                'nh4_emission': round(nh4_emission, 2),
                'n2o_emission': round(n2o_emission, 2),
                'total_emission': round(total_emission, 2),
                'total_emission_t': round(total_emission_t, 3)
            }

            return jsonify({'success': True, 'data': new_record})

        # Handle GET request for fetching data
        page = request.args.get('page', 1, type=int)
        per_page = 20
        offset = (page - 1) * per_page

        # Retrieve filter parameters
        year_filter = request.args.get('year', '')
        category_filter = request.args.get('category', '')
        fuel_type_filter = request.args.get('fuelType', '')

        # Prepare SQL query for fetching data
        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM fuel_emissions WHERE campus IN ({placeholders})"
        params = associated_campuses

        if year_filter:
            sql += " AND YEAR(date) = %s"
            params.append(year_filter)
        if category_filter:
            sql += " AND category = %s"
            params.append(category_filter)
        if fuel_type_filter:
            sql += " AND fuel_type = %s"
            params.append(fuel_type_filter)

        # Count query for pagination
        count_query = f"SELECT COUNT(*) AS total FROM ({sql}) AS total_query"
        cursor.execute(count_query, tuple(params))
        total_records = cursor.fetchone()['total']
        total_pages = (total_records + per_page - 1) // per_page

        # Add pagination to the query
        sql += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

        # Execute the final query
        cursor.execute(sql, tuple(params))
        reports = cursor.fetchall()

        return render_template('emu_fuel.html', reports=reports, current_page=page, total_pages=total_pages)

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        reports = []
        total_pages = 0

    finally:
        cursor.close()
        conn.close()

@app.route('/emu_fuel/all', methods=['GET'])
def get_fuel_data_for_printing():
    if 'loggedIn' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    user_campus = session.get('campus')

    if user_campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif user_campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [user_campus]

    year_filter = request.args.get('year', '')
    category_filter = request.args.get('category', '')
    fuel_type_filter = request.args.get('fuelType', '')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM fuel_emissions WHERE campus IN ({placeholders})"
        params = associated_campuses

        if year_filter:
            sql += " AND YEAR(date) = %s"
            params.append(year_filter)
        if category_filter:
            sql += " AND category = %s"
            params.append(category_filter)
        if fuel_type_filter:
            sql += " AND fuel_type = %s"
            params.append(fuel_type_filter)

        cursor.execute(sql, params)
        records = cursor.fetchall()

        return jsonify(records)

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)})

    finally:
        cursor.close()
        conn.close()

@app.route('/delete_fuel_record/<int:id>', methods=['DELETE'])
def delete_fuel_record(id):
    if 'loggedIn' not in session:
        return jsonify({'success': False, 'message': 'User is not logged in.'})

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # SQL query to delete the record
        sql = "DELETE FROM fuel_emissions WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()

        # Return success if deletion was successful
        if cursor.rowcount > 0:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Record not found.'})

    except mysql.connector.Error as e:
        return jsonify({'success': False, 'message': f"Database error: {e}"})

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/waste_segregation', methods=['GET', 'POST'])
def waste_segregation():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    campus = session.get('campus')
    if not campus:
        flash("No campus found in session.", "danger")
        return redirect(url_for('emu_dashboard'))

    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page

    # Handle POST request (adding new records)
    if request.method == 'POST':
        try:
            year = request.form.get('year')
            month = request.form.get('month')
            quarter = request.form.get('quarter')
            main_category = request.form.get('mainCategory')
            sub_category = request.form.get('subCategory')
            quantity = float(request.form.get('quantity'))

            emission_factors = {
                "Biodegradable": {
                    "Garden Waste": 0.57896,
                    "Food Waste": 0.62687,
                    "Mixed Food & Garden Waste": 0.58734
                },
                "Recyclable": {
                    "Plastic Waste": 0.00890,
                    "Metal Waste": 0.00890,
                    "Paper Waste": 1.04180,
                    "Glass Waste": 0.00890
                },
                "Residual": {
                    "Residual Waste": 0.44624
                },
                "Special": {
                    "Hazardous Waste": 0.00890
                }
            }

            emission_factor = emission_factors.get(main_category, {}).get(sub_category)
            if emission_factor is None:
                raise ValueError("Invalid main category or subcategory")

            ghg_emission_kg = quantity * emission_factor
            ghg_emission_t = ghg_emission_kg / 1000

            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """INSERT INTO tblsolidwastesegregated 
                     (Campus, Year, Quarter, Month, MainCategory, SubCategory, QuantityInKG, GHGEmissionKGCO2e, GHGEmissionTCO2e)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (campus, year, quarter, month, main_category, sub_category, quantity, ghg_emission_kg, ghg_emission_t))
            conn.commit()

            flash("Waste segregation record added successfully.", "success")
        except (mysql.connector.Error, ValueError) as e:
            flash(f"Error: {e}", "danger")
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('waste_segregation'))

    # Handle GET request (display reports with optional filtering)
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM tblsolidwastesegregated WHERE Campus = %s"
        params = [campus]

        # Apply filtering if present
        month_filter = request.args.get('month')
        quarter_filter = request.args.get('quarter')
        year_filter = request.args.get('year')

        if month_filter:
            sql += " AND Month = %s"
            params.append(month_filter)
        if quarter_filter:
            sql += " AND Quarter = %s"
            params.append(quarter_filter)
        if year_filter:
            sql += " AND Year = %s"
            params.append(year_filter)

        # Get total records count with current filters
        count_sql = f"SELECT COUNT(*) FROM ({sql}) AS count_query"
        cursor.execute(count_sql, tuple(params))
        total_records = cursor.fetchone()['COUNT(*)']
        total_pages = (total_records + per_page - 1) // per_page

        # Apply pagination
        sql += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

        cursor.execute(sql, tuple(params))
        reports = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        reports = []
        total_pages = 0
    finally:
        cursor.close()
        conn.close()

    return render_template(
        'waste_segregation.html',
        reports=reports,
        current_page=page,
        total_pages=total_pages,
        selected_month=month_filter,
        selected_quarter=quarter_filter,
        selected_year=year_filter
    )



# Updated route with a unique function name
@app.route('/delete_waste_record/<int:record_id>', methods=['DELETE'])
def delete_waste_record_by_id(record_id):  # Changed function name to avoid conflicts
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM tblsolidwastesegregated WHERE id = %s"
        cursor.execute(sql, (record_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'success': False, 'message': 'Record not found.'}), 404
        return jsonify({'success': True, 'message': 'Record deleted successfully.'})
    except mysql.connector.Error as e:
        return jsonify({'success': False, 'message': f'Database error: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/waste_segregation/all', methods=['GET'])
def get_waste_segregation_data_for_printing():
    # Ensure user is logged in
    if 'loggedIn' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    campus = session.get('campus')
    if not campus:
        return jsonify({"error": "No campus found in session"}), 400

    # Retrieve filter parameters from request arguments
    month_filter = request.args.get('month')
    quarter_filter = request.args.get('quarter')
    year_filter = request.args.get('year')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Build base SQL query
        sql = "SELECT * FROM tblsolidwastesegregated WHERE Campus = %s"
        params = [campus]

        # Append filter conditions dynamically
        if month_filter:
            sql += " AND Month = %s"
            params.append(month_filter)
        if quarter_filter:
            sql += " AND Quarter = %s"
            params.append(quarter_filter)
        if year_filter:
            sql += " AND Year = %s"
            params.append(year_filter)

        # Execute query
        cursor.execute(sql, params)
        records = cursor.fetchall()

        return jsonify(records)  # Return fetched data as JSON

    except mysql.connector.Error as e:
        return jsonify({"error": f"Database Error: {e}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()




# Route for Waste Unsegregation
@app.route('/waste_unsegregation', methods=['GET'])
def waste_unsegregation():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Get the logged-in campus from the session
    campus = session.get('campus')

    # Determine which campuses to include in the query
    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        # For any other campus, include only that campus
        associated_campuses = [campus]

    # Set up pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page

    selected_year = request.args.get('year')
    selected_month = request.args.get('month')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Create the SQL query with dynamic placeholders for associated campuses
        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM tblsolidwasteunsegregated WHERE Campus IN ({placeholders})"
        count_sql = f"SELECT COUNT(*) AS total FROM tblsolidwasteunsegregated WHERE Campus IN ({placeholders})"
        params = associated_campuses

        if selected_year:
            sql += " AND Year = %s"
            count_sql += " AND Year = %s"
            params.append(selected_year)

        if selected_month:
            sql += " AND Month = %s"
            count_sql += " AND Month = %s"
            params.append(selected_month)

        # Get total record count for pagination
        cursor.execute(count_sql, params)
        total_records = cursor.fetchone()['total']
        total_pages = (total_records + per_page - 1) // per_page

        # Apply pagination
        sql += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])
        cursor.execute(sql, params)
        reports = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        reports = []
        total_pages = 0

    finally:
        cursor.close()
        conn.close()

    return render_template(
        'waste_unsegregation.html',
        reports=reports,
        current_page=page,
        total_pages=total_pages,
        selected_year=selected_year,
        selected_month=selected_month
    )

# Route to fetch all or filtered waste unsegregated data for printing
@app.route('/waste_unsegregation/all', methods=['GET'])
def get_waste_unsegregated_data_for_printing():
    if 'loggedIn' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    campus = session.get('campus')

    # Determine associated campuses
    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [campus]

    selected_year = request.args.get('year')
    selected_month = request.args.get('month')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM tblsolidwasteunsegregated WHERE Campus IN ({placeholders})"
        params = associated_campuses

        if selected_year:
            sql += " AND Year = %s"
            params.append(selected_year)

        if selected_month:
            sql += " AND Month = %s"
            params.append(selected_month)

        cursor.execute(sql, params)
        records = cursor.fetchall()

        return jsonify(records)

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)})

    finally:
        cursor.close()
        conn.close()

# Route for handling the addition of waste unsegregation data via POST request
@app.route('/add_waste_unsegregated', methods=['POST'])
def add_waste_unsegregated():
    try:
        campus = request.form.get('campus')
        year = request.form.get('year')
        month = request.form.get('month')
        waste_type = request.form.get('wasteType')
        
        quantity_kg = float(request.form.get('quantityKg') or 0)
        sent_to_landfill_kg = float(request.form.get('sentToLandfillKg') or 0)

        sent_to_landfill_tons = sent_to_landfill_kg / 1000
        percentage = (sent_to_landfill_kg / quantity_kg * 100) if quantity_kg else 0

        ghg_emission_kg_co2e = sent_to_landfill_tons * 0.8 * 0.25 * 0.5 * 0.5 * 1.33 * 1000
        ghg_emission_t_co2e = ghg_emission_kg_co2e / 1000

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO tblsolidwasteunsegregated 
            (Campus, Year, Month, WasteType, QuantityInKG, SentToLandfillKG, SentToLandfillTONS, Percentage, GHGEmissionKGCO2e, GHGEmissionTCO2e)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            campus, year, month, waste_type, quantity_kg, sent_to_landfill_kg,
            sent_to_landfill_tons, percentage, ghg_emission_kg_co2e, ghg_emission_t_co2e
        ))
        conn.commit()

        flash("Waste unsegregated record added successfully.", "success")
        return redirect(url_for('waste_unsegregation'))

    except (ValueError, TypeError) as e:
        flash(f"Invalid input data: {e}", "danger")
        return redirect(url_for('waste_unsegregation'))

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        return redirect(url_for('waste_unsegregation'))

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()



# Route for deleting a waste record
@app.route('/delete_waste_record/<int:record_id>', methods=['DELETE'])
def delete_waste_record(record_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete record from the database
        cursor.execute("DELETE FROM tblsolidwasteunsegregated WHERE id = %s", (record_id,))
        conn.commit()

        return jsonify({'success': True, 'message': 'Record deleted successfully'})

    except mysql.connector.Error as e:
        return jsonify({'success': False, 'message': str(e)})

    finally:
        cursor.close()
        conn.close()


# Route for managing accounts
bcrypt = Bcrypt(app)  # Initialize Bcrypt

@app.route('/manage_account', methods=['GET', 'POST'])
def manage_account():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        office = request.form['office']
        campus = request.form['campus']
        email = request.form['email']
        password = request.form['password']

        # Hash the password for security
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert new account into tblsignin table
            insert_query = """
            INSERT INTO tblsignin (username, office, campus, email, password)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (username, office, campus, email, hashed_password))
            conn.commit()

            flash("Account created successfully!", "success")
            return redirect(url_for('manage_account'))

        except mysql.connector.Error as e:
            flash(f"An error occurred: {e}", "danger")

        finally:
            cursor.close()
            conn.close()

    return render_template('manage_account.html')

from datetime import datetime
from flask import session, redirect, url_for, request, render_template, flash
import mysql.connector
from prophet import Prophet
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np

from datetime import datetime
from flask import session, redirect, url_for, request, render_template, flash
import mysql.connector
from prophet import Prophet
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np


@app.route('/csd_dashboard')
def csd_dashboard():
    # Ensure the user is logged in
    if 'loggedIn' not in session:
        flash("You need to be logged in to access this page.", "warning")
        return redirect(url_for('login'))

    selected_campus = request.args.get('campus', 'all')  # Get selected campus from the URL args

    # Initialize data lists
    electricity_data = []
    fuel_emissions_data = []
    water_data = []
    lpg_data = []
    food_waste_data = []
    treated_water_data =[]
    solid_waste_unsegregated_data = []
    solid_waste_segregated_data = []
    accommodation_data = []
    flight_data = []

    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Could not establish database connection.")

        cursor = conn.cursor(dictionary=True)

        # Function to execute queries for fetching data
        def fetch_data(query, params=None):
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()

        # Fetch data for all resources
        if selected_campus == 'all':
            electricity_data = fetch_data(
                "SELECT month, year, kg_co2_per_kwh FROM electricity_consumption "
                "WHERE year BETWEEN 2020 AND 2024 ORDER BY year, month ASC"
            )
            fuel_emissions_data = fetch_data(
                "SELECT date, total_emission FROM fuel_emissions "
                "WHERE YEAR(date) BETWEEN 2020 AND 2024 ORDER BY date ASC"
            )
            water_data = fetch_data(
                "SELECT Date, FactorKGCO2e FROM tblwater "
                "WHERE YEAR(Date) BETWEEN 2020 AND 2024 ORDER BY Date ASC"
            )
            treated_water_data = fetch_data(
                """SELECT MONTH(Month) AS Month, YEAR(Month) AS Year, SUM(FactorKGCO2e) AS TotalFactorKGCO2e
                FROM tbltreatedwater
                WHERE YEAR(Month) BETWEEN 2020 AND 2024
                GROUP BY YEAR(Month), MONTH(Month)
                ORDER BY YEAR(Month), MONTH(Month)"""
            )
            lpg_data = fetch_data(
                "SELECT Month, GHGEmissionKGCO2e FROM tbllpg "
                "WHERE YearTransact BETWEEN 2020 AND 2024 ORDER BY YearTransact, Month ASC"
            )
            food_waste_data = fetch_data(
                "SELECT Month, YearTransaction, GHGEmissionKGCO2e FROM tblfoodwaste "
                "WHERE YearTransaction BETWEEN 2020 AND 2024 ORDER BY YearTransaction, Month ASC"
            )
            solid_waste_unsegregated_data = fetch_data(
                "SELECT Month, Year, GHGEmissionKGCO2e FROM tblsolidwasteunsegregated "
                "WHERE Year BETWEEN 2020 AND 2024 ORDER BY Year, month ASC"
            )
            solid_waste_segregated_data = fetch_data(
                "SELECT Month, Year, SUM(GHGEmissionKGCO2e) as TotalEmissions FROM tblsolidwastesegregated "
                "WHERE Year BETWEEN 2020 AND 2024 "
                "GROUP BY Year, Month ORDER BY Year, FIELD(Month, 'January', 'February', 'March', 'April', "
                "'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')"
            )
            accommodation_data = fetch_data(
                "SELECT YearTransact, SUM(GHGEmissionKGC02e) as TotalEmissions FROM tblaccommodation "
                "WHERE YearTransact BETWEEN 2020 AND 2024 GROUP BY YearTransact ORDER BY YearTransact ASC"
            )
            flight_data = fetch_data(
                "SELECT Year, SUM(GHGEmissionKGC02e) as TotalEmissions FROM tblflight "
                "WHERE Year BETWEEN 2020 AND 2024 GROUP BY Year ORDER BY Year ASC"
            )
        else:
            query_filter = " WHERE campus = %s AND year BETWEEN 2020 AND 2024 ORDER BY year, month ASC"
            electricity_data = fetch_data(
                "SELECT month, year, kg_co2_per_kwh FROM electricity_consumption" + query_filter,
                (selected_campus,)
            )
            fuel_emissions_data = fetch_data(
                "SELECT date, total_emission FROM fuel_emissions "
                "WHERE campus = %s AND YEAR(date) BETWEEN 2020 AND 2024 ORDER BY date ASC",
                (selected_campus,)
            )
            water_data = fetch_data(
                "SELECT Date, FactorKGCO2e FROM tblwater "
                "WHERE Campus = %s AND YEAR(Date) BETWEEN 2020 AND 2024 ORDER BY Date ASC",
                (selected_campus,)
            )
            treated_water_data = fetch_data(
                """SELECT MONTH(Month) AS Month, YEAR(Month) AS Year, SUM(FactorKGCO2e) AS TotalFactorKGCO2e
                FROM tbltreatedwater
                WHERE Campus = %s AND YEAR(Month) BETWEEN 2020 AND 2024
                GROUP BY YEAR(Month), MONTH(Month)
                ORDER BY YEAR(Month), MONTH(Month)""",
                (selected_campus,)  # Pass selected_campus as a tuple
            )
            lpg_data = fetch_data(
                "SELECT Month, GHGEmissionKGCO2e FROM tbllpg "
                "WHERE Campus = %s AND YearTransact BETWEEN 2020 AND 2024 ORDER BY YearTransact, Month ASC",
                (selected_campus,)
            )
            food_waste_data = fetch_data(
                "SELECT Month, YearTransaction, GHGEmissionKGCO2e FROM tblfoodwaste "
                "WHERE Campus = %s AND YearTransaction BETWEEN 2020 AND 2024 ORDER BY YearTransaction, Month ASC",
                (selected_campus,)
            )
            solid_waste_unsegregated_data = fetch_data(
                "SELECT Month, Year, GHGEmissionKGCO2e FROM tblsolidwasteunsegregated "
                "WHERE Campus = %s AND Year BETWEEN 2020 AND 2024 ORDER BY Year, month ASC",
                (selected_campus,)
            )
            solid_waste_segregated_data = fetch_data(
                "SELECT Month, Year, SUM(GHGEmissionKGCO2e) as TotalEmissions FROM tblsolidwastesegregated "
                "WHERE Campus = %s AND Year BETWEEN 2020 AND 2024 "
                "GROUP BY Year, Month ORDER BY Year, FIELD(Month, 'January', 'February', 'March', 'April', "
                "'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')",
                (selected_campus,)
            )
            accommodation_data = fetch_data(
                "SELECT YearTransact, SUM(GHGEmissionKGC02e) as TotalEmissions FROM tblaccommodation "
                "WHERE Campus = %s AND YearTransact BETWEEN 2020 AND 2024 GROUP BY YearTransact ORDER BY YearTransact ASC",
                (selected_campus,)
            )
            flight_data = fetch_data(
                "SELECT Year, SUM(GHGEmissionKGC02e) as TotalEmissions FROM tblflight "
                "WHERE Campus = %s AND Year BETWEEN 2020 AND 2024 GROUP BY Year ORDER BY Year ASC",
                (selected_campus,)
            )

    except Exception as e:
        flash(f"Database Error: {e}", "danger")
        return render_template("error.html", message=f"Database Error: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

    # Helper function to extract and forecast data with Prophet
    def forecast_with_prophet(data, start_date, periods=12):
        if len(data) > 1:
            try:
                df = pd.DataFrame({'ds': pd.date_range(start=start_date, periods=len(data), freq='M'), 'y': data})
                df = df[df['y'] > 0]
                model = Prophet(yearly_seasonality=True)
                model.fit(df)
                future = model.make_future_dataframe(periods=periods, freq='M')
                forecast = model.predict(future)
                return forecast['yhat'][-periods:].tolist(), df['y'].tolist(), forecast['ds'][-periods:].dt.strftime('%m/%Y').tolist()
            except Exception as e:
                flash(f"Prophet Error: {e}", "danger")
                avg_value = sum(data) / len(data)
                return [avg_value] * periods, data, ['01/24'] * periods
        else:
            flash("Insufficient data for forecasting", "warning")
            return [0] * periods, data, ['01/24'] * periods

    # Prepare the actual and forecasted data for electricity
    actual_electricity_values = [row['kg_co2_per_kwh'] for row in electricity_data if row['kg_co2_per_kwh'] is not None]
    electricity_months = [f"{row['month']}/{row['year']}" for row in electricity_data]
    electricity_forecasted_values, actual_electricity_values_filtered, electricity_forecast_months = forecast_with_prophet(
        actual_electricity_values, start_date='2020-01-01', periods=12
    )

    # Prepare the actual and forecasted data for fuel emissions
    actual_fuel_emissions_values = [row['total_emission'] for row in fuel_emissions_data if row['total_emission'] is not None]
    fuel_emissions_dates = [row['date'].strftime('%m/%Y') for row in fuel_emissions_data]
    fuel_emissions_forecasted_values, actual_fuel_emissions_values_filtered, fuel_emissions_forecast_dates = forecast_with_prophet(
        actual_fuel_emissions_values, start_date='2020-01-01', periods=12
    )

    # Prepare the actual and forecasted data for water
    actual_water_values = [row['FactorKGCO2e'] for row in water_data if row['FactorKGCO2e'] is not None]
    water_dates = [row['Date'].strftime('%m/%Y') for row in water_data]
    water_forecasted_values, actual_water_values_filtered, water_forecast_dates = forecast_with_prophet(
        actual_water_values, start_date='2020-01-01', periods=12
    )

    # Prepare the actual and forecasted data for LPG
    actual_lpg_values = [row['GHGEmissionKGCO2e'] for row in lpg_data if row['GHGEmissionKGCO2e'] is not None]
    lpg_months = [row['Month'] for row in lpg_data]
    lpg_forecasted_values, actual_lpg_values_filtered, lpg_forecast_months = forecast_with_prophet(
        actual_lpg_values, start_date='2020-01-01', periods=12
    )

    # Prepare the actual and forecasted data for food waste
    actual_food_waste_values = [row['GHGEmissionKGCO2e'] for row in food_waste_data if row['GHGEmissionKGCO2e'] is not None]
    food_waste_months = [f"{row['Month']}/{row['YearTransaction']}" for row in food_waste_data]
    food_waste_forecasted_values, actual_food_waste_values_filtered, food_waste_forecast_months = forecast_with_prophet(
        actual_food_waste_values, start_date='2020-01-01', periods=12
    )
    actual_solid_waste_unsegregated_values = [row['GHGEmissionKGCO2e'] for row in solid_waste_unsegregated_data if row['GHGEmissionKGCO2e'] is not None]
    solid_waste_unsegregated_months = [f"{row['Month']}/{row['Year']}" for row in solid_waste_unsegregated_data]
    solid_waste_unsegregated_forecasted_values, actual_solid_waste_unsegregated_values_filtered, solid_waste_unsegregated_forecast_months = forecast_with_prophet(
        actual_solid_waste_unsegregated_values, start_date='2020-01-01', periods=12
    )
    actual_solid_waste_segregated_values = [row['TotalEmissions'] for row in solid_waste_segregated_data if row['TotalEmissions'] is not None]
    solid_waste_segregated_months = [f"{row['Month']}/{row['Year']}" for row in solid_waste_segregated_data]
    solid_waste_segregated_forecasted_values, actual_solid_waste_segregated_values_filtered, solid_waste_segregated_forecast_months = forecast_with_prophet(
        actual_solid_waste_segregated_values, start_date='2020-01-01', periods=12
    )
    actual_accommodation_values = [row['TotalEmissions'] for row in accommodation_data if row['TotalEmissions'] is not None]
    accommodation_years = [row['YearTransact'] for row in accommodation_data]
    accommodation_forecasted_values, actual_accommodation_values_filtered, accommodation_forecast_years = forecast_with_prophet(
        actual_accommodation_values, start_date='2020-01-01', periods=5
    )

    # Prepare flight data
    actual_flight_values = [row['TotalEmissions'] for row in flight_data if row['TotalEmissions'] is not None]
    flight_years = [row['Year'] for row in flight_data]
    flight_forecasted_values, actual_flight_values_filtered, flight_forecast_years = forecast_with_prophet(
        actual_flight_values, start_date='2020-01-01', periods=5
    )

    # Prepare the actual and forecasted data for treated water
    actual_treated_water_values = [row['TotalFactorKGCO2e'] for row in treated_water_data if row['TotalFactorKGCO2e'] is not None]
    treated_water_months = [f"{row['Month']}/{row['Year']}" for row in treated_water_data]
    treated_water_forecasted_values, actual_treated_water_values_filtered, treated_water_forecast_months = forecast_with_prophet(
        actual_treated_water_values, start_date='2020-01-01', periods=12
    )

    # Add treated water data to the template context
    return render_template(
        'csd_dashboard.html',
        actual_electricity_values=actual_electricity_values_filtered,
        electricity_forecasted_values=electricity_forecasted_values,
        electricity_months=electricity_months,
        electricity_forecast_months=electricity_forecast_months,
        actual_fuel_emissions_values=actual_fuel_emissions_values_filtered,
        fuel_emissions_forecasted_values=fuel_emissions_forecasted_values,
        fuel_emissions_dates=fuel_emissions_dates,
        fuel_emissions_forecast_dates=fuel_emissions_forecast_dates,
        actual_water_values=actual_water_values_filtered,
        water_forecasted_values=water_forecasted_values,
        water_dates=water_dates,
        water_forecast_dates=water_forecast_dates,
        actual_lpg_values=actual_lpg_values_filtered,
        lpg_forecasted_values=lpg_forecasted_values,
        lpg_months=lpg_months,
        lpg_forecast_months=lpg_forecast_months,
        actual_food_waste_values=actual_food_waste_values_filtered,
        food_waste_forecasted_values=food_waste_forecasted_values,
        food_waste_months=food_waste_months,
        food_waste_forecast_months=food_waste_forecast_months,
        actual_solid_waste_unsegregated_values=actual_solid_waste_unsegregated_values_filtered,
        solid_waste_unsegregated_forecasted_values=solid_waste_unsegregated_forecasted_values,
        solid_waste_unsegregated_months=solid_waste_unsegregated_months,
        solid_waste_unsegregated_forecast_months=solid_waste_unsegregated_forecast_months,
        actual_solid_waste_segregated_values=actual_solid_waste_segregated_values_filtered,
        solid_waste_segregated_forecasted_values=solid_waste_segregated_forecasted_values,
        solid_waste_segregated_months=solid_waste_segregated_months,
        solid_waste_segregated_forecast_months=solid_waste_segregated_forecast_months,
        actual_accommodation_values=actual_accommodation_values_filtered,
        accommodation_forecasted_values=accommodation_forecasted_values,
        accommodation_years=accommodation_years,
        accommodation_forecast_years=accommodation_forecast_years,
        actual_flight_values=actual_flight_values_filtered,
        flight_forecasted_values=flight_forecasted_values,
        flight_years=flight_years,
        flight_forecast_years=flight_forecast_years,
        actual_treated_water_values=actual_treated_water_values_filtered,
        treated_water_forecasted_values=treated_water_forecasted_values,
        treated_water_months=treated_water_months,
        treated_water_forecast_months=treated_water_forecast_months,
        selected_campus=selected_campus,
    )


# Helper function to fetch data from the database with pagination and filtering
def fetch_electricity_data(page, per_page, campus=None, category=None, month=None, year=None, quarter=None):
    offset = (page - 1) * per_page
    query = "SELECT * FROM electricity_consumption WHERE 1=1"
    total_query = "SELECT COUNT(*) AS total FROM electricity_consumption WHERE 1=1"
    params = []

    # Add filters to the query if they are provided
    if campus:
        query += " AND campus = %s"
        total_query += " AND campus = %s"
        params.append(campus)
    if category:
        query += " AND category = %s"
        total_query += " AND category = %s"
        params.append(category)
    if month:
        query += " AND month = %s"
        total_query += " AND month = %s"
        params.append(month)
    if year:
        query += " AND year = %s"
        total_query += " AND year = %s"
        params.append(year)
    if quarter:
        query += " AND quarter = %s"
        total_query += " AND quarter = %s"
        params.append(quarter)

    # Add pagination
    query += " LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    data = []
    total_records = 0
    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)

        # Fetch limited records for the current page
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()

        # Fetch the total number of records to calculate total pages
        cursor.execute(total_query, tuple(params[:-2]))  # Exclude LIMIT and OFFSET params
        total_records = cursor.fetchone()["total"]

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    return data, total_records


# Route for Electricity Report with pagination and filtering
@app.route('/report/electricity')
def electricity_report():
    # Define pagination parameters
    per_page = 20  # Number of records per page
    current_page = request.args.get("page", 1, type=int)
    
    # Retrieve filter parameters from the request
    campus = request.args.get("campus")
    category = request.args.get("category")
    month = request.args.get("month")
    year = request.args.get("year")
    quarter = request.args.get("quarter")
    
    # Fetch data for the current page with filters applied
    data, total_records = fetch_electricity_data(
        current_page, per_page, campus=campus, category=category, month=month, year=year, quarter=quarter
    )
    
    # Calculate total pages
    total_pages = math.ceil(total_records / per_page)
    
    return render_template(
        'electricity_report.html', 
        data=data, 
        current_page=current_page, 
        total_pages=total_pages,
        campus=campus,
        category=category,
        month=month,
        year=year,
        quarter=quarter
    )
@app.route('/download_electricity_pdf')
def download_electricity_pdf():
    campus = request.args.get("campus", None)
    category = request.args.get("category", None)
    month = request.args.get("month", None)
    quarter = request.args.get("quarter", None)
    year = request.args.get("year", None)

    query = "SELECT * FROM electricity_consumption WHERE 1=1"
    params = []

    if campus:
        query += " AND campus = %s"
        params.append(campus)
    if category:
        query += " AND category = %s"
        params.append(category)
    if month:
        query += " AND month = %s"
        params.append(month)
    if quarter:
        query += " AND quarter = %s"
        params.append(quarter)
    if year:
        query += " AND year = %s"
        params.append(year)

    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(query, params)
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    # Convert data to DataFrame
    df = pd.DataFrame(data)
    
    # Handle empty data case
    if df.empty:
        return "No data available to generate PDF", 404

    # Calculate column width to fit all columns within the page width
    page_width = landscape(A4)[0] - 20  # 20 for margins
    num_columns = len(df.columns)
    col_width = page_width / num_columns

    # Create PDF in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to list of lists
    data_list = [df.columns.tolist()] + df.values.tolist()  # Headers and data rows

    # Define table with dynamic column widths
    table = Table(data_list, colWidths=[col_width] * num_columns)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),  # Smaller font for more data
        ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ]))

    # Build the PDF with the table
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="electricity_consumption_report.pdf", as_attachment=True, mimetype='application/pdf')

@app.route('/fetch_all_electricity_data')
def fetch_all_electricity_data():
    # Retrieve filter parameters from the request
    campus = request.args.get("campus")
    category = request.args.get("category")
    month = request.args.get("month")
    year = request.args.get("year")
    quarter = request.args.get("quarter")

    # Prepare the SQL query with conditional filters
    sql = "SELECT * FROM electricity_consumption WHERE 1=1"
    params = []

    if campus:
        sql += " AND campus = %s"
        params.append(campus)
    if category:
        sql += " AND category = %s"
        params.append(category)
    if month:
        sql += " AND month = %s"
        params.append(month)
    if year:
        sql += " AND year = %s"
        params.append(year)
    if quarter:
        sql += " AND quarter = %s"
        params.append(quarter)

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Execute the query with the collected parameters
        cursor.execute(sql, params)
        data = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        data = []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Return the data as JSON for printing purposes
    return jsonify(data)


# Helper function to fetch filtered and paginated data from the database
def fetch_filtered_fuel_emissions_data(campus, year, page, per_page):
    offset = (page - 1) * per_page
    base_query = "SELECT * FROM fuel_emissions"
    filters = []
    parameters = []
    
    # Filter by campus if selected
    if campus:
        filters.append("campus = %s")
        parameters.append(campus)
    
    # Filter by year if selected
    if year:
        filters.append("YEAR(date) = %s")  # Assumes `date` is the column storing the date in the database
        parameters.append(year)
    
    # Construct the final query with filters and pagination
    query = base_query + (" WHERE " + " AND ".join(filters) if filters else "") + " LIMIT %s OFFSET %s"
    parameters.extend([per_page, offset])
    
    # Query to count total records after applying filters
    count_query = "SELECT COUNT(*) AS total FROM fuel_emissions" + (" WHERE " + " AND ".join(filters) if filters else "")
    
    data = []
    total_records = 0
    
    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        
        # Get filtered data for the current page
        cursor.execute(query, parameters)
        data = cursor.fetchall()
        
        # Get the total record count for pagination
        cursor.execute(count_query, parameters[:-2])  # Exclude limit and offset for count query
        total_records = cursor.fetchone()['total']
        
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()
    
    return data, total_records

# Route for Fuel Emissions Report with pagination and filters
@app.route('/report/fuel_emissions')
def fuel_emissions_report():
    # Pagination settings
    per_page = 20  # Records per page
    current_page = request.args.get('page', 1, type=int)
    
    # Retrieve filter parameters
    campus = request.args.get('campus', '')
    year = request.args.get('year', '')

    # Fetch data for the current page with filters
    data, total_records = fetch_filtered_fuel_emissions_data(campus, year, current_page, per_page)
    
    # Calculate total pages for pagination
    total_pages = math.ceil(total_records / per_page)
    
    return render_template(
        'fuel_emissions_report.html', 
        data=data,
        current_page=current_page,
        total_pages=total_pages,
        campus=campus,
        year=year  # Pass year to retain filter selection
    )

def fetch_all_filtered_fuel_emissions_data(campus, year):
    base_query = "SELECT * FROM fuel_emissions"
    filters = []
    parameters = []
    
    if campus:
        filters.append("campus = %s")
        parameters.append(campus)
    
    if year:
        filters.append("YEAR(date) = %s")
        parameters.append(year)
    
    query = base_query + (" WHERE " + " AND ".join(filters) if filters else "")
    
    data = []
    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(query, parameters)
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()
    
    return data

@app.route('/report/fuel_emissions/all_data')
def all_fuel_emissions_data():
    campus = request.args.get('campus', '')
    year = request.args.get('year', '')
    
    # Fetch all data based on the filters
    data = fetch_all_filtered_fuel_emissions_data(campus, year)
    
    # Return data as JSON
    return jsonify(data)

@app.route('/download_fuel_emissions_pdf')
def download_fuel_emissions_pdf():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)

    # Fetch all data based on the filters
    query = "SELECT * FROM fuel_emissions WHERE 1=1"
    params = []

    if campus:
        query += " AND campus = %s"
        params.append(campus)
    
    if year:
        query += " AND YEAR(date) = %s"
        params.append(year)

    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(query, params)
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Handle empty data case
    if df.empty:
        return "No data available to generate PDF", 404

    # Calculate column width to fit all columns within the page width
    page_width = landscape(A4)[0] - 20  # 20 for total left and right margins
    num_columns = len(df.columns)
    col_width = page_width / num_columns

    # Create a PDF file in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to list of lists
    data_list = [df.columns.tolist()] + df.values.tolist()  # Add headers and data rows

    # Define table with dynamic column widths
    table = Table(data_list, colWidths=[col_width] * num_columns)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 6),  # Further reduce font size to 6
        ('GRID', (0, 0), (-1, -1), 0.3, colors.black),  # Thinner grid lines
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ]))

    # Build the PDF with the table
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="fuel_emissions_report.pdf", as_attachment=True, mimetype='application/pdf')


def fetch_treated_water_data(page=1, per_page=20, campus=None, month=None):
    base_query = "SELECT * FROM tbltreatedwater WHERE 1=1"  # Start with a condition that always matches
    total_query = "SELECT COUNT(*) AS total FROM tbltreatedwater WHERE 1=1"
    params = []

    # Apply campus filter if provided
    if campus:
        base_query += " AND campus = %s"
        total_query += " AND campus = %s"
        params.append(campus)

    # Apply month filter if provided
    if month:
        base_query += " AND month = %s"
        total_query += " AND month = %s"
        params.append(month)

    # Handle pagination if page and per_page are provided
    if page is not None and per_page is not None:
        offset = (page - 1) * per_page
        base_query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

    data = []
    total_records = 0

    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)

        # Fetch records with filters
        cursor.execute(base_query, params)
        data = cursor.fetchall()

        # Fetch total count of filtered records
        if page is not None and per_page is not None:
            cursor.execute(total_query, params[:-2])  # Exclude pagination params for count query
            total_records = cursor.fetchone()["total"]
        else:
            cursor.execute(total_query, params)  # No pagination params for full count
            total_records = cursor.fetchone()["total"]

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    return data, total_records



# Route for Treated Water Report with pagination and filters
@app.route('/report/treated_water')
def treated_water_report():
    per_page = 20  # Number of records per page
    current_page = request.args.get("page", 1, type=int)
    
    # Get campus and month filter values from the request args
    campus = request.args.get("campus", None)
    month = request.args.get("month", None)  # Month should be numeric, e.g., '01', '02'

    # Fetch paginated and filtered data
    data, total_records = fetch_treated_water_data(page=current_page, per_page=per_page, campus=campus, month=month)
    
    # Calculate total pages based on filtered results
    total_pages = math.ceil(total_records / per_page)
    
    return render_template(
        'treated_water_report.html',
        data=data,
        current_page=current_page,
        total_pages=total_pages,
        campus=campus,
        month=month
    )

def fetch_all_treated_water_data(campus=None, month=None):
    query = "SELECT * FROM tbltreatedwater WHERE 1=1"
    params = []
    
    if campus:
        query += " AND Campus = %s"
        params.append(campus)
    
    if month:
        query += " AND Month = %s"
        params.append(month)
    
    data = []
    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(query, params)
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching all data: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    return data

@app.route('/report/treated_water/all_data')
def all_treated_water_data():
    campus = request.args.get('campus', '')
    month = request.args.get('month', '')

    data = fetch_all_treated_water_data(campus, month)
    return jsonify(data)

@app.route('/download_treated_water_pdf')
def download_treated_water_pdf():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    month = request.args.get("month", None)

    # Fetch all data based on the filters
    data, _ = fetch_treated_water_data(page=None, per_page=None, campus=campus, month=month)

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Handle empty data case
    if df.empty:
        return "No data available to generate PDF", 404

    # Create a PDF file in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to list of lists
    data_list = [df.columns.tolist()] + df.values.tolist()  # Add headers and data rows

    # Create table and style
    table = Table(data_list)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the PDF with the table
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="treated_water_report.pdf", as_attachment=True, mimetype='application/pdf')

@app.route('/download_treated_water_data')
def download_treated_water_data():
    campus = request.args.get("campus")
    month = request.args.get("month")

    # Fetch all data based on the filters
    data = fetch_all_treated_water_data(campus, month)

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create an Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Treated Water Data')

    output.seek(0)

    # Send the file to the client
    return send_file(output, download_name="treated_water_data.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/fetch_all_water_data')
def fetch_all_water_data():
    campus = request.args.get("campus")
    year = request.args.get("year")
    category = request.args.get("category")
    
    # Fetch all data without pagination limit
    data, _ = fetch_water_data(campus, year, category, page=None, per_page=None)
    
    return jsonify(data)


def fetch_water_data(campus=None, year=None, category=None, page=None, per_page=None):
    offset = (page - 1) * per_page if page and per_page else 0
    limit = per_page if per_page else 18446744073709551615  # Use a large number for no practical limit

    query = "SELECT * FROM tblwater"
    conditions = []
    params = []

    if campus:
        conditions.append("Campus = %s")
        params.append(campus)
    if year:
        conditions.append("YEAR(Date) = %s")
        params.append(year)
    if category:
        conditions.append("Category = %s")
        params.append(category)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                data = cursor.fetchall()
                # Only execute count query if pagination is needed
                if page:
                    count_query = "SELECT COUNT(*) AS total FROM tblwater"
                    if conditions:
                        count_query += " WHERE " + " AND ".join(conditions)
                    cursor.execute(count_query, params[:-2])  # remove limit and offset
                    total_records = cursor.fetchone()['total']
                    return data, total_records
                return data, None
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        raise  # Raising the error to make it visible as an HTTP 500 error

# Route for Water Consumption Report with filtering and pagination
@app.route('/report/water')
def water_report():
    # Pagination and filter settings
    per_page = 20
    current_page = request.args.get("page", 1, type=int)

    # Retrieve filter parameters
    campus = request.args.get("campus")
    year = request.args.get("year")
    category = request.args.get("category")

    # Fetch data with filters applied
    data, total_records = fetch_water_data(campus, year, category, page=current_page, per_page=per_page)
    
    # Calculate total pages for pagination
    total_pages = math.ceil(total_records / per_page)
    
    return render_template(
        "water_report.html",
        data=data,
        current_page=current_page,
        total_pages=total_pages,
        campus=campus,
        year=year,
        category=category
    )

@app.route('/download_water_data')
def download_water_data():
    campus = request.args.get("campus")
    year = request.args.get("year")
    category = request.args.get("category")

    # Fetch data using the existing function which should return data in a list of dicts
    data, _ = fetch_water_data(campus, year, category, page=None, per_page=None)

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create an Excel writer object and write the DataFrame
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Water Data')

    output.seek(0)

    # Send the file to the client
    return send_file(output, download_name="water_data.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/download_water_pdf')
def download_water_pdf():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)
    category = request.args.get("category", None)

    # Fetch all data based on the filters
    data, _ = fetch_water_data(page=None, per_page=None, campus=campus, year=year, category=category)

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Handle empty data case
    if df.empty:
        return "No data available to generate PDF", 404

    # Create a PDF file in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to list of lists
    data_list = [df.columns.tolist()] + df.values.tolist()  # Add headers and data rows

    # Create table and style
    table = Table(data_list)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the PDF with the table
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="water_consumption_report.pdf", as_attachment=True, mimetype='application/pdf')


# Helper function to fetch data from the database with pagination and filters
def fetch_waste_segregation_data(page=1, per_page=20, campus=None, year=None, quarter=None, main_category=None):
    # Start the base query with a condition that always matches
    base_query = "SELECT * FROM tblsolidwastesegregated WHERE 1=1"
    total_query = "SELECT COUNT(*) AS total FROM tblsolidwastesegregated WHERE 1=1"
    params = []

    # Apply campus filter if provided
    if campus:
        base_query += " AND campus = %s"
        total_query += " AND campus = %s"
        params.append(campus)

    # Apply year filter if provided
    if year:
        base_query += " AND year = %s"
        total_query += " AND year = %s"
        params.append(year)

    # Apply quarter filter if provided
    if quarter:
        base_query += " AND quarter = %s"
        total_query += " AND quarter = %s"
        params.append(quarter)

    # Apply main category filter if provided
    if main_category:
        base_query += " AND mainCategory = %s"
        total_query += " AND mainCategory = %s"
        params.append(main_category)

    # Only add pagination if both `page` and `per_page` are not None
    if page is not None and per_page is not None:
        offset = (page - 1) * per_page
        base_query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

    data = []
    total_records = 0

    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)

        # Fetch records with filters
        cursor.execute(base_query, params)
        data = cursor.fetchall()

        # Fetch total count of filtered records if pagination is applied
        if page is not None and per_page is not None:
            cursor.execute(total_query, params[:-2])  # Exclude pagination params for count query
            total_records = cursor.fetchone()["total"]
        else:
            # If no pagination, get total count without limit/offset
            cursor.execute(total_query, params)
            total_records = cursor.fetchone()["total"]

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    return data, total_records

@app.route('/report/waste_segregation')
def waste_segregation_report():
    per_page = 20  # Number of records per page
    current_page = request.args.get("page", 1, type=int)
    
    # Get filter values from request arguments and convert `year` to a string if it's not None
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)
    if year:
        year = str(year)  # Convert `year` to a string to avoid issues in the template
    quarter = request.args.get("quarter", None)
    main_category = request.args.get("main_category", None)

    # Fetch paginated and filtered data
    data, total_records = fetch_waste_segregation_data(
        page=current_page, 
        per_page=per_page, 
        campus=campus, 
        year=year, 
        quarter=quarter, 
        main_category=main_category
    )

    # Calculate total pages
    total_pages = math.ceil(total_records / per_page)

    return render_template(
    'waste_segregation_report.html',
    data=data,
    current_page=current_page,
    total_pages=total_pages,
    campus=campus,
    year=year,
    quarter=quarter,
    main_category=main_category,
    str=str  # Pass the `str` function explicitly to the template
)

@app.route('/download_waste_segregation_data')
def download_waste_segregation_data():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)
    quarter = request.args.get("quarter", None)
    main_category = request.args.get("main_category", None)

    # Fetch all data based on the filters
    data, _ = fetch_waste_segregation_data(page=None, per_page=None, campus=campus, year=year, quarter=quarter, main_category=main_category)

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create an Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Waste Segregation Data')

    output.seek(0)

    # Send the file to the client
    return send_file(output, download_name="waste_segregation_data.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/download_waste_segregation_pdf')
def download_waste_segregation_pdf():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)
    quarter = request.args.get("quarter", None)
    main_category = request.args.get("main_category", None)

    # Fetch all data based on the filters
    data, _ = fetch_waste_segregation_data(page=None, per_page=None, campus=campus, year=year, quarter=quarter, main_category=main_category)

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a PDF file in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to list of lists
    data_list = [df.columns.tolist()] + df.values.tolist()  # Add headers and data rows

    # Create table and style
    table = Table(data_list)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the PDF with the table
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="waste_segregation_report.pdf", as_attachment=True, mimetype='application/pdf')

def fetch_waste_unsegregation_data(page=1, per_page=20, campus=None, year=None, month=None):
    offset = (page - 1) * per_page
    base_query = "SELECT * FROM tblsolidwasteunsegregated WHERE 1=1"
    total_query = "SELECT COUNT(*) AS total FROM tblsolidwasteunsegregated WHERE 1=1"
    params = []

    # Apply campus filter if provided
    if campus:
        base_query += " AND Campus = %s"
        total_query += " AND Campus = %s"
        params.append(campus)

    # Apply year filter if provided
    if year:
        base_query += " AND Year = %s"
        total_query += " AND Year = %s"
        params.append(year)

    # Apply month filter if provided
    if month:
        base_query += " AND Month = %s"
        total_query += " AND Month = %s"
        params.append(month)

    # Add pagination limits
    base_query += " LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    data = []
    total_records = 0

    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        
        # Fetch records with applied filters and pagination
        cursor.execute(base_query, params)
        data = cursor.fetchall()

        # Fetch the total record count with the same filters
        cursor.execute(total_query, params[:-2])  # Exclude pagination params for count query
        total_records = cursor.fetchone()["total"]

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    return data, total_records


@app.route('/download_waste_unseg_pdf')
def download_waste_unseg_pdf():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)
    month = request.args.get("month", None)

    # Fetch all data based on the filters
    data, _ = fetch_waste_unsegregation_data(page=1, per_page=10000, campus=campus, year=year, month=month)

    # Handle empty data case
    if not data:
        return "No data available to generate PDF", 404

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a PDF file in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to list of lists
    data_list = [df.columns.tolist()] + df.values.tolist()  # Add headers and data rows

    # Calculate default column widths
    page_width = landscape(A4)[0] - 20  # 20 for margins
    num_columns = len(df.columns)
    col_widths = [page_width / num_columns] * num_columns

    # Check if "WasteType" column exists before setting its width
    if "WasteType" in df.columns:
        waste_type_index = df.columns.get_loc("WasteType")
        col_widths[waste_type_index] *= 1.5  # Increase width of WasteType column by 50%

    # Define table with adjusted column widths
    table = Table(data_list, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 6),  # Reduced font size for fitting more data
        ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ]))

    # Build the PDF with the table
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="waste_unsegregation_report.pdf", as_attachment=True, mimetype='application/pdf')

@app.route('/download_waste_unseg_excel')
def download_waste_unseg_excel():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)
    month = request.args.get("month", None)

    # Fetch data based on filters
    data, _ = fetch_waste_unsegregation_data(page=1, per_page=10000, campus=campus, year=year, month=month)

    # Handle empty data case
    if not data:
        return "No data available to generate Excel file", 404

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create an Excel file in memory
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Waste Unsegregation Report')
        workbook = writer.book
        worksheet = writer.sheets['Waste Unsegregation Report']
        
        # Optional: Adjust column width
        for i, col in enumerate(df.columns):
            column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_width)

    buffer.seek(0)

    # Send the Excel file as a downloadable file
    return send_file(buffer, download_name="waste_unsegregation_report.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/report/waste_unsegregation')
def waste_unseg_report():
    # Get filter values from request args with None as default
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)
    month = request.args.get("month", None)

    # Fetch paginated and filtered data
    data, total_records = fetch_waste_unsegregation_data(
        page=request.args.get("page", 1, type=int),
        per_page=20,
        campus=campus,
        year=year,
        month=month
    )

    # Pass all variables to the template
    return render_template(
        'waste_unseg_report.html',
        data=data,
        total_pages=(total_records + 19) // 20,  # Calculate total pages
        current_page=request.args.get("page", 1, type=int),
        campus=campus,
        year=year,
        month=month
    )

def fetch_food_data(page=1, per_page=20, campus=None, month=None, year=None, office=None):
    offset = (page - 1) * per_page
    base_query = "SELECT * FROM tblfoodwaste WHERE 1=1"  # Base query with always-true condition
    total_query = "SELECT COUNT(*) as count FROM tblfoodwaste WHERE 1=1"
    params = []

    # Apply filters if provided
    if campus:
        base_query += " AND Campus = %s"
        total_query += " AND Campus = %s"
        params.append(campus)

    if month:
        base_query += " AND Month = %s"
        total_query += " AND Month = %s"
        params.append(month)

    if year:
        base_query += " AND YearTransaction = %s"
        total_query += " AND YearTransaction = %s"
        params.append(year)

    if office:
        base_query += " AND Office = %s"
        total_query += " AND Office = %s"
        params.append(office)

    # Add pagination to the main query
    base_query += " LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    data = []
    total_records = 0

    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)

        # Execute main query with filters and pagination
        cursor.execute(base_query, params)
        data = cursor.fetchall()

        # Execute count query for total records with the same filters (without pagination params)
        cursor.execute(total_query, params[:-2])
        total_records = cursor.fetchone()['count']

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    return data, total_records

@app.route('/report/food_consumption')
def food_consumption_report():
    per_page = 20  # Items per page
    current_page = request.args.get("page", 1, type=int)

    # Get filters from URL parameters
    campus = request.args.get("campus")
    month = request.args.get("month")
    year = request.args.get("year")
    office = request.args.get("office")

    # Fetch data with pagination and filters
    data, total_records = fetch_food_data(
        page=current_page, 
        per_page=per_page, 
        campus=campus, 
        month=month, 
        year=year, 
        office=office
    )

    # Calculate total pages
    total_pages = math.ceil(total_records / per_page)

    return render_template(
        'food_consumption_report.html',
        data=data,
        current_page=current_page,
        total_pages=total_pages,
        campus=campus,
        month=month,
        year=year,
        office=office
    )

@app.route('/download_food_consumption_excel')
def download_food_consumption_excel():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    month = request.args.get("month", None)
    year = request.args.get("year", None)
    office = request.args.get("office", None)

    # Fetch data based on filters (with a large per_page to ensure we get all data)
    data, _ = fetch_food_data(page=1, per_page=10000, campus=campus, month=month, year=year, office=office)

    # Handle empty data case
    if not data:
        return "No data available to generate Excel file", 404

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create an Excel file in memory
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Food Consumption Report')
        workbook = writer.book
        worksheet = writer.sheets['Food Consumption Report']
        
        # Optional: Adjust column width
        for i, col in enumerate(df.columns):
            column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_width)

    buffer.seek(0)

    # Send the Excel file as a downloadable file
    return send_file(buffer, download_name="food_consumption_report.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@app.route('/download_food_consumption_pdf')
def download_food_consumption_pdf():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    month = request.args.get("month", None)
    year = request.args.get("year", None)
    office = request.args.get("office", None)

    # Fetch all data based on the filters (setting a high per_page value to retrieve all data at once)
    data, _ = fetch_food_data(page=1, per_page=10000, campus=campus, month=month, year=year, office=office)
    
    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Handle empty data case
    if df.empty:
        return "No data available to generate PDF", 404

    # Create a PDF file in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to list of lists for table structure
    data_list = [df.columns.tolist()] + df.values.tolist()  # Add headers and data rows

    # Calculate column width to fit all columns within the page width
    page_width = landscape(A4)[0] - 20  # 20 for total left and right margins
    num_columns = len(df.columns)
    col_width = page_width / num_columns

    # Define table with dynamic column widths
    table = Table(data_list, colWidths=[col_width] * num_columns)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Reduced font size for fitting more data
        ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ]))

    # Build the PDF with the table
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="food_consumption_report.pdf", as_attachment=True, mimetype='application/pdf')

# Helper function to fetch data from the database with pagination and filters
def fetch_lpg_data(page=1, per_page=20, campus=None, year=None, month=None, office=None):
    offset = (page - 1) * per_page
    query = "SELECT * FROM tbllpg WHERE 1=1"  # Base query
    count_query = "SELECT COUNT(*) as count FROM tbllpg WHERE 1=1"  # For counting total records
    params = []

    # Apply filters if provided
    if campus:
        query += " AND Campus = %s"
        count_query += " AND Campus = %s"
        params.append(campus)
    
    if year:
        query += " AND YearTransact = %s"
        count_query += " AND YearTransact = %s"
        params.append(year)
    
    if month:
        query += " AND Month = %s"
        count_query += " AND Month = %s"
        params.append(month)
    
    if office:
        query += " AND Office = %s"
        count_query += " AND Office = %s"
        params.append(office)

    # Add pagination to query
    query += " LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    data = []
    total_records = 0
    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        
        # Execute query for current page data
        cursor.execute(query, params)
        data = cursor.fetchall()
        
        # Execute count query to get total records
        cursor.execute(count_query, params[:-2])  # Exclude pagination params for count query
        total_records = cursor.fetchone()['count']
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()
    
    return data, total_records

# Route for LPG Consumption Report
@app.route('/report/lpg_consumption')
def lpg_consumption_report():
    per_page = 20  # Items per page
    current_page = request.args.get("page", 1, type=int)

    # Get filter values from request args
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)
    month = request.args.get("month", None)
    office = request.args.get("office", None)

    # Fetch filtered and paginated data
    data, total_records = fetch_lpg_data(page=current_page, per_page=per_page, campus=campus, year=year, month=month, office=office)

    # Calculate total pages
    total_pages = math.ceil(total_records / per_page)

    return render_template(
        'lpg_consumption_report.html',
        data=data,
        current_page=current_page,
        total_pages=total_pages,
        campus=campus,
        year=year,
        month=month,
        office=office
    )

@app.route('/download_lpg_consumption_pdf')
def download_lpg_consumption_pdf():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)
    month = request.args.get("month", None)
    office = request.args.get("office", None)

    # Fetch all data based on the filters (using a high per_page value to retrieve all data at once)
    data, _ = fetch_lpg_data(page=1, per_page=10000, campus=campus, year=year, month=month, office=office)
    
    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Handle empty data case
    if df.empty:
        return "No data available to generate PDF", 404

    # Create a PDF file in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to list of lists for table structure
    data_list = [df.columns.tolist()] + df.values.tolist()  # Add headers and data rows

    # Calculate column width to fit all columns within the page width
    page_width = landscape(A4)[0] - 20  # 20 for total left and right margins
    num_columns = len(df.columns)
    col_width = page_width / num_columns

    # Define table with dynamic column widths
    table = Table(data_list, colWidths=[col_width] * num_columns)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Reduced font size for fitting more data
        ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ]))

    # Build the PDF with the table
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="lpg_consumption_report.pdf", as_attachment=True, mimetype='application/pdf')
@app.route('/download_lpg_consumption_excel')
def download_lpg_consumption_excel():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)
    month = request.args.get("month", None)
    office = request.args.get("office", None)

    # Fetch data based on filters (set a high `per_page` value to retrieve all data)
    data, _ = fetch_lpg_data(page=1, per_page=10000, campus=campus, year=year, month=month, office=office)

    # Handle empty data case
    if not data:
        return "No data available to generate Excel file", 404

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create an Excel file in memory
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='LPG Consumption Report')
        workbook = writer.book
        worksheet = writer.sheets['LPG Consumption Report']

        # Optional: Adjust column width
        for i, col in enumerate(df.columns):
            column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_width)

    buffer.seek(0)

    # Send the Excel file as a downloadable file
    return send_file(buffer, download_name="lpg_consumption_report.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# Helper function to fetch data with pagination and filters
def fetch_flight_data(page=1, per_page=20, campus=None, office=None, year=None):
    offset = (page - 1) * per_page
    query = "SELECT * FROM tblflight WHERE 1=1"  # Base query
    count_query = "SELECT COUNT(*) as count FROM tblflight WHERE 1=1"  # For counting total records
    params = []

    # Apply filters if provided
    if campus:
        query += " AND Campus = %s"
        count_query += " AND Campus = %s"
        params.append(campus)
    
    if office:
        query += " AND Office = %s"
        count_query += " AND Office = %s"
        params.append(office)
    
    if year:
        query += " AND Year = %s"
        count_query += " AND Year = %s"
        params.append(year)

    # Add pagination to query
    query += " LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    data = []
    total_records = 0
    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        
        # Execute query for current page data
        cursor.execute(query, params)
        data = cursor.fetchall()
        
        # Execute count query to get total records
        cursor.execute(count_query, params[:-2])  # Exclude pagination params for count query
        total_records = cursor.fetchone()['count']
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()
    
    return data, total_records

# Route for Flight Emissions Report
@app.route('/report/flight_emissions')
def flight_emissions_report():
    per_page = 20  # Items per page
    current_page = request.args.get("page", 1, type=int)

    # Get filter values from request args
    campus = request.args.get("campus", None)
    office = request.args.get("office", None)
    year = request.args.get("year", None)

    # Fetch filtered and paginated data
    data, total_records = fetch_flight_data(page=current_page, per_page=per_page, campus=campus, office=office, year=year)

    # Calculate total pages
    total_pages = math.ceil(total_records / per_page)

    return render_template(
        'flight_emissions_report.html',
        data=data,
        current_page=current_page,
        total_pages=total_pages,
        campus=campus,
        office=office,
        year=year
    )

@app.route('/download_flight_emissions_pdf')
def download_flight_emissions_pdf():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    office = request.args.get("office", None)
    year = request.args.get("year", None)

    # Fetch all data based on the filters
    data, _ = fetch_flight_data(page=1, per_page=10000, campus=campus, office=office, year=year)

    # Handle empty data case
    if not data:
        return "No data available to generate PDF", 404

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a PDF file in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to list of lists for table structure
    data_list = [df.columns.tolist()] + df.values.tolist()  # Add headers and data rows

    # Calculate column width to fit all columns within the page width
    page_width = landscape(A4)[0] - 20  # 20 for total left and right margins
    num_columns = len(df.columns)
    col_width = page_width / num_columns

    # Define table with dynamic column widths
    table = Table(data_list, colWidths=[col_width] * num_columns)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Reduced font size for fitting more data
        ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ]))

    # Build the PDF with the table
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="flight_emissions_report.pdf", as_attachment=True, mimetype='application/pdf')

@app.route('/download_flight_emissions_excel')
def download_flight_emissions_excel():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    office = request.args.get("office", None)
    year = request.args.get("year", None)

    # Fetch data based on filters (set a high `per_page` value to retrieve all data)
    data, _ = fetch_flight_data(page=1, per_page=10000, campus=campus, office=office, year=year)

    # Handle empty data case
    if not data:
        return "No data available to generate Excel file", 404

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create an Excel file in memory
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Flight Emissions Report')
        workbook = writer.book
        worksheet = writer.sheets['Flight Emissions Report']

        # Optional: Adjust column width
        for i, col in enumerate(df.columns):
            column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_width)

    buffer.seek(0)

    # Send the Excel file as a downloadable file
    return send_file(buffer, download_name="flight_emissions_report.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# Updated helper function to fetch data with filters
def fetch_accommodation_data(page=1, per_page=20, campus=None, office=None, year=None):
    offset = (page - 1) * per_page
    base_query = "SELECT * FROM tblaccommodation WHERE 1=1"
    total_query = "SELECT COUNT(*) as count FROM tblaccommodation WHERE 1=1"
    params = []

    # Apply filters if provided
    if campus:
        base_query += " AND Campus = %s"
        total_query += " AND Campus = %s"
        params.append(campus)
    if office:
        base_query += " AND Office = %s"
        total_query += " AND Office = %s"
        params.append(office)
    if year:
        base_query += " AND YearTransact = %s"
        total_query += " AND YearTransact = %s"
        params.append(year)

    # Add pagination to the query
    base_query += " LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    data = []
    total_records = 0

    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        
        # Execute the main query with filters
        cursor.execute(base_query, params)
        data = cursor.fetchall()
        
        # Execute the total count query
        cursor.execute(total_query, params[:len(params) - 2])  # Exclude pagination params for count
        total_records = cursor.fetchone()['count']
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    return data, total_records

# Update route to handle filters
@app.route('/report/accommodation_emissions')
def accommodation_emissions_report():
    per_page = 20  # Number of records per page
    current_page = request.args.get("page", 1, type=int)

    # Get filter values from query parameters
    campus = request.args.get("campus", None)
    office = request.args.get("office", None)
    year = request.args.get("year", None)

    # Fetch paginated and filtered data
    data, total_records = fetch_accommodation_data(page=current_page, per_page=per_page, campus=campus, office=office, year=year)

    # Calculate total pages based on filtered results
    total_pages = math.ceil(total_records / per_page)

    return render_template(
        'accommodation_emissions_report.html',
        data=data,
        current_page=current_page,
        total_pages=total_pages,
        campus=campus,
        office=office,
        year=year
    )

@app.route('/download_accommodation_emissions_pdf')
def download_accommodation_emissions_pdf():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    office = request.args.get("office", None)
    year = request.args.get("year", None)

    # Fetch all data based on the filters (using a high per_page value to retrieve all data at once)
    data, _ = fetch_accommodation_data(page=1, per_page=10000, campus=campus, office=office, year=year)

    # Handle empty data case
    if not data:
        return "No data available to generate PDF", 404

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a PDF file in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to list of lists for table structure
    data_list = [df.columns.tolist()] + df.values.tolist()  # Add headers and data rows

    # Calculate column width to fit all columns within the page width
    page_width = landscape(A4)[0] - 20  # 20 for total left and right margins
    num_columns = len(df.columns)
    col_width = page_width / num_columns

    # Define table with dynamic column widths
    table = Table(data_list, colWidths=[col_width] * num_columns)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Reduced font size for fitting more data
        ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ]))

    # Build the PDF with the table
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="accommodation_emissions_report.pdf", as_attachment=True, mimetype='application/pdf')


@app.route('/download_accommodation_emissions_excel')
def download_accommodation_emissions_excel():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    office = request.args.get("office", None)
    year = request.args.get("year", None)

    # Fetch data based on filters (set a high `per_page` value to retrieve all data)
    data, _ = fetch_accommodation_data(page=1, per_page=10000, campus=campus, office=office, year=year)

    # Handle empty data case
    if not data:
        return "No data available to generate Excel file", 404

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create an Excel file in memory
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Accommodation Emissions Report')
        workbook = writer.book
        worksheet = writer.sheets['Accommodation Emissions Report']

        # Optional: Adjust column width
        for i, col in enumerate(df.columns):
            column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_width)

    buffer.seek(0)

    # Send the Excel file as a downloadable file
    return send_file(buffer, download_name="accommodation_emissions_report.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


# Route for the Center for Sustainable Development Report
@app.route('/csd_report', methods=['GET'])
def csd_report():
    # Retrieve the selected campus and office from the request arguments
    campus = request.args.get('campus', 'All Campuses')
    selected_office = request.args.get('office', 'all_offices')

    reports = {}

    # Define the database table queries
    tables = {
        'electricity': "SELECT * FROM electricity_consumption",
        'water': "SELECT * FROM tblwater",
        'waste_unsegregation': "SELECT * FROM tblsolidwasteunsegregated",
        'waste_segregation': "SELECT * FROM tblsolidwastesegregated",
        'treated_water': "SELECT * FROM tbltreatedwater",
        'lpg_data': "SELECT * FROM tbllpg",
        'fuel_emissions': "SELECT * FROM fuel_emissions",
        'food_data': "SELECT * FROM tblfoodwaste",
        'accommodation_data': "SELECT * FROM tblaccommodation",
        'flight_data': "SELECT * FROM tblflight"
    }

    # Mapping of offices to the tables they should display
    office_tables = {
        'all_offices': tables.keys(),  # Show all tables if "All Offices" is selected
        'environmental_management_unit': [
            'electricity', 'fuel_emissions', 'water',
            'treated_water', 'waste_segregation', 'waste_unsegregation'
        ],
        'procurement_office': ['food_data', 'lpg_data'],
        'external_affair': ['flight_data', 'accommodation_data']
    }

    # Determine which tables to query based on the selected office
    tables_to_query = office_tables.get(selected_office, tables.keys())

    try:
        # Establish database connection
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)

        # Loop through each relevant table, applying campus filtering if needed
        for key in tables_to_query:
            # Build query with optional campus filtering
            base_query = tables[key]
            if campus and campus != "All Campuses":
                # Apply campus filter if a specific campus is selected
                query = f"{base_query} WHERE campus = %s"
                cursor.execute(query, (campus,))
            else:
                # No campus filter, retrieve all data
                query = base_query
                cursor.execute(query)

            # Fetch all data for each table
            data = cursor.fetchall()
            reports[key] = data

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        return "An error occurred while fetching the data."

    finally:
        # Close cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    # Render the report page with the filtered reports data
    return render_template(
        'csd_report.html',
        reports=reports,
        selected_campus=campus,
        selected_office=selected_office
    )

    
@app.route('/export_data', methods=['POST'])
def export_data():
    try:
        # Get the selected consumption type from the form
        consumption_type = request.form.get('consumption_type', 'all')

        # Define queries for each table to fetch all data
        tables_to_export = {
            'electricity': "SELECT * FROM electricity_consumption",
            'water': "SELECT * FROM tblwater",
            'treated_water': "SELECT * FROM tbltreatedwater",
            'waste_unsegregation': "SELECT * FROM tblsolidwasteunsegregated",
            'waste_segregation': "SELECT * FROM tblsolidwastesegregated",
            'fuel_emissions': "SELECT * FROM fuel_emissions",
            'food_data': "SELECT * FROM tblfoodwaste",
            'lpg_data': "SELECT * FROM tbllpg",
            'flight_data': "SELECT * FROM tblflight",
            'accommodation_data': "SELECT * FROM tblaccommodation"
        }

        # Ensure the requested report type is valid
        if consumption_type not in tables_to_export and consumption_type != 'all':
            return jsonify({'error': 'Invalid report type selected'}), 400

        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)

        # Fetch data for the selected consumption type or all if 'all' is selected
        all_data = {}
        for key, query in tables_to_export.items():
            if consumption_type == 'all' or consumption_type == key:
                cursor.execute(query)
                records = cursor.fetchall()
                if records:
                    df = pd.DataFrame(records)
                    if 'id' in df.columns:
                        df = df.drop(columns=['id'])  # Drop 'id' column if it exists
                    all_data[key] = df

        cursor.close()
        db_connection.close()

        # Render all data to the client without pagination logic
        return render_template('csd_report.html', reports=all_data, report_type=consumption_type)

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        return "An error occurred while fetching the data."
    except Exception as e:
        print("An error occurred during export:")
        traceback.print_exc()
        return "An error occurred during data export."


    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        return "An error occurred while fetching the data.", 500
    except Exception as e:
        print("An error occurred during export:")
        traceback.print_exc()
        return "An error occurred during data export.", 500


from flask import render_template, request, session, redirect, url_for, flash
from datetime import datetime
import mysql.connector
import pandas as pd
from prophet import Prophet

from sklearn.metrics import r2_score

@app.route('/sdo_dashboard', methods=['GET', 'POST'])
def sdo_dashboard():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    campus = session.get('campus', 'default_campus')
    selected_year = int(request.args.get('year', datetime.now().year))
    selected_month = request.args.get('month', None)
    current_year = datetime.now().year

    # Initialize data lists for emissions
    electricity_data = [0] * 12
    fuel_data = [0] * 12
    waste_segregated_data = [0] * 12
    waste_unsegregated_data = [0] * 12
    water_data = [0] * 12
    treated_water_data = [0] * 12
    food_waste_data = [0] * 12
    lpg_data = [0] * 12
    flight_data = [0] * 5  # For years 2020 to 2024
    accommodation_data = [0] * 5  # For years 2020 to 2024

    current_emission_data = {
        "electricity": 0,
        "fuel": 0,
        "waste_segregated": 0,
        "waste_unsegregated": 0,
        "water": 0,
        "treated_water": 0,
        "food_waste": 0,
        "lpg": 0,
        "flight": 0,
        "accommodation": 0,
    }

    month_to_index = {
        "January": 0, "February": 1, "March": 2, "April": 3, "May": 4, "June": 5,
        "July": 6, "August": 7, "September": 8, "October": 9, "November": 10, "December": 11
    }
    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Could not establish database connection.")

        cursor = conn.cursor(dictionary=True)

        # Queries for other data
        queries = [
            ("SELECT month, kg_co2_per_kwh FROM electricity_consumption WHERE campus = %s AND year = %s ORDER BY month ASC", electricity_data, "electricity"),
            ("SELECT MONTHNAME(date) AS month, total_emission FROM fuel_emissions WHERE campus = %s AND YEAR(date) = %s ORDER BY MONTH(date) ASC", fuel_data, "fuel"),
            ("SELECT Month, SUM(GHGEmissionKGCO2e) AS total_emission FROM tblsolidwastesegregated WHERE Campus = %s AND Year = %s GROUP BY Month ORDER BY FIELD(Month, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')", waste_segregated_data, "waste_segregated"),
            ("SELECT Month, GHGEmissionKGCO2e FROM tblsolidwasteunsegregated WHERE Campus = %s AND Year = %s ORDER BY FIELD(Month, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')", waste_unsegregated_data, "waste_unsegregated"),
            ("SELECT MONTHNAME(Date) AS month, SUM(FactorKGCO2e) AS total_emission FROM tblwater WHERE Campus = %s AND YEAR(Date) = %s GROUP BY MONTHNAME(Date) ORDER BY FIELD(MONTHNAME(Date), 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')", water_data, "water"),
        ]

        for query, data_list, category in queries:
            cursor.execute(query, (campus, selected_year))
            for row in cursor.fetchall():
                month_index = month_to_index.get(row.get('month') or row.get('Month'), -1)
                if month_index != -1:
                    emission_value = row.get('total_emission') or row.get('kg_co2_per_kwh') or row.get('GHGEmissionKGCO2e')
                    if emission_value is not None:
                        data_list[month_index] = float(emission_value)
                        current_emission_data[category] += float(emission_value)

        # Treated Water Data
        treated_water_query = """
            SELECT Month, SUM(FactorKGCO2e) AS total_emission
            FROM tbltreatedwater
            WHERE Campus = %s AND YEAR(CURDATE()) = %s
        """
        params = [campus, selected_year]
        if selected_month:
            treated_water_query += " AND Month = %s"
            params.append(selected_month)

        treated_water_query += """
            GROUP BY Month
            ORDER BY FIELD(Month, 'January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December')
        """

        cursor.execute(treated_water_query, params)
        for row in cursor.fetchall():
            month_index = month_to_index.get(row.get('Month'), -1)
            if month_index != -1:
                treated_value = row.get('total_emission')
                if treated_value is not None:
                    treated_water_data[month_index] = float(treated_value)
                    current_emission_data["treated_water"] += float(treated_value)

        # Food Waste Data
        food_waste_query = """
            SELECT Month, GHGEmissionKGCO2e
            FROM tblfoodwaste
            WHERE Campus = %s AND YearTransaction = %s
            ORDER BY FIELD(Month, 'January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December')
        """
        cursor.execute(food_waste_query, (campus, selected_year))
        for row in cursor.fetchall():
            month_index = month_to_index.get(row.get('Month'), -1)
            if month_index != -1:
                emission_value = row.get('GHGEmissionKGCO2e')
                if emission_value is not None:
                    food_waste_data[month_index] = float(emission_value)
                    current_emission_data["food_waste"] += float(emission_value)

        # LPG Data
        lpg_query = """
            SELECT Month, GHGEmissionKGCO2e
            FROM tbllpg
            WHERE Campus = %s AND YearTransact = %s
            ORDER BY FIELD(Month, 'January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December')
        """
        cursor.execute(lpg_query, (campus, selected_year))
        for row in cursor.fetchall():
            month_index = month_to_index.get(row.get('Month'), -1)
            if month_index != -1:
                emission_value = row.get('GHGEmissionKGCO2e')
                if emission_value is not None:
                    lpg_data[month_index] = float(emission_value)
                    current_emission_data["lpg"] += float(emission_value)

        # Flight Data
        flight_query = """
            SELECT Year, SUM(GHGEmissionKGC02e) AS total_emission
            FROM tblflight
            WHERE Campus = %s AND Year BETWEEN 2020 AND 2024
            GROUP BY Year
            ORDER BY Year
        """
        cursor.execute(flight_query, (campus,))
        for row in cursor.fetchall():
            year_index = row['Year'] - 2020
            if 0 <= year_index < len(flight_data):
                flight_data[year_index] = float(row['total_emission'])
                current_emission_data["flight"] += float(row['total_emission'])

        # Accommodation Data Query
        accommodation_query = """
            SELECT YearTransact AS Year, SUM(GHGEmissionKGC02e) AS total_emission
            FROM tblaccommodation
            WHERE Campus = %s AND YearTransact BETWEEN 2020 AND 2024
            GROUP BY YearTransact
            ORDER BY YearTransact
        """
        cursor.execute(accommodation_query, (campus,))
        rows = cursor.fetchall()

        # Debugging: Print the fetched rows
        if not rows:
            print("No data fetched for tblaccommodation")
        else:
            print("Accommodation Query Results:", rows)

        for row in rows:
            year_index = row['Year'] - 2020
            if 0 <= year_index < len(accommodation_data):
                accommodation_data[year_index] = float(row['total_emission'])


    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Forecast function using Prophet
    def forecast_prophet(data, periods):
        if all(v == 0 for v in data):
            return [0] * periods, 0

        try:
            df = pd.DataFrame({'ds': pd.date_range(start='2023-01-01', periods=len(data), freq='M'), 'y': data})
            df = df[df['y'] > 0]
            model = Prophet(yearly_seasonality=True)
            model.fit(df)
            future = model.make_future_dataframe(periods=periods, freq='M')
            forecast = model.predict(future)
            return forecast['yhat'][-periods:].tolist(), r2_score(df['y'], model.predict(df)['yhat'])
        except Exception as e:
            flash(f"Forecast Error: {e}", "danger")
            return [0] * periods, 0

    # Forecast data with R² scores using Prophet
    forecast_data = {
        "electricity_forecast": {
            "prophet": {
                "forecast": forecast_prophet(electricity_data, periods=12)[0],
                "r2_score": forecast_prophet(electricity_data, periods=12)[1],
            }
        },
        "fuel_forecast": {
            "prophet": {
                "forecast": forecast_prophet(fuel_data, periods=12)[0],
                "r2_score": forecast_prophet(fuel_data, periods=12)[1],
            }
        },
        "waste_segregated_forecast": {
            "prophet": {
                "forecast": forecast_prophet(waste_segregated_data, periods=12)[0],
                "r2_score": forecast_prophet(waste_segregated_data, periods=12)[1],
            }
        },
        "waste_unsegregated_forecast": {
            "prophet": {
                "forecast": forecast_prophet(waste_unsegregated_data, periods=12)[0],
                "r2_score": forecast_prophet(waste_unsegregated_data, periods=12)[1],
            }
        },
        "water_forecast": {
            "prophet": {
                "forecast": forecast_prophet(water_data, periods=12)[0],
                "r2_score": forecast_prophet(water_data, periods=12)[1],
            }
        },
        "treated_water_forecast": {
            "prophet": {
                "forecast": forecast_prophet(treated_water_data, periods=12)[0],
                "r2_score": forecast_prophet(treated_water_data, periods=12)[1],
            }
        },
        "food_waste_forecast": {
            "prophet": {
                "forecast": forecast_prophet(food_waste_data, periods=12)[0],
                "r2_score": forecast_prophet(food_waste_data, periods=12)[1],
            }
        },
        "lpg_forecast": {
            "prophet": {
                "forecast": forecast_prophet(lpg_data, periods=12)[0],
                "r2_score": forecast_prophet(lpg_data, periods=12)[1],
            }
        },
        "flight_forecast": {
            "prophet": {
                "forecast": forecast_prophet(flight_data, periods=5)[0],
                "r2_score": forecast_prophet(flight_data, periods=5)[1],
            }
        },
        "accommodation_forecast": {
            "prophet": {
                "forecast": forecast_prophet(accommodation_data, periods=5)[0],
                "r2_score": forecast_prophet(accommodation_data, periods=5)[1],
            }
        },

    }

    # Print R² scores for validation
    for key, value in forecast_data.items():
        print(f"{key.replace('_forecast', '').title()} Prophet R² Score:", value["prophet"]["r2_score"])

    # Month labels
    def get_month_labels(start_month, start_year, total_months):
        return [f"{(start_month + i) % 12 + 1:02d}/{(start_year + (start_month + i) // 12) % 100:02d}" for i in range(total_months)]

    month_labels = [f"{i:02d}" for i in range(1, 13)]
    labels = get_month_labels(0, selected_year, 12)

    # Render the template with forecast data
    return render_template(
        'sdo_dashboard.html',
        electricity_data=electricity_data,
        fuel_data=fuel_data,
        waste_segregated_data=waste_segregated_data,
        waste_unsegregated_data=waste_unsegregated_data,
        water_data=water_data,
        treated_water_data=treated_water_data,
        food_waste_data=food_waste_data,
        lpg_data=lpg_data,
        flight_data=flight_data,
        accommodation_data=accommodation_data,
        forecast_data=forecast_data,
        current_emission_data=current_emission_data,
        selected_year=selected_year,
        current_year=current_year,
        labels=labels,
        month_labels=month_labels
    )

@app.route('/sdo_electricity_report', methods=['GET'])
def sdo_electricity_report():
    # Ensure that the user is logged in and has a valid session
    if 'campus' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    user_campus = session['campus']  # Get the campus from the session
    
    # Get filter parameters from the request
    campus_filter = request.args.get('campus', '')
    category_filter = request.args.get('category', '')
    month_filter = request.args.get('month', '')
    quarter_filter = request.args.get('quarter', '')
    year_filter = request.args.get('year', '')
    
    # Pagination setup
    per_page = 20  # Records per page
    current_page = request.args.get('page', 1, type=int)

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to fetch rows as dicts

    # Base query
    query = """
        SELECT campus, category, month, quarter, year, prev_reading, current_reading, multiplier, 
               total_amount, consumption, price_per_kwh, kg_co2_per_kwh, t_co2_per_kwh
        FROM electricity_consumption
        WHERE 1=1  -- This allows easy appending of additional filters
    """
    
    # Initialize filter parameters for cursor execution
    params = []

    # Add filters to query if they are provided
    if campus_filter:
        query += " AND campus = %s"
        params.append(campus_filter)
    if category_filter:
        query += " AND category = %s"
        params.append(category_filter)
    if month_filter:
        query += " AND month = %s"
        params.append(month_filter)
    if quarter_filter:
        query += " AND quarter = %s"
        params.append(quarter_filter)
    if year_filter:
        query += " AND year = %s"
        params.append(year_filter)

    # Count query for total records (to calculate pages), using the same filters
    count_query = """
        SELECT COUNT(*) as total 
        FROM electricity_consumption
        WHERE 1=1
    """
    
    # Add the same filters to the count query
    count_params = []
    if campus_filter:
        count_query += " AND campus = %s"
        count_params.append(campus_filter)
    if category_filter:
        count_query += " AND category = %s"
        count_params.append(category_filter)
    if month_filter:
        count_query += " AND month = %s"
        count_params.append(month_filter)
    if quarter_filter:
        count_query += " AND quarter = %s"
        count_params.append(quarter_filter)
    if year_filter:
        count_query += " AND year = %s"
        count_params.append(year_filter)

    # Execute the count query
    cursor.execute(count_query, tuple(count_params))
    total_records = cursor.fetchone()['total']
    
    # Calculate offset for pagination
    offset = (current_page - 1) * per_page
    
    # Add LIMIT and OFFSET to the main query for pagination
    query += " LIMIT %s OFFSET %s"
    params.append(per_page)
    params.append(offset)
    
    # Execute the main query
    cursor.execute(query, tuple(params))
    electricity_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Calculate total pages
    total_pages = (total_records + per_page - 1) // per_page

    # Render the template with data
    return render_template(
        'sdo_electricity_report.html',
        electricity_data=electricity_data,
        current_page=current_page,
        total_pages=total_pages,
        campus=campus_filter,
        category=category_filter,
        month=month_filter,
        quarter=quarter_filter,
        year=year_filter
    )

@app.route('/export_electricity_report_pdf')
def export_electricity_report_pdf():
    campus = request.args.get("campus", None)
    category = request.args.get("category", None)
    month = request.args.get("month", None)
    quarter = request.args.get("quarter", None)
    year = request.args.get("year", None)

    # Base query with WHERE 1=1 for easy appending of filters
    query = "SELECT * FROM electricity_consumption WHERE 1=1"
    params = []

    # Add filters dynamically to the query
    if campus:
        query += " AND campus = %s"
        params.append(campus)
    if category:
        query += " AND category = %s"
        params.append(category)
    if month:
        query += " AND month = %s"
        params.append(month)
    if quarter:
        query += " AND quarter = %s"
        params.append(quarter)
    if year:
        query += " AND year = %s"
        params.append(year)

    # Execute the query
    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(query, params)
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    # If no data is returned, handle the empty case
    if not data:
        return "No data available to generate PDF", 404

    # Convert data to DataFrame for easier handling
    df = pd.DataFrame(data)
    
    # Calculate the column width for the PDF (based on the number of columns)
    page_width = landscape(A4)[0] - 20  # 20 for margins
    num_columns = len(df.columns)
    col_width = page_width / num_columns

    # Create a PDF buffer
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to a list of lists (header + data rows)
    data_list = [df.columns.tolist()] + df.values.tolist()

    # Define table style (including grid and background color)
    table = Table(data_list, colWidths=[col_width] * num_columns)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),  # Smaller font for more data
        ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ]))

    # Build the PDF with the data
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="sdo_electricity_report.pdf", as_attachment=True, mimetype='application/pdf')

@app.route('/export_electricity_report_excel')
def export_electricity_report_excel():
    campus = request.args.get("campus", None)
    category = request.args.get("category", None)
    month = request.args.get("month", None)
    quarter = request.args.get("quarter", None)
    year = request.args.get("year", None)

    # Base query with WHERE 1=1 for easy appending of filters
    query = "SELECT * FROM electricity_consumption WHERE 1=1"
    params = []

    # Add filters dynamically to the query
    if campus:
        query += " AND campus = %s"
        params.append(campus)
    if category:
        query += " AND category = %s"
        params.append(category)
    if month:
        query += " AND month = %s"
        params.append(month)
    if quarter:
        query += " AND quarter = %s"
        params.append(quarter)
    if year:
        query += " AND year = %s"
        params.append(year)

    # Execute the query to fetch the data
    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(query, params)
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    # If no data is returned, handle the empty case
    if not data:
        return "No data available to generate Excel", 404

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Convert DataFrame to Excel in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Electricity Consumption")
    output.seek(0)

    # Send the Excel file as a download
    return send_file(output, download_name="electricity_consumption_report.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/sdo_fuel_emissions_report')
def sdo_fuel_emissions_report():
    # Ensure that the user is logged in and has a valid session
    if 'campus' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    user_campus = session['campus']  # Get the campus from the session
    
    # Get the filter parameters from the query string (URL)
    campus_filter = request.args.get('campus', user_campus)  # Default to user's campus if no filter is provided
    year_filter = request.args.get('year', None)  # Optional filter for year
    
    # Pagination setup
    per_page = 20  # Records per page
    current_page = request.args.get('page', 1, type=int)

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to fetch rows as dicts

    # Base query for counting the records, applying the filters
    count_query = """
        SELECT COUNT(*) as total 
        FROM fuel_emissions
        WHERE 1=1
    """
    
    # Add the campus filter if it's not "All Campuses"
    if campus_filter != '':
        count_query += " AND campus = %s"

    # Add year filter to the query if provided
    if year_filter:
        count_query += " AND YEAR(date) = %s"

    # Execute the count query with the parameters
    if campus_filter != '' and year_filter:
        cursor.execute(count_query, (campus_filter, year_filter))
    elif campus_filter != '':
        cursor.execute(count_query, (campus_filter,))
    elif year_filter:
        cursor.execute(count_query, (year_filter,))
    else:
        cursor.execute(count_query)
    
    total_records = cursor.fetchone()['total']

    # Calculate offset for pagination
    offset = (current_page - 1) * per_page

    # Query to fetch paginated data, filtered by the selected campus and year
    query = """
        SELECT campus, date, driver, type, vehicle_equipment, plate_no, category, fuel_type, 
               quantity_liters, total_amount, co2_emission, nh4_emission, n2o_emission, 
               total_emission, total_emission_t
        FROM fuel_emissions
        WHERE 1=1
    """
    
    # Add campus filter if it's not "All Campuses"
    if campus_filter != '':
        query += " AND campus = %s"

    # Add year filter to the query if provided
    if year_filter:
        query += " AND YEAR(date) = %s"

    query += " ORDER BY date DESC LIMIT %s OFFSET %s"

    # Execute the query with the appropriate parameters
    if campus_filter != '' and year_filter:
        cursor.execute(query, (campus_filter, year_filter, per_page, offset))
    elif campus_filter != '':
        cursor.execute(query, (campus_filter, per_page, offset))
    elif year_filter:
        cursor.execute(query, (year_filter, per_page, offset))
    else:
        cursor.execute(query, (per_page, offset))

    fuel_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Calculate total pages for pagination
    total_pages = (total_records + per_page - 1) // per_page

    # Render the template with data, filters, and pagination
    return render_template(
        'sdo_fuel_emissions_report.html',
        data=fuel_data,
        current_page=current_page,
        total_pages=total_pages,
        campus_filter=campus_filter,
        year_filter=year_filter
    )

@app.route('/export_fuel_report_pdf')
def export_fuel_report_pdf():
    # Get filter parameters from the request (query parameters)
    campus = request.args.get("campus", None)
    category = request.args.get("category", None)
    month = request.args.get("month", None)
    quarter = request.args.get("quarter", None)
    year = request.args.get("year", None)

    # Debugging: Print the filter parameters to check if they are passed
    print("Filter Parameters:", campus, category, month, quarter, year)

    # Start building the query (with WHERE 1=1 to facilitate dynamic filtering)
    query = "SELECT * FROM fuel_emissions WHERE 1=1"
    params = []

    # Dynamically add filters to the query if they are provided
    if campus:
        query += " AND campus = %s"
        params.append(campus)
    if category:
        query += " AND category = %s"
        params.append(category)
    if month:
        query += " AND month = %s"
        params.append(month)
    if quarter:
        query += " AND quarter = %s"
        params.append(quarter)
    if year:
        query += " AND year = %s"
        params.append(year)

    # Debugging: Print the final query and parameters to check if the filters are being applied
    print("Final Query:", query)
    print("Parameters:", params)

    # Execute the query
    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(query, params)
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    # If no data is returned, handle the empty case
    if not data:
        print("No data returned from the query!")
        return "No data available to generate PDF", 404

    # Debugging: Print the fetched data
    print("Fetched Data:", data)

    # Convert data to DataFrame for easier handling
    df = pd.DataFrame(data)

    # Check if DataFrame is correctly populated
    print("DataFrame Data:")
    print(df.head())  # Display the first few rows of the DataFrame

    # Calculate the column width for the PDF (based on the number of columns)
    page_width = landscape(A4)[0] - 20  # 20 for margins
    num_columns = len(df.columns)
    col_width = page_width / num_columns

    # Create a PDF buffer
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to a list of lists (header + data rows)
    data_list = [df.columns.tolist()] + df.values.tolist()

    # Define table style (including grid and background color)
    table = Table(data_list, colWidths=[col_width] * num_columns)
    table.setStyle(TableStyle([ 
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),  # Smaller font for more data
        ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ]))

    # Build the PDF with the data
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="fuel_consumption_report.pdf", as_attachment=True, mimetype='application/pdf')

@app.route('/export_fuel_report_excel')
def export_fuel_report_excel():
    # Get filter parameters from the request (query parameters)
    campus = request.args.get("campus", None)
    category = request.args.get("category", None)
    month = request.args.get("month", None)
    quarter = request.args.get("quarter", None)
    year = request.args.get("year", None)

    # Start building the query (with WHERE 1=1 to facilitate dynamic filtering)
    query = "SELECT * FROM fuel_emissions WHERE 1=1"
    params = []

    # Dynamically add filters to the query if they are provided
    if campus:
        query += " AND campus = %s"
        params.append(campus)
    if category:
        query += " AND category = %s"
        params.append(category)
    if month:
        query += " AND month = %s"
        params.append(month)
    if quarter:
        query += " AND quarter = %s"
        params.append(quarter)
    if year:
        query += " AND YEAR(date_column) = %s"  # Use correct column name if it's a date field
        params.append(year)

    # Execute the query
    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(query, params)
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    # If no data is returned, handle the empty case
    if not data:
        return "No data available to generate Excel report", 404

    # Convert the data to a DataFrame for easier handling
    df = pd.DataFrame(data)

    # Create an in-memory Excel file (using BytesIO) and save the dataframe to it
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Write the DataFrame to the Excel file
        df.to_excel(writer, index=False, sheet_name='Fuel Emissions Report')
        
    # Seek to the beginning of the in-memory file
    output.seek(0)

    # Return the Excel file as a downloadable response
    return send_file(
        output,
        download_name="fuel_consumption_report.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.route('/sdo_water_report')
def sdo_water_report():
    # Ensure that the user is logged in and has a valid session
    if 'campus' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    user_campus = session['campus']  # Get the campus from the session
    
    # Get the filter parameters from the request (GET parameters)
    selected_campus = request.args.get('campus', None)
    selected_year = request.args.get('year', None)
    selected_category = request.args.get('category', None)
    
    # Pagination setup
    per_page = 20  # Records per page
    current_page = request.args.get('page', 1, type=int)

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to fetch rows as dicts

    # Building the WHERE clause dynamically based on filters
    query_conditions = ["Campus = %s"]
    query_params = [user_campus]  # Start with the user's campus as a mandatory filter
    
    if selected_campus:
        query_conditions.append("Campus = %s")
        query_params.append(selected_campus)
    
    if selected_year:
        query_conditions.append("YEAR(Date) = %s")
        query_params.append(selected_year)
    
    if selected_category:
        query_conditions.append("Category = %s")
        query_params.append(selected_category)

    # Query for total records (to calculate pages), with dynamic filters
    count_query = f"""
        SELECT COUNT(*) as total
        FROM tblwater
        WHERE {' AND '.join(query_conditions)}
    """
    cursor.execute(count_query, tuple(query_params))
    total_records = cursor.fetchone()['total']

    # Calculate offset for pagination
    offset = (current_page - 1) * per_page

    # Fetch paginated data, with dynamic filters
    query = f"""
        SELECT Campus, Date, Category, PreviousReading, CurrentReading, Consumption, TotalAmount, 
               PricePerLiter, FactorKGCO2e, FactorTCO2e
        FROM tblwater
        WHERE {' AND '.join(query_conditions)}
        ORDER BY Date DESC
        LIMIT %s OFFSET %s
    """
    query_params.extend([per_page, offset])  # Append pagination parameters
    cursor.execute(query, tuple(query_params))
    water_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Calculate total pages
    total_pages = (total_records + per_page - 1) // per_page

    # Render the template with the data
    return render_template(
        'sdo_water_report.html',
        data=water_data,
        current_page=current_page,
        total_pages=total_pages,
        selected_campus=selected_campus,
        selected_year=selected_year,
        selected_category=selected_category
    )

@app.route('/export_water_report_pdf')
def export_water_report_pdf():
    # Get filter parameters from request
    campus = request.args.get("campus", None)
    category = request.args.get("category", None)
    year = request.args.get("year", None)

    # Base query with WHERE 1=1 for easy appending of filters
    query = """
        SELECT Campus, Date, Category, PreviousReading, CurrentReading, Consumption, 
               TotalAmount, PricePerLiter, FactorKGCO2e, FactorTCO2e
        FROM tblwater
        WHERE 1=1
    """
    params = []

    # Add filters dynamically to the query
    if campus:
        query += " AND Campus = %s"
        params.append(campus)
    if category:
        query += " AND Category = %s"
        params.append(category)
    if year:
        query += " AND YEAR(Date) = %s"
        params.append(year)

    # Execute the query
    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(query, params)
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    # If no data is returned, handle the empty case
    if not data:
        return "No data available to generate PDF", 404

    # Convert data to DataFrame for easier handling
    df = pd.DataFrame(data)
    
    # Calculate the column width for the PDF (based on the number of columns)
    page_width = landscape(A4)[0] - 20  # 20 for margins
    num_columns = len(df.columns)
    col_width = page_width / num_columns

    # Create a PDF buffer
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to a list of lists (header + data rows)
    data_list = [df.columns.tolist()] + df.values.tolist()

    # Define table style (including grid and background color)
    table = Table(data_list, colWidths=[col_width] * num_columns)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),  # Smaller font for more data
        ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ]))

    # Build the PDF with the data
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="sdo_water_report.pdf", as_attachment=True, mimetype='application/pdf')

@app.route('/export_water_report_excel')
def export_water_report_excel():
    # Get filter parameters
    campus = request.args.get("campus", None)
    category = request.args.get("category", None)
    year = request.args.get("year", None)

    # Base query for the water report
    query = """
        SELECT Campus, Date, Category, PreviousReading, CurrentReading, Consumption, 
               TotalAmount, PricePerLiter, FactorKGCO2e, FactorTCO2e
        FROM tblwater
        WHERE 1=1
    """
    params = []

    # Add filters dynamically to the query
    if campus:
        query += " AND Campus = %s"
        params.append(campus)
    if category:
        query += " AND Category = %s"
        params.append(category)
    if year:
        query += " AND YEAR(Date) = %s"
        params.append(year)

    # Connect to the database and fetch the data
    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(query, params)
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    # If no data is found, handle the empty case
    if not data:
        return "No data available to export", 404

    # Convert the data into a DataFrame
    df = pd.DataFrame(data)

    # Create a BytesIO buffer to hold the Excel file
    output = BytesIO()

    # Write the DataFrame to the buffer in Excel format
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Water Report')

    # Move the buffer's position to the beginning
    output.seek(0)

    # Send the Excel file as a download
    return send_file(output, as_attachment=True, download_name="water_report.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/sdo_treated_water_report')
def sdo_treated_water_report():
    # Ensure that the user is logged in and has a valid session
    if 'campus' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    user_campus = session['campus']  # Get the campus from the session
    
    # Get the filter values from the request args
    campus_filter = request.args.get('campus', None)  # Default to None to fetch all campuses
    month_filter = request.args.get('month', None)   # Default to None to fetch all months
    
    # If "All Months" is selected, set month_filter to None
    if month_filter == "All Months":
        month_filter = None
    
    # Pagination setup
    per_page = 20  # Records per page
    current_page = request.args.get('page', 1, type=int)

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to fetch rows as dicts

    # Base query for counting records, with filters applied
    count_query = """
        SELECT COUNT(*) as total
        FROM tbltreatedwater
        WHERE 1=1
    """
    params = []

    # Apply campus filter only if it's not 'All Campuses'
    if campus_filter and campus_filter != "All Campuses":
        count_query += " AND Campus = %s"
        params.append(campus_filter)
    
    # Apply month filter if selected
    if month_filter:
        count_query += " AND Month = %s"
        params.append(month_filter)

    cursor.execute(count_query, params)
    total_records = cursor.fetchone()['total']

    # Calculate offset for pagination
    offset = (current_page - 1) * per_page

    # Base query for fetching paginated data, with filters applied
    query = """
        SELECT Campus, Month, TreatedWaterVolume, ReusedTreatedWaterVolume, EffluentVolume, 
               PricePerLiter, FactorKGCO2e, FactorTCO2e
        FROM tbltreatedwater
        WHERE 1=1
    """
    
    # Apply campus filter only if it's not 'All Campuses'
    if campus_filter and campus_filter != "All Campuses":
        query += " AND Campus = %s"
    
    # Apply month filter if selected (None means no filter)
    if month_filter:
        query += " AND Month = %s"
    
    query += " ORDER BY id ASC LIMIT %s OFFSET %s"
    params.append(per_page)
    params.append(offset)

    cursor.execute(query, params)
    treated_water_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Calculate total pages
    total_pages = (total_records + per_page - 1) // per_page

    # Render the template with data
    return render_template(
        'sdo_treated_water_report.html',
        data=treated_water_data,
        current_page=current_page,
        total_pages=total_pages,
        campus_filter=campus_filter,
        month_filter=month_filter
    )


@app.route('/generate_treated_water_pdf')
def generate_treated_water_pdf():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    month = request.args.get("month", None)

    # Fetch all data based on the filters
    data, _ = fetch_treated_water_data(page=None, per_page=None, campus=campus, month=month)

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Handle empty data case
    if df.empty:
        return "No data available to generate PDF", 404

    # Create a PDF file in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to list of lists
    data_list = [df.columns.tolist()] + df.values.tolist()  # Add headers and data rows

    # Create table and style
    table = Table(data_list)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the PDF with the table
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="treated_water_report.pdf", as_attachment=True, mimetype='application/pdf')

@app.route('/export_treated_water_report_excel')
def export_treated_water_report_excel():
    # Get filter parameters from the request
    campus = request.args.get("campus", None)
    month = request.args.get("month", None)

    # Base query for fetching treated water data
    query = """
        SELECT Campus, Month, TreatedWaterVolume, ReusedTreatedWaterVolume, EffluentVolume, 
               PricePerLiter, FactorKGCO2e, FactorTCO2e
        FROM tbltreatedwater
        WHERE 1=1
    """
    params = []

    # Add filters dynamically to the query
    if campus:
        query += " AND Campus = %s"
        params.append(campus)
    if month:
        query += " AND Month = %s"
        params.append(month)

    # Connect to the database and fetch the data
    try:
        db_connection = mysql.connector.connect(**db_config)  # Assuming `db_config` contains your DB credentials
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(query, params)
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    # If no data is found, handle the empty case
    if not data:
        return "No data available to export", 404

    # Convert the data into a DataFrame
    df = pd.DataFrame(data)

    # Create a BytesIO buffer to hold the Excel file
    output = BytesIO()

    # Write the DataFrame to the buffer in Excel format using XlsxWriter engine
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Treated Water Report')

        # Access the worksheet
        worksheet = writer.sheets['Treated Water Report']

        # Set column widths to make it readable
        worksheet.set_column('A:A', 20)  # Campus
        worksheet.set_column('B:B', 15)  # Month
        worksheet.set_column('C:C', 25)  # Treated Water Volume
        worksheet.set_column('D:D', 30)  # Reused Treated Water Volume
        worksheet.set_column('E:E', 20)  # Effluent Volume
        worksheet.set_column('F:F', 15)  # Price Per Liter
        worksheet.set_column('G:G', 20)  # Factor KGCO2e
        worksheet.set_column('H:H', 20)  # Factor TCO2e

        # Add a bold header format
        header_format = writer.book.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#D9EAD3',
            'border': 1
        })

        # Apply the header format to the first row (header row)
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

    # Move the buffer's position to the beginning before sending it
    output.seek(0)

    # Send the Excel file as a downloadable response
    return send_file(output, as_attachment=True, download_name="treated_water_report.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@app.route('/sdo_waste_segregation_report')
def sdo_waste_segregation_report():
    # Ensure that the user is logged in and has a valid session
    if 'campus' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    user_campus = session['campus']  # Get the campus from the session

    # Get filter parameters from the request arguments
    campus_filter = request.args.get("campus", 'All')  # Default to 'All' if not provided
    year_filter = request.args.get("year", None)
    quarter_filter = request.args.get("quarter", None)
    main_category_filter = request.args.get("main_category", None)
    
    # Pagination setup
    per_page = 20  # Records per page
    current_page = request.args.get('page', 1, type=int)

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Fetch rows as dictionaries

    # Base query for counting records with filters applied
    count_query = """
        SELECT COUNT(*) as total
        FROM tblsolidwastesegregated
        WHERE (%s = 'All' OR Campus = %s)
    """
    params = [campus_filter, campus_filter]  # Default to filtering by the selected campus

    # Apply year filter if selected
    if year_filter:
        count_query += " AND Year = %s"
        params.append(year_filter)

    # Apply quarter filter if selected
    if quarter_filter:
        count_query += " AND Quarter = %s"
        params.append(quarter_filter)

    # Apply main category filter if selected
    if main_category_filter:
        count_query += " AND MainCategory = %s"
        params.append(main_category_filter)

    cursor.execute(count_query, params)
    total_records = cursor.fetchone()['total']

    # Calculate offset for pagination
    offset = (current_page - 1) * per_page

    # Base query for fetching paginated data with filters applied
    query = """
        SELECT Campus, Year, Quarter, Month, MainCategory, SubCategory, 
               QuantityInKG, GHGEmissionKGCO2e, GHGEmissionTCO2e
        FROM tblsolidwastesegregated
        WHERE (%s = 'All' OR Campus = %s)
    """
    query_params = [campus_filter, campus_filter]  # Default to filtering by the selected campus

    # Apply year filter if selected
    if year_filter:
        query += " AND Year = %s"
        query_params.append(year_filter)

    # Apply quarter filter if selected
    if quarter_filter:
        query += " AND Quarter = %s"
        query_params.append(quarter_filter)

    # Apply main category filter if selected
    if main_category_filter:
        query += " AND MainCategory = %s"
        query_params.append(main_category_filter)

    # Apply ordering and pagination
    query += " ORDER BY Year DESC, Month ASC LIMIT %s OFFSET %s"
    query_params.append(per_page)
    query_params.append(offset)

    cursor.execute(query, query_params)
    waste_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Calculate total pages
    total_pages = (total_records + per_page - 1) // per_page

    # Render the template with data
    return render_template(
        'sdo_waste_segregation_report.html',
        data=waste_data,
        current_page=current_page,
        total_pages=total_pages,
        campus_filter=campus_filter,
        year_filter=year_filter,
        quarter_filter=quarter_filter,
        main_category_filter=main_category_filter
    )

@app.route('/sdo_waste_segregation_pdf')
def sdo_waste_segregation_pdf():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)
    quarter = request.args.get("quarter", None)
    main_category = request.args.get("main_category", None)

    # Debug: Print the filter values
    print(f"Filters: campus={campus}, year={year}, quarter={quarter}, main_category={main_category}")

    # Fetch all data based on the filters
    data, _ = fetch_waste_segre_data(page=None, per_page=None, campus=campus, year=year, quarter=quarter, main_category=main_category)

    # Check if the data is empty
    if not data:
        return "No data available for the selected filters."

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a PDF file in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert DataFrame to list of lists (include headers and rows)
    data_list = [df.columns.tolist()] + df.values.tolist()  # Add headers and data rows

    # Create table and style
    table = Table(data_list)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the PDF with the table
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="waste_segregation_report.pdf", as_attachment=True, mimetype='application/pdf')

def fetch_waste_segre_data(page=1, per_page=20, campus=None, year=None, quarter=None, main_category=None):
    # Start the base query with a condition that always matches
    base_query = "SELECT * FROM tblsolidwastesegregated WHERE 1=1"
    total_query = "SELECT COUNT(*) AS total FROM tblsolidwastesegregated WHERE 1=1"
    params = []

    # Apply filters based on the parameters provided
    if campus and campus != 'All':  # Handle 'All' campus case
        base_query += " AND campus = %s"
        total_query += " AND campus = %s"
        params.append(campus)

    if year:
        base_query += " AND year = %s"
        total_query += " AND year = %s"
        params.append(year)

    if quarter:
        base_query += " AND quarter = %s"
        total_query += " AND quarter = %s"
        params.append(quarter)

    if main_category:
        base_query += " AND mainCategory = %s"
        total_query += " AND mainCategory = %s"
        params.append(main_category)

    # Apply pagination if both `page` and `per_page` are provided
    if page is not None and per_page is not None:
        offset = (page - 1) * per_page
        base_query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

    data = []
    total_records = 0

    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)

        # Fetch filtered records
        cursor.execute(base_query, params)
        data = cursor.fetchall()

        # Fetch the total count of filtered records (for pagination purposes)
        if page is not None and per_page is not None:
            cursor.execute(total_query, params[:-2])  # Exclude pagination parameters from count query
            total_records = cursor.fetchone()["total"]
        else:
            cursor.execute(total_query, params)
            total_records = cursor.fetchone()["total"]

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    return data, total_records

@app.route('/sdo_waste_segregation_excel')
def sdo_waste_segregation_excel():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)
    quarter = request.args.get("quarter", None)
    main_category = request.args.get("main_category", None)

    # Fetch all data based on the filters
    data, _ = fetch_waste_segre_data(page=None, per_page=None, campus=campus, year=year, quarter=quarter, main_category=main_category)

    # Check if the data is empty
    if not data:
        return "No data available for the selected filters."

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a BytesIO buffer to write the Excel file to memory
    buffer = BytesIO()
    
    # Write the DataFrame to the buffer as an Excel file
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Waste Segregation Report')

    # Seek to the beginning of the buffer to send the file
    buffer.seek(0)

    # Send the Excel file as a downloadable response
    return send_file(buffer, download_name="waste_segregation_report.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')



@app.route('/sdo_waste_unseg_report')
def sdo_waste_unseg_report():
    # Ensure that the user is logged in and has a valid session
    if 'campus' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    user_campus = session['campus']  # Get the campus from the session
    
    # Get filter parameters from the request arguments
    campus_filter = request.args.get("campus", "All")  # Default to 'All' if not provided
    year_filter = request.args.get("year", None)
    month_filter = request.args.get("month", None)
    
    # Pagination setup
    per_page = 20  # Records per page
    current_page = request.args.get('page', 1, type=int)

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Fetch rows as dictionaries

    # Base query for counting records (to calculate pages)
    count_query = """
        SELECT COUNT(*) as total 
        FROM tblsolidwasteunsegregated
        WHERE (%s = 'All' OR Campus = %s)
    """
    params = [campus_filter, campus_filter]  # Default to filtering by the selected campus

    # Apply year filter if selected
    if year_filter:
        count_query += " AND Year = %s"
        params.append(year_filter)

    # Apply month filter if selected
    if month_filter:
        count_query += " AND Month = %s"
        params.append(month_filter)

    cursor.execute(count_query, params)
    total_records = cursor.fetchone()['total']

    # Calculate offset for pagination
    offset = (current_page - 1) * per_page

    # Base query for fetching paginated data
    query = """
        SELECT Campus, Year, Month, WasteType, QuantityInKG, SentToLandfillKG, 
               SentToLandfillTONS, GHGEmissionKGCO2e, GHGEmissionTCO2e
        FROM tblsolidwasteunsegregated
        WHERE (%s = 'All' OR Campus = %s)
    """
    query_params = [campus_filter, campus_filter]  # Default to filtering by the selected campus

    # Apply year filter if selected
    if year_filter:
        query += " AND Year = %s"
        query_params.append(year_filter)

    # Apply month filter if selected
    if month_filter:
        query += " AND Month = %s"
        query_params.append(month_filter)

    # Apply ordering and pagination
    query += " ORDER BY Year DESC, Month ASC LIMIT %s OFFSET %s"
    query_params.append(per_page)
    query_params.append(offset)

    cursor.execute(query, query_params)
    waste_unseg_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Calculate total pages
    total_pages = (total_records + per_page - 1) // per_page

    # Create the pagination URL with filters
    pagination_url = url_for('sdo_waste_unseg_report', campus=campus_filter, year=year_filter, month=month_filter)

    # Render the template with data
    return render_template(
        'sdo_waste_unseg_report.html',
        data=waste_unseg_data,
        current_page=current_page,
        total_pages=total_pages,
        campus_filter=campus_filter,
        year_filter=year_filter,
        month_filter=month_filter,
        pagination_url=pagination_url
    )

@app.route('/sdo_waste_unseg_excel')
def sdo_waste_unseg_excel():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)
    month = request.args.get("month", None)

    # Fetch all data based on the filters (ignore pagination)
    data, _ = fetch_waste_unseg_data(page=None, per_page=None, campus=campus, year=year, month=month, fetch_all=True)

    # Check if the data is empty
    if not data:
        return "No data available for the selected filters."

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a BytesIO buffer to write the Excel file to memory
    buffer = BytesIO()

    # Write the DataFrame to the buffer as an Excel file
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Waste Unsegregated Report')

    # Seek to the beginning of the buffer to send the file
    buffer.seek(0)

    # Send the Excel file as a downloadable response
    return send_file(buffer, download_name="waste_unsegregated_report.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/sdo_waste_unseg_pdf')
def sdo_waste_unseg_pdf():
    # Retrieve filter parameters from request arguments
    campus = request.args.get("campus", None)
    year = request.args.get("year", None)
    month = request.args.get("month", None)

    # Fetch all data based on the filters (ignoring pagination)
    data, _ = fetch_waste_unseg_data(page=None, per_page=None, campus=campus, year=year, month=month, fetch_all=True)

    # Check if the data is empty
    if not data:
        return "No data available for the selected filters."

    # Convert data into a list of lists (for the PDF Table)
    table_data = [["Campus", "Year", "Month", "Waste Type", "Quantity (KG)", 
                   "Sent to Landfill (KG)", "Sent to Landfill (TONS)", 
                   "GHG Emission (KG CO₂e)", "GHG Emission (T CO₂e)"]]
    for row in data:
        table_data.append([
            row["Campus"], row["Year"], row["Month"], row["WasteType"], 
            row["QuantityInKG"], row["SentToLandfillKG"], row["SentToLandfillTONS"], 
            row["GHGEmissionKGCO2e"], row["GHGEmissionTCO2e"]
        ])

    # Create a PDF in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Create the table for the PDF
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 8),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Gridlines for the table
    ]))

    # Build the PDF
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF file as a downloadable response
    return send_file(buffer, download_name="waste_unsegregated_report.pdf", as_attachment=True, mimetype='application/pdf')

def fetch_waste_unseg_data(page=1, per_page=20, campus=None, year=None, month=None, fetch_all=False):
    # If `fetch_all` is True, ignore pagination
    if fetch_all:
        page = None
        per_page = None

    # Calculate the offset based on page and per_page (only if pagination is applied)
    offset = (page - 1) * per_page if page and per_page else 0
    
    base_query = "SELECT * FROM tblsolidwasteunsegregated WHERE 1=1"
    total_query = "SELECT COUNT(*) AS total FROM tblsolidwasteunsegregated WHERE 1=1"
    params = []

    # Apply campus filter if provided and not "All"
    if campus and campus != "All":
        base_query += " AND Campus = %s"
        total_query += " AND Campus = %s"
        params.append(campus)

    # Apply year filter if provided
    if year:
        base_query += " AND Year = %s"
        total_query += " AND Year = %s"
        params.append(year)

    # Apply month filter if provided
    if month:
        base_query += " AND Month = %s"
        total_query += " AND Month = %s"
        params.append(month)

    # Add pagination limits only if not fetching all data
    if not fetch_all:
        base_query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

    print(f"Executing query: {base_query}")
    print(f"With parameters: {params}")

    data = []
    total_records = 0

    try:
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)
        
        # Fetch records with applied filters (and pagination, if not `fetch_all`)
        cursor.execute(base_query, params)
        data = cursor.fetchall()

        # Fetch the total record count with the same filters (without pagination)
        if not fetch_all:
            cursor.execute(total_query, params[:-2])  # Exclude pagination params for count query
        else:
            cursor.execute(total_query, params)
        total_records = cursor.fetchone()["total"]

        # Debug: Print fetched data
        print(f"Fetched {len(data)} records.")

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    return data, total_records





@app.route('/sdo_food_consumption_report')
def sdo_food_consumption_report():
    # Ensure that the user is logged in and has a valid session
    if 'campus' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    user_campus = session['campus']  # Get the campus from the session
    
    # Get filter parameters from the request arguments
    campus_filter = request.args.get("campus", user_campus)  # Default to user campus if not provided
    year_filter = request.args.get("year", None)
    month_filter = request.args.get("month", None)
    office_filter = request.args.get("office", None)
    
    # Pagination setup
    per_page = 20  # Records per page
    current_page = request.args.get('page', 1, type=int)

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to fetch rows as dicts

    # Base query for counting records (to calculate pages)
    count_query = """
        SELECT COUNT(*) as total 
        FROM tblfoodwaste
        WHERE (%s = 'All' OR Campus = %s)
    """
    params = [campus_filter, campus_filter]  # Default to filtering by the selected campus

    # Apply year filter if selected
    if year_filter:
        count_query += " AND YearTransaction = %s"
        params.append(year_filter)

    # Apply month filter if selected
    if month_filter:
        count_query += " AND Month = %s"
        params.append(month_filter)

    # Apply office filter if selected
    if office_filter:
        count_query += " AND Office = %s"
        params.append(office_filter)

    cursor.execute(count_query, params)
    total_records = cursor.fetchone()['total']

    # Calculate offset for pagination
    offset = (current_page - 1) * per_page

    # Base query for fetching paginated data
    query = """
        SELECT Campus, YearTransaction, Month, Office, TypeOfFoodServed, QuantityOfServing, 
               GHGEmissionKGCO2e, GHGEmissionTCO2e
        FROM tblfoodwaste
        WHERE (%s = 'All' OR Campus = %s)
    """
    query_params = [campus_filter, campus_filter]  # Default to filtering by the selected campus

    # Apply year filter if selected
    if year_filter:
        query += " AND YearTransaction = %s"
        query_params.append(year_filter)

    # Apply month filter if selected
    if month_filter:
        query += " AND Month = %s"
        query_params.append(month_filter)

    # Apply office filter if selected
    if office_filter:
        query += " AND Office = %s"
        query_params.append(office_filter)

    # Apply ordering and pagination
    query += " ORDER BY YearTransaction DESC, Month ASC LIMIT %s OFFSET %s"
    query_params.append(per_page)
    query_params.append(offset)

    cursor.execute(query, query_params)
    food_waste_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Calculate total pages
    total_pages = (total_records + per_page - 1) // per_page

    # Create the pagination URL with filters
    pagination_url = url_for('sdo_food_consumption_report', campus=campus_filter, year=year_filter, month=month_filter, office=office_filter)

    # Render the template with data
    return render_template(
        'sdo_food_consumption_report.html',
        data=food_waste_data,
        current_page=current_page,
        total_pages=total_pages,
        campus_filter=campus_filter,
        year_filter=year_filter,
        month_filter=month_filter,
        office_filter=office_filter,
        pagination_url=pagination_url
    )

@app.route('/sdo_food_consumption_pdf')
def sdo_food_consumption_pdf():
    # Get filter parameters
    campus = request.args.get("campus", "All")
    year = request.args.get("year", None)
    month = request.args.get("month", None)
    office = request.args.get("office", None)

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Build the WHERE clause dynamically
    filter_conditions = []
    params = []

    if campus != 'All':
        filter_conditions.append("Campus = %s")
        params.append(campus)

    if year:
        filter_conditions.append("YearTransaction = %s")
        params.append(year)

    if month:
        filter_conditions.append("Month = %s")
        params.append(month)

    if office:
        filter_conditions.append("Office = %s")
        params.append(office)

    where_clause = ""
    if filter_conditions:
        where_clause = "WHERE " + " AND ".join(filter_conditions)

    # Query to fetch all data matching the filters
    query = f"""
        SELECT Campus, YearTransaction, Month, Office, TypeOfFoodServed, QuantityOfServing, 
               GHGEmissionKGCO2e, GHGEmissionTCO2e
        FROM tblfoodwaste {where_clause}
        ORDER BY YearTransaction DESC, Month ASC
    """
    cursor.execute(query, tuple(params))
    food_data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Check if data exists
    if not food_data:
        return "No data available for the selected filters."

    # Create a PDF file in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(food_data)

    # Convert DataFrame to list of lists (headers + data)
    data_list = [df.columns.tolist()] + df.values.tolist()

    # Create a table with ReportLab
    table = Table(data_list)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the PDF
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="food_consumption_report.pdf", as_attachment=True, mimetype='application/pdf')

@app.route('/sdo_food_consumption_excel')
def sdo_food_consumption_excel():
    # Get filter parameters
    campus = request.args.get("campus", "All")
    year = request.args.get("year", None)
    month = request.args.get("month", None)
    office = request.args.get("office", None)

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Build the WHERE clause dynamically
    filter_conditions = []
    params = []

    if campus != 'All':
        filter_conditions.append("Campus = %s")
        params.append(campus)

    if year:
        filter_conditions.append("YearTransaction = %s")
        params.append(year)

    if month:
        filter_conditions.append("Month = %s")
        params.append(month)

    if office:
        filter_conditions.append("Office = %s")
        params.append(office)

    where_clause = ""
    if filter_conditions:
        where_clause = "WHERE " + " AND ".join(filter_conditions)

    # Query to fetch all data matching the filters
    query = f"""
        SELECT Campus, YearTransaction, Month, Office, TypeOfFoodServed, QuantityOfServing, 
               GHGEmissionKGCO2e, GHGEmissionTCO2e
        FROM tblfoodwaste {where_clause}
        ORDER BY YearTransaction DESC, Month ASC
    """
    cursor.execute(query, tuple(params))
    food_data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Check if data exists
    if not food_data:
        return "No data available for the selected filters."

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(food_data)

    # Create a BytesIO buffer to write the Excel file to memory
    buffer = BytesIO()

    # Write the DataFrame to the Excel file
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Food Waste Report')

    buffer.seek(0)

    # Send the Excel file as a downloadable response
    return send_file(
        buffer,
        download_name="food_consumption_report.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@app.route('/sdo_lpg_consumption_report')
def sdo_lpg_consumption_report():
    # Ensure that the user is logged in and has a valid session
    if 'campus' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    user_campus = session['campus']  # Get the campus from the session

    # Pagination setup
    per_page = 20  # Records per page
    current_page = request.args.get('page', 1, type=int)

    # Get filter values from request arguments
    campus_filter = request.args.get('campus', 'All')
    year_filter = request.args.get('year', '')
    month_filter = request.args.get('month', '')
    office_filter = request.args.get('office', '')

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Fetch rows as dictionaries

    # Build the WHERE clause dynamically based on filters
    filter_conditions = []
    params = []

    if campus_filter != 'All':
        filter_conditions.append("Campus = %s")
        params.append(campus_filter)

    if year_filter:
        filter_conditions.append("YearTransact = %s")
        params.append(year_filter)

    if month_filter:
        filter_conditions.append("Month = %s")
        params.append(month_filter)

    if office_filter:
        filter_conditions.append("Office = %s")
        params.append(office_filter)

    # If no filter is applied, show all data
    where_clause = ""
    if filter_conditions:
        where_clause = "WHERE " + " AND ".join(filter_conditions)
    
    # Query for total records (to calculate pages)
    count_query = f"SELECT COUNT(*) as total FROM tbllpg {where_clause}"
    cursor.execute(count_query, tuple(params))
    total_records = cursor.fetchone()['total']

    # Calculate offset for pagination
    offset = (current_page - 1) * per_page

    # Fetch paginated data
    query = f"""
        SELECT Campus, YearTransact, Month, Office, ConcessionariesType, TankQuantity, 
               TankWeight, TankVolume, TotalTankVolume, GHGEmissionKGCO2e, GHGEmissionTCO2e
        FROM tbllpg {where_clause}
        ORDER BY YearTransact DESC, Month ASC
        LIMIT %s OFFSET %s
    """
    cursor.execute(query, tuple(params + [per_page, offset]))
    lpg_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Calculate total pages
    total_pages = (total_records + per_page - 1) // per_page

    # Render the template with data and filter parameters
    return render_template(
        'sdo_lpg_consumption_report.html',
        data=lpg_data,
        current_page=current_page,
        total_pages=total_pages,
        campus_filter=campus_filter,
        year_filter=year_filter,
        month_filter=month_filter,
        office_filter=office_filter
    )

@app.route('/sdo_lpg_consumption_pdf')
def sdo_lpg_consumption_pdf():
    # Get filter values from request arguments
    campus = request.args.get('campus', 'All')
    year = request.args.get('year', '')
    month = request.args.get('month', '')
    office = request.args.get('office', '')

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Build the WHERE clause dynamically based on filters
    filter_conditions = []
    params = []

    if campus != 'All':
        filter_conditions.append("Campus = %s")
        params.append(campus)

    if year:
        filter_conditions.append("YearTransact = %s")
        params.append(year)

    if month:
        filter_conditions.append("Month = %s")
        params.append(month)

    if office:
        filter_conditions.append("Office = %s")
        params.append(office)

    # If no filter is applied, show all data
    where_clause = ""
    if filter_conditions:
        where_clause = "WHERE " + " AND ".join(filter_conditions)

    # Query for all data matching the filters (no pagination)
    query = f"""
        SELECT Campus, YearTransact, Month, Office, ConcessionariesType, TankQuantity, 
               TankWeight, TankVolume, TotalTankVolume, GHGEmissionKGCO2e, GHGEmissionTCO2e
        FROM tbllpg {where_clause}
        ORDER BY YearTransact DESC, Month ASC
    """
    cursor.execute(query, tuple(params))
    lpg_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Check if data is empty
    if not lpg_data:
        return "No data available for the selected filters."

    # Prepare table data for the PDF
    table_data = [["Campus", "Year", "Month", "Office", "Concessionaire Type", "Qty (no. of tanks)",
                   "Tank Weight", "Tank Volume", "Total Tank Volume", "GHG Emission (KG CO₂e)", "GHG Emission (T CO₂e)"]]
    for row in lpg_data:
        table_data.append([
            row["Campus"], row["YearTransact"], row["Month"], row["Office"], row["ConcessionariesType"],
            row["TankQuantity"], row["TankWeight"], row["TankVolume"], row["TotalTankVolume"],
            row["GHGEmissionKGCO2e"], row["GHGEmissionTCO2e"]
        ])

    # Generate PDF
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Create the table for the PDF
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 8),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Gridlines for the table
    ]))

    # Build the PDF
    pdf.build([table])

    # Return the PDF file as a downloadable response
    buffer.seek(0)
    return send_file(buffer, download_name="lpg_consumption_report.pdf", as_attachment=True, mimetype='application/pdf')

@app.route('/sdo_lpg_consumption_excel')
def sdo_lpg_consumption_excel():
    # Get filter values from request arguments
    campus = request.args.get('campus', 'All')
    year = request.args.get('year', '')
    month = request.args.get('month', '')
    office = request.args.get('office', '')

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Build the WHERE clause dynamically based on filters
    filter_conditions = []
    params = []

    if campus != 'All':
        filter_conditions.append("Campus = %s")
        params.append(campus)

    if year:
        filter_conditions.append("YearTransact = %s")
        params.append(year)

    if month:
        filter_conditions.append("Month = %s")
        params.append(month)

    if office:
        filter_conditions.append("Office = %s")
        params.append(office)

    # If no filter is applied, show all data
    where_clause = ""
    if filter_conditions:
        where_clause = "WHERE " + " AND ".join(filter_conditions)

    # Query to fetch all data matching the filters
    query = f"""
        SELECT Campus, YearTransact, Month, Office, ConcessionariesType, TankQuantity, 
               TankWeight, TankVolume, TotalTankVolume, GHGEmissionKGCO2e, GHGEmissionTCO2e
        FROM tbllpg {where_clause}
        ORDER BY YearTransact DESC, Month ASC
    """
    cursor.execute(query, tuple(params))
    lpg_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Check if data is empty
    if not lpg_data:
        return "No data available for the selected filters."

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(lpg_data)

    # Create an in-memory Excel file
    buffer = BytesIO()

    # Write the DataFrame to the Excel file
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='LPG Consumption Report')

    # Set the buffer position to the start
    buffer.seek(0)

    # Send the Excel file as a downloadable response
    return send_file(
        buffer,
        download_name="lpg_consumption_report.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@app.route('/sdo_flight_emissions_report')
def sdo_flight_emissions_report():
    # Ensure the user is logged in
    if 'campus' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    user_campus = session['campus']  # Get the campus from the session
    
    # Pagination setup
    per_page = 20  # Records per page
    current_page = request.args.get('page', 1, type=int)

    # Get filter values from the request arguments
    campus_filter = request.args.get('campus', user_campus)  # Default to user's campus
    office_filter = request.args.get('office', '')
    year_filter = request.args.get('year', '')

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query to count the total records after applying the filters
    count_query = """
        SELECT COUNT(*) as total
        FROM tblflight
        WHERE (%s = '' OR Campus = %s)
        AND (%s = '' OR Office = %s)
        AND (%s = '' OR Year = %s)
    """
    cursor.execute(count_query, (campus_filter, campus_filter, office_filter, office_filter, year_filter, year_filter))
    total_records = cursor.fetchone()['total']

    # Calculate offset for pagination
    offset = (current_page - 1) * per_page

    # Query to fetch paginated data based on the filters
    query = """
        SELECT Campus, Office, Year, TravellerName, TravelPurpose, TravelDate, 
               DomesticInternational, Origin, Destination, Class, OnewayRoundTrip, 
               GHGEmissionKGC02e, GHGEmissionTC02e
        FROM tblflight
        WHERE (%s = '' OR Campus = %s)
        AND (%s = '' OR Office = %s)
        AND (%s = '' OR Year = %s)
        ORDER BY TravelDate DESC
        LIMIT %s OFFSET %s
    """
    cursor.execute(query, (campus_filter, campus_filter, office_filter, office_filter, year_filter, year_filter, per_page, offset))
    flight_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Calculate total pages
    total_pages = (total_records + per_page - 1) // per_page

    # Render the template with data and filters
    return render_template(
        'sdo_flight_emissions_report.html',
        data=flight_data,
        current_page=current_page,
        total_pages=total_pages,
        campus_filter=campus_filter,
        office_filter=office_filter,
        year_filter=year_filter
    )

@app.route('/sdo_flight_emissions_pdf')
def sdo_flight_emissions_pdf():
    # Get filter parameters
    campus = request.args.get("campus", "")
    office = request.args.get("office", "")
    year = request.args.get("year", "")

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Build the WHERE clause dynamically
    filter_conditions = []
    params = []

    if campus:
        filter_conditions.append("Campus = %s")
        params.append(campus)

    if office:
        filter_conditions.append("Office = %s")
        params.append(office)

    if year:
        filter_conditions.append("Year = %s")
        params.append(year)

    where_clause = ""
    if filter_conditions:
        where_clause = "WHERE " + " AND ".join(filter_conditions)

    # Query to fetch all data matching the filters
    query = f"""
        SELECT Campus, Office, Year, TravellerName, TravelPurpose, TravelDate, 
               DomesticInternational, Origin, Destination, Class, OnewayRoundTrip, 
               GHGEmissionKGC02e, GHGEmissionTC02e
        FROM tblflight {where_clause}
        ORDER BY TravelDate DESC
    """
    cursor.execute(query, tuple(params))
    flight_data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Check if data exists
    if not flight_data:
        return "No data available for the selected filters."

    # Create a PDF file in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(flight_data)

    # Convert DataFrame to list of lists (headers + data)
    data_list = [df.columns.tolist()] + df.values.tolist()

    # Adjust column widths to fit the page width (landscape A4 = ~842 points)
    column_widths = [
        60,  # Campus
        60,  # Office
        40,  # Year
        80, # TravellerName
        80, # TravelPurpose
        60,  # TravelDate
        60,  # Domestic/International
        60,  # Origin
        60,  # Destination
        50,  # Class
        60,  # OneWay/RoundTrip
        80,  # GHGEmissionKGC02e
        80   # GHGEmissionTC02e
    ]

    # Create a table with ReportLab
    table = Table(data_list, colWidths=column_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),  # Slightly larger font for headers
        ('FONTSIZE', (0, 1), (-1, -1), 6),  # Smaller font for data
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    # Build the PDF
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="flight_emissions_report.pdf", as_attachment=True, mimetype='application/pdf')

@app.route('/sdo_flight_emissions_excel')
def sdo_flight_emissions_excel():
    # Get filter parameters
    campus = request.args.get("campus", "")
    office = request.args.get("office", "")
    year = request.args.get("year", "")

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Build the WHERE clause dynamically
    filter_conditions = []
    params = []

    if campus:
        filter_conditions.append("Campus = %s")
        params.append(campus)

    if office:
        filter_conditions.append("Office = %s")
        params.append(office)

    if year:
        filter_conditions.append("Year = %s")
        params.append(year)

    where_clause = ""
    if filter_conditions:
        where_clause = "WHERE " + " AND ".join(filter_conditions)

    # Query to fetch all data matching the filters
    query = f"""
        SELECT Campus, Office, Year, TravellerName, TravelPurpose, TravelDate, 
               DomesticInternational, Origin, Destination, Class, OnewayRoundTrip, 
               GHGEmissionKGC02e, GHGEmissionTC02e
        FROM tblflight {where_clause}
        ORDER BY TravelDate DESC
    """
    cursor.execute(query, tuple(params))
    flight_data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Check if data exists
    if not flight_data:
        return "No data available for the selected filters."

    # Convert data into a pandas DataFrame
    df = pd.DataFrame(flight_data)

    # Create a BytesIO buffer to write the Excel file to memory
    buffer = BytesIO()

    # Write the DataFrame to the Excel file
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Flight Emissions Report')

    buffer.seek(0)

    # Send the Excel file as a downloadable response
    return send_file(
        buffer,
        download_name="flight_emissions_report.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@app.route('/sdo_accommodation_emissions_report')
def sdo_accommodation_emissions_report():
    # Ensure that the user is logged in and has a valid session
    if 'campus' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    user_campus = session['campus']  # Get the campus from the session
    
    # Pagination setup
    per_page = 20  # Records per page
    current_page = request.args.get('page', 1, type=int)

    # Get filter values from request args
    campus_filter = request.args.get('campus', '')
    office_filter = request.args.get('office', '')
    year_filter = request.args.get('year', '')
    
    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Fetch rows as dictionaries

    # Base query for total records, applying filters if provided
    count_query = """
        SELECT COUNT(*) as total 
        FROM tblaccommodation
        WHERE (%s = '' OR Campus = %s)
        AND (%s = '' OR Office = %s)
        AND (%s = '' OR YearTransact = %s)
    """
    cursor.execute(count_query, (campus_filter, campus_filter, office_filter, office_filter, year_filter, year_filter))
    total_records = cursor.fetchone()['total']

    # Calculate offset for pagination
    offset = (current_page - 1) * per_page

    # Query for paginated data, applying filters if provided
    query = """
        SELECT Campus, Office, YearTransact, TravellerName, TravelPurpose, TravelDateFrom, 
               TravelDateTo, Country, TravelType, NumOccupiedRoom, NumNightPerRoom, 
               GHGEmissionKGC02e, GHGEmissionTC02e
        FROM tblaccommodation
        WHERE (%s = '' OR Campus = %s)
        AND (%s = '' OR Office = %s)
        AND (%s = '' OR YearTransact = %s)
        ORDER BY TravelDateFrom DESC
        LIMIT %s OFFSET %s
    """
    cursor.execute(query, (campus_filter, campus_filter, office_filter, office_filter, year_filter, year_filter, per_page, offset))
    accommodation_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Calculate total pages
    total_pages = (total_records + per_page - 1) // per_page

    # Render the template with data and filters
    return render_template(
        'sdo_accommodation_emissions_report.html',
        data=accommodation_data,
        current_page=current_page,
        total_pages=total_pages,
        campus_filter=campus_filter,
        office_filter=office_filter,
        year_filter=year_filter
    )

@app.route('/sdo_accommodation_emissions_pdf')
def sdo_accommodation_emissions_pdf():
    # Get filter parameters
    campus = request.args.get("campus", "")
    office = request.args.get("office", "")
    year = request.args.get("year", "")

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Build WHERE clause dynamically based on filters
    filter_conditions = []
    params = []

    if campus:
        filter_conditions.append("Campus = %s")
        params.append(campus)

    if office:
        filter_conditions.append("Office = %s")
        params.append(office)

    if year:
        filter_conditions.append("YearTransact = %s")
        params.append(year)

    where_clause = ""
    if filter_conditions:
        where_clause = "WHERE " + " AND ".join(filter_conditions)

    # Query to fetch filtered data
    query = f"""
        SELECT Campus, Office, YearTransact, TravellerName, TravelPurpose, TravelDateFrom, 
               TravelDateTo, Country, TravelType, NumOccupiedRoom, NumNightPerRoom, 
               GHGEmissionKGC02e, GHGEmissionTC02e
        FROM tblaccommodation
        {where_clause}
        ORDER BY TravelDateFrom DESC
    """
    cursor.execute(query, tuple(params))
    accommodation_data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Check if data exists
    if not accommodation_data:
        return "No data available for the selected filters."

    # Create a PDF in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Convert data to pandas DataFrame
    df = pd.DataFrame(accommodation_data)

    # Convert DataFrame to list of lists (headers + data)
    data_list = [df.columns.tolist()] + df.values.tolist()

    # Define column widths to fit the page
    column_widths = [
        40,  # Campus
        50,  # Office
        50,  # YearTransact
        80, # TravellerName
        80, # TravelPurpose
        70,  # TravelDateFrom
        70,  # TravelDateTo
        60,  # Country
        40,  # TravelType
        60,  # NumOccupiedRoom
        60,  # NumNightPerRoom
        80,  # GHGEmissionKGC02e
        80   # GHGEmissionTC02e
    ]

    # Create table with ReportLab
    table = Table(data_list, colWidths=column_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),  # Slightly larger font for headers
        ('FONTSIZE', (0, 1), (-1, -1), 6),  # Smaller font for data
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    # Build the PDF
    pdf.build([table])

    buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(buffer, download_name="accommodation_emissions_report.pdf", as_attachment=True, mimetype='application/pdf')


@app.route('/sdo_accommodation_emissions_excel')
def sdo_accommodation_emissions_excel():
    # Get filter parameters
    campus = request.args.get("campus", "")
    office = request.args.get("office", "")
    year = request.args.get("year", "")

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Build WHERE clause dynamically based on filters
    filter_conditions = []
    params = []

    if campus:
        filter_conditions.append("Campus = %s")
        params.append(campus)

    if office:
        filter_conditions.append("Office = %s")
        params.append(office)

    if year:
        filter_conditions.append("YearTransact = %s")
        params.append(year)

    where_clause = ""
    if filter_conditions:
        where_clause = "WHERE " + " AND ".join(filter_conditions)

    # Query to fetch filtered data
    query = f"""
        SELECT Campus, Office, YearTransact, TravellerName, TravelPurpose, TravelDateFrom, 
               TravelDateTo, Country, TravelType, NumOccupiedRoom, NumNightPerRoom, 
               GHGEmissionKGC02e, GHGEmissionTC02e
        FROM tblaccommodation
        {where_clause}
        ORDER BY TravelDateFrom DESC
    """
    cursor.execute(query, tuple(params))
    accommodation_data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Check if data exists
    if not accommodation_data:
        return "No data available for the selected filters."

    # Convert data to pandas DataFrame
    df = pd.DataFrame(accommodation_data)

    # Create a BytesIO buffer to write Excel file
    buffer = BytesIO()

    # Write DataFrame to Excel
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Accommodation Emissions Report')

    buffer.seek(0)

    # Send the Excel file as a downloadable response
    return send_file(
        buffer,
        download_name="accommodation_emissions_report.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# Route for Manage Account (renamed to manageacc_sdo)
@app.route('/manageacc_sdo', methods=['GET', 'POST'])
def manageacc_sdo():
    if request.method == 'POST':
        username = request.form['username']
        office = request.form['office']
        campus = request.form['campus']
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert into the tblsignin table
            cursor.execute(
                "INSERT INTO tblsignin (username, office, campus, email, password) VALUES (%s, %s, %s, %s, %s)",
                (username, office, campus, email, password)
            )
            conn.commit()
            flash('Account created successfully!', 'success')

        except mysql.connector.Error as e:
            flash(f'Database Error: {e}', 'danger')

        finally:
            cursor.close()
            conn.close()

    return render_template('manageacc_sdo.html')

@app.route('/sdo_report')
def sdo_report():
    # Check if the user is logged in and campus is available in session
    if 'loggedIn' in session and 'campus' in session:
        campus = session['campus']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Queries to retrieve data based on campus
            queries = {
                'electricity_data': "SELECT * FROM electricity_consumption WHERE campus = %s",
                'water_data': "SELECT * FROM tblwater WHERE campus = %s",
                'unseg_waste_data': "SELECT * FROM tblsolidwasteunsegregated WHERE campus = %s",
                'seg_waste_data': "SELECT * FROM tblsolidwastesegregated WHERE campus = %s",
                'treated_water_data': "SELECT * FROM tbltreatedwater WHERE campus = %s",
                'lpg_data': "SELECT * FROM tbllpg WHERE campus = %s",
                'fuel_data': "SELECT * FROM fuel_emissions WHERE campus = %s",
                'food_waste_data': "SELECT * FROM tblfoodwaste WHERE campus = %s",
                'accommodation_data': "SELECT * FROM tblaccommodation WHERE campus = %s",
                'flight_data': "SELECT * FROM tblflight WHERE campus = %s"
            }

            data = {}
            for key, query in queries.items():
                cursor.execute(query, (campus,))
                data[key] = cursor.fetchall()

        except Exception as e:
            # Handle errors (log it or render an error page)
            print(f"An error occurred: {e}")
            return render_template('error.html', error_message="An error occurred while retrieving data.")

        finally:
            # Ensure the connection is closed
            cursor.close()
            conn.close()

        return render_template('sdo_report.html', **data)
    
    return redirect(url_for('login'))

@app.route('/get_full_report', methods=['GET'])
def get_full_report():
    table_name = request.args.get('table')
    campus = session.get('campus')

    if not campus:
        return jsonify({"error": "Campus not found in session"}), 400

    table_map = {
        'electricityTable': 'electricity_consumption',
        'waterTable': 'tblwater',
        'segWasteTable': 'tblsolidwastesegregated',
        'unsegWasteTable': 'tblsolidwasteunsegregated',
        'treatedWaterTable': 'tbltreatedwater',
        'lpgTable': 'tbllpg',
        'fuelEmissionsTable': 'fuel_emissions',
        'foodWasteTable': 'tblfoodwaste',
        'flightTable': 'tblflight',
        'accommodationTable': 'tblaccommodation'
    }

    if table_name not in table_map:
        return jsonify({"error": "Invalid table name"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        sql = f"SELECT * FROM {table_map[table_name]} WHERE campus = %s"
        cursor.execute(sql, (campus,))
        data = cursor.fetchall()

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()



import decimal  # Import decimal for Decimal type handling
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np
from flask import session, redirect, url_for, request, render_template, flash
import mysql.connector
from datetime import datetime

@app.route('/external_dashboard', methods=['GET', 'POST'])
def external_dashboard():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    selected_campus = request.args.get('campus', 'all')
    selected_year = int(request.args.get('year', datetime.now().year))
    selected_month = request.args.get('month', None)
    current_year = datetime.now().year

    # Initialize data lists for emissions
    flight_data = [0] * 5  # For years 2020 to 2024
    accommodation_data = [0] * 5  # For years 2020 to 2024

    current_emission_data = {
        "flight": 0,
        "accommodation": 0,
    }

    month_to_index = {
        "January": 0, "February": 1, "March": 2, "April": 3, "May": 4, "June": 5,
        "July": 6, "August": 7, "September": 8, "October": 9, "November": 10, "December": 11
    }

    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Could not establish database connection.")

        cursor = conn.cursor(dictionary=True)

        # Queries for flight and accommodation data
        queries = [
            ("SELECT Year, SUM(GHGEmissionKGC02e) AS total_emission FROM tblflight WHERE (%s = 'all' OR campus = %s) AND Year BETWEEN 2020 AND 2024 GROUP BY Year ORDER BY Year", flight_data, "flight"),
(
    """
    SELECT YearTransact AS Year, 
           SUM(GHGEmissionKGC02e) AS total_emission 
    FROM tblaccommodation 
    WHERE (%s = 'all' OR Campus = %s) 
          AND YearTransact BETWEEN 2020 AND 2024 
    GROUP BY YearTransact 
    ORDER BY YearTransact ASC
    """, 
    accommodation_data, 
    "accommodation"
)
        ]

        for query, data_list, category in queries:
            cursor.execute(query, (selected_campus, selected_campus))
            for row in cursor.fetchall():
                year_index = row['Year'] - 2020
                if 0 <= year_index < len(data_list):
                    data_list[year_index] = float(row['total_emission'])
                    current_emission_data[category] += float(row['total_emission'])

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Forecast function using Prophet
    def forecast_prophet(data, periods):
        if all(v == 0 for v in data):
            return [0] * periods, 0

        try:
            df = pd.DataFrame({'ds': pd.date_range(start='2023-01-01', periods=len(data), freq='M'), 'y': data})
            df = df[df['y'] > 0]
            model = Prophet(yearly_seasonality=True)
            model.fit(df)
            future = model.make_future_dataframe(periods=periods, freq='M')
            forecast = model.predict(future)
            return forecast['yhat'][-periods:].tolist(), r2_score(df['y'], model.predict(df)['yhat'])
        except Exception as e:
            flash(f"Forecast Error: {e}", "danger")
            return [0] * periods, 0

    # Forecast data with R² scores
    forecast_data = {
        "flight_forecast": {
            "prophet": {
                "forecast": forecast_prophet(flight_data, periods=5)[0],
                "r2_score": forecast_prophet(flight_data, periods=5)[1],
            }
        },
        "accommodation_forecast": {
            "prophet": {
                "forecast": forecast_prophet(accommodation_data, periods=5)[0],
                "r2_score": forecast_prophet(accommodation_data, periods=5)[1],
            }
        },
    }

    # Print R² scores for validation
    for key, value in forecast_data.items():
        print(f"{key.replace('_forecast', '').title()} Prophet R² Score:", value["prophet"]["r2_score"])

    return render_template(
        'external_dashboard.html',
        flight_data=flight_data,
        accommodation_data=accommodation_data,
        forecast_data=forecast_data,
        current_emission_data=current_emission_data,
        selected_campus=selected_campus,
        selected_year=selected_year,
        current_year=current_year,
    )


@app.route('/flight', methods=['GET', 'POST'])
def flight():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Get the logged-in campus from the session
    session_campus = session.get('campus')

    # Determine associated campuses based on the logged-in campus
    if session_campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif session_campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        # For any other campus, include only that campus
        associated_campuses = [session_campus]

    if request.method == 'POST':
        # Handle flight data submission
        try:
            # Extract form data, including the specific campus from the form
            campus = request.form.get('campus')  # Get campus from the form input
            office = request.form.get('office')
            year = request.form.get('year')
            traveller_name = request.form.get('travellerName')
            travel_purpose = request.form.get('travelPurpose')
            travel_date = request.form.get('travelDate')
            domestic_international = request.form.get('domesticInternational')
            origin = request.form.get('origin')
            destination = request.form.get('destination')
            flight_class = request.form.get('class')
            oneway_roundtrip = request.form.get('onewayRoundTrip')
            ghg_emission_kg_co2e = float(request.form.get('ghgEmissionKGC02e', 0))
            ghg_emission_t_co2e = float(request.form.get('ghgEmissionTC02e', 0))

            # Database connection and insertion
            conn = get_db_connection()
            cursor = conn.cursor()

            sql = """INSERT INTO tblflight (Campus, Office, Year, TravellerName, TravelPurpose, TravelDate, DomesticInternational, 
                     Origin, Destination, Class, OnewayRoundTrip, GHGEmissionKGC02e, GHGEmissionTC02e) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (campus, office, year, traveller_name, travel_purpose, travel_date, domestic_international, 
                                 origin, destination, flight_class, oneway_roundtrip, ghg_emission_kg_co2e, ghg_emission_t_co2e))
            conn.commit()

            flash("Flight record inserted successfully!", "success")
        except mysql.connector.Error as e:
            flash(f"Database Error: {e}", "danger")
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('flight'))

    # Get current page and year filter from request arguments, default page to 1 and year to None
    current_page = int(request.args.get('page', 1))
    selected_year = request.args.get('year')

    # Build SQL query for selecting records with campus association
    placeholders = ', '.join(['%s'] * len(associated_campuses))
    query = f"SELECT * FROM tblflight WHERE Campus IN ({placeholders})"
    params = associated_campuses[:]

    if selected_year:
        query += " AND Year = %s"
        params.append(selected_year)

    limit = 10
    offset = (current_page - 1) * limit
    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)

    flight_data = cursor.fetchall()

    # Count total records for pagination with the same filtering
    count_query = f"SELECT COUNT(*) AS total FROM tblflight WHERE Campus IN ({placeholders})"
    count_params = associated_campuses[:]

    if selected_year:
        count_query += " AND Year = %s"
        count_params.append(selected_year)

    cursor.execute(count_query, count_params)
    total_records = cursor.fetchone()['total']
    total_pages = (total_records // limit) + (1 if total_records % limit > 0 else 0)

    cursor.close()
    conn.close()

    return render_template('flight.html', flight_data=flight_data, total_pages=total_pages, 
                           current_page=current_page, selected_year=selected_year)

@app.route('/flight/all', methods=['GET'])
def get_all_flight_data():
    if 'loggedIn' not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    # Get the logged-in campus from the session
    session_campus = session.get('campus')

    # Determine the associated campuses based on the logged-in campus
    if session_campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif session_campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        # For any other campus, include only that campus
        associated_campuses = [session_campus]

    # Get filter parameters
    year_filter = request.args.get('year')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Base SQL query with campus association filtering
        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM tblflight WHERE Campus IN ({placeholders})"
        params = associated_campuses[:]

        if year_filter:
            sql += " AND Year = %s"
            params.append(year_filter)

        cursor.execute(sql, params)
        records = cursor.fetchall()

        return jsonify(records)  # Return data as JSON

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        conn.close()




@app.route('/delete_flight/<int:ID>', methods=['DELETE'])
def delete_flight(ID):  # Match the parameter name with the route parameter
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tblflight WHERE ID = %s", (ID,))  # Use `ID` as per your database column name
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)  # Success response
    except Exception as e:
        print("Error:", e)
        return jsonify(success=False, error=str(e))  # Failure response with error message



# Function to determine the emission factor based on country and travel type
def get_factor(country, local_or_international):
    country_factors = {
        "Philippines": 66.54, "Australia": 51.47,
        "Argentina": 77.08, "Armenia": 77.08, "Aruba": 77.08,
        "Bahamas": 18.73, "Austria": 18.73, "Bahrain": 18.73, "Bangladesh": 18.73,
        "Belarus": 18.73, "Barbados": 18.73, "Belgium": 16.04, "Belize": 16.04,
        "Benin": 16.04, "Bermuda": 16.04, "Bhutan": 16.04, "Bolivia": 16.04,
        "Bosnia and Herzegovina": 16.04, "Botswana": 16.04, "Brazil": 16.77,
        "British Indian Ocean Territory": 16.77, "British Virgin Islands": 16.77,
        "Brunei": 16.77, "Bulgaria": 16.77, "Burkina Faso": 16.77, "Burundi": 16.77,
        "Cambodia": 16.77, "Cameroon": 16.77, "Canada": 23.00, "Cape Verde": 23.00,
        "Cayman Islands": 23.00, "Central African Republic": 23.00, "Chad": 23.00,
        "Chile": 38.50, "China": 76.74, "Christmas Island": 76.74, "Cocos Islands": 76.74,
        "Colombia": 18.69, "Comoros": 18.69, "Cook Islands": 18.69, "Costa Rica": 11.10,
        "Croatia": 11.10, "Cuba": 11.10, "Curacao": 11.10, "Cyprus": 11.10,
        "Czech Republic": 53.04, "Democratic Republic of the Congo": 53.04, "Denmark": 53.04,
        "Djibouti": 53.04, "Dominica": 53.04, "East Timor": 53.04, "Ecuador": 53.04,
        "Egypt": 65.38, "El Salvador": 65.38, "Equatorial Guinea": 65.38, "Eritrea": 65.38,
        "Estonia": 65.38, "Ethiopia": 65.38, "Falkland Islands": 65.38, "Faroe Islands": 65.38,
        "Fiji": 48.99, "Finland": 48.99, "France": 8.01, "French Polynesia": 8.01,
        "Gabon": 8.01, "Gambia": 8.01, "Georgia": 8.01, "Germany": 22.57, "Ghana": 22.57,
        "Gibraltar": 22.57, "Greece": 56.63, "Greenland": 56.63, "Grenada": 56.63,
        "Guam": 56.63, "Guernsey": 56.63, "Guinea": 56.63, "Guyana": 56.63,
        "Guinea-Bissau": 56.63, "Haiti": 56.63, "Honduras": 56.63, "Hong Kong": 56.63,
        "Hungary": 84.43, "Iceland": 84.43, "India": 93.20, "Indonesia": 110.37,
        "Iran": 110.37, "Iraq": 110.37, "Ireland": 31.78, "Isle of Man": 31.78,
        "Israel": 72.60, "Italy": 26.20, "Ivory Coast": 26.20, "Jamaica": 26.20,
        "Japan": 81.86, "Jersey": 81.86, "Jordan": 80.48, "Kazakhstan": 80.48,
        "Kenya": 80.48, "Kiribati": 80.48, "Kosovo": 85.19, "Kuwait": 85.19,
        "Kyrgyzstan": 85.19, "Laos": 85.19, "Latvia": 85.19, "Lebanon": 85.19,
        "Lesotho": 85.19, "Liberia": 85.19, "Libya": 85.19, "Liechtenstein": 85.19,
        "Lithuania": 85.19, "Luxembourg": 85.19, "Macau": 85.19, "Macedonia": 109.01,
        "Madagascar": 109.01, "Malaysia": 95.94, "Maldives": 218.68, "Mali": 218.68,
        "Malta": 218.68, "Marshall Island": 218.68, "Mauritania": 218.68, "Mauritius": 218.68,
        "Mayotte": 218.68, "Mexico": 30.52, "Micronesia": 30.52, "Moldova": 30.52,
        "Monaco": 30.52, "Montenegro": 30.52, "Mongolia": 30.52, "Montserrat": 30.52,
        "Morocco": 30.52, "Mozambique": 30.52, "Myanmar": 30.52, "Namibia": 30.52,
        "Nauru": 30.52, "Nepal": 30.52, "Netherlands": 23.78, "New Caledonia": 23.78,
        "Netherlands Antilles": 23.78, "New Zealand": 11.57, "Nicaragua": 11.57,
        "Niger": 11.57, "Niue": 11.57, "Nigeria": 11.57, "North Korea": 11.57,
        "Northern Mariana Islands": 11.57, "Norway": 11.57, "Oman": 11.57, "Pakistan": 11.57,
        "Palau": 11.57, "Palestine": 11.57, "Panama": 31.72, "Papua New Guinea": 31.72,
        "Paraguay": 31.72, "Peru": 31.72, "Pitcairn": 66.54, "Poland": 39.12,
        "Portugal": 36.47, "Qatar": 165.18, "Republic of the Congo": 165.18, "Reunion": 165.18,
        "Romania": 34.16, "Russia": 34.16, "Rwanda": 37.98, "Saint Barthelemy": 37.98,
        "Saint Helena": 37.98, "Saint Kitts and Nevis": 37.98, "Saint Lucia": 37.98,
        "Saint Martin": 37.98, "Saint Pierre and Miquelon": 37.98, "Saint Vincent and the Grenadines": 37.98,
        "Samoa": 37.98, "San Marino": 37.98, "Sao Tome and Principe": 37.98, "Saudi Arabia": 156.64,
        "Senegal": 156.64, "Serbia": 156.64, "Seychelles": 156.64, "Sierra Leone": 156.64,
        "Singapore": 51.33, "Sint Maarten": 51.33, "Slovakia": 21.34, "Slovenia": 21.34,
        "Solomon Islands": 21.34, "Somalia": 21.34, "South Africa": 82.36, "South Korea": 82.36,
        "South Sudan": 82.36, "Spain": 20.07, "Sri Lanka": 20.07, "Sudan": 20.07,
        "Suriname": 20.07, "Svalbard and Jan Mayen": 20.07, "Swaziland": 20.07,
        "Sweden": 20.07, "Switzerland": 10.75, "Syria": 10.75, "Taiwan": 10.75,
        "Tajikistan": 117.82, "Tanzania": 117.82, "Thailand": 59.05, "Togo": 59.05,
        "Tokelau": 59.05, "Tonga": 59.05, "Trinidad and Tobago": 59.05, "Tunisia": 59.05,
        "Turkey": 41.77, "Turkmenistan": 41.77, "Turks and Caicos Islands": 41.77,
        "Tuvalu": 41.77, "U.S. Virgin Islands": 41.77, "Uganda": 41.77, "Ukraine": 41.77,
        "United Arab Emirates": 145.46, "United Kingdom": 18.41, "United States": 23.04,
        "Uruguay": 23.04, "Uzbekistan": 23.04, "Vanuatu": 23.04, "Vatican": 23.04,
        "Venezuela": 23.04, "Vietnam": 60.12, "Wallis and Futuna": 60.12, "Western Sahara": 60.12,
        "Yemen": 60.12, "Zambia": 60.12, "Zimbabwe": 60.12
    }
    return country_factors.get(country, 0)

@app.route('/accommodation', methods=['GET', 'POST'])
def accommodation():
    # Ensure user is logged in
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Get the logged-in campus from the session
    session_campus = session.get('campus', '')

    # Determine associated campuses for specific campuses
    if session_campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif session_campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [session_campus]

    # Retrieve filters from request arguments
    selected_year = request.args.get('year')
    selected_office = request.args.get('office')

    # Pagination variables
    current_page = request.args.get('page', 1, type=int)
    per_page = 20  # Number of records per page

    if request.method == 'POST':
        # Retrieve form data, including the specific campus from the form
        campus = request.form.get('campus')  # Use campus from form input instead of session
        office = request.form.get('officeDepartment')
        year = request.form.get('year')
        traveller_name = request.form.get('travellerName')
        event_name = request.form.get('eventName')
        travel_date_from = request.form.get('travelDateFrom')
        travel_date_to = request.form.get('travelDateTo')
        country = request.form.get('country')
        local_or_international = request.form.get('localOrInternational')
        occupied_rooms = float(request.form.get('occupiedRooms'))
        nights_per_room = float(request.form.get('nightsPerRoom'))

        # Calculate emissions based on country
        factor = get_factor(country, local_or_international)
        kg_co2 = occupied_rooms * nights_per_room * factor
        t_co2 = kg_co2 / 1000

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert data into the database
            sql = """INSERT INTO tblaccommodation (Campus, Office, YearTransact, TravellerName, TravelPurpose, 
                     TravelDateFrom, TravelDateTo, Country, TravelType, NumOccupiedRoom, NumNightPerRoom, Factor, 
                     GHGEmissionKGC02e, GHGEmissionTC02e)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (campus, office, year, traveller_name, event_name, travel_date_from, travel_date_to, 
                                 country, local_or_international, occupied_rooms, nights_per_room, factor, kg_co2, t_co2))
            conn.commit()

            flash("Accommodation emission record added successfully!", "success")

        except mysql.connector.Error as e:
            flash(f"Database error: {e}", "danger")

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

        return redirect(url_for('accommodation'))

    # For GET requests, fetch paginated accommodation data with optional filters
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Create SQL query with dynamic placeholders for associated campuses
        placeholders = ', '.join(['%s'] * len(associated_campuses))
        query = f"SELECT * FROM tblaccommodation WHERE Campus IN ({placeholders})"
        params = associated_campuses

        if selected_year:
            query += " AND YearTransact = %s"
            params.append(selected_year)
        if selected_office:
            query += " AND Office = %s"
            params.append(selected_office)

        # Get total count for pagination
        count_query = f"SELECT COUNT(*) AS total FROM tblaccommodation WHERE Campus IN ({placeholders})"
        count_params = associated_campuses[:]

        if selected_year:
            count_query += " AND YearTransact = %s"
            count_params.append(selected_year)
        if selected_office:
            count_query += " AND Office = %s"
            count_params.append(selected_office)

        cursor.execute(count_query, count_params)
        total_records = cursor.fetchone()['total']
        total_pages = (total_records + per_page - 1) // per_page

        # Add LIMIT and OFFSET for pagination
        offset = (current_page - 1) * per_page
        query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

        cursor.execute(query, params)
        accommodation_data = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", 'danger')
        accommodation_data = []
        total_pages = 1  # Default to 1 page if there's an error

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

    # Render the template with filtering and pagination data
    return render_template('accommodation.html',
                           accommodation_data=accommodation_data,
                           current_page=current_page,
                           total_pages=total_pages,
                           selected_year=selected_year,
                           selected_office=selected_office)

@app.route('/accommodation/all', methods=['GET'])
def get_all_accommodation_data():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))
    
    session_campus = session.get('campus', '')

    # Determine associated campuses
    if session_campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif session_campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [session_campus]

    year_filter = request.args.get('year', '')
    office_filter = request.args.get('office', '')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Base SQL query
        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM tblaccommodation WHERE Campus IN ({placeholders})"
        params = associated_campuses

        # Apply filters if present
        if year_filter:
            sql += " AND YearTransact = %s"
            params.append(year_filter)
        if office_filter:
            sql += " AND Office = %s"
            params.append(office_filter)

        cursor.execute(sql, params)
        accommodation_data = cursor.fetchall()

        return jsonify(accommodation_data)  # Return data as JSON for use in JavaScript

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)})

    finally:
        cursor.close()
        conn.close()



@app.route('/accommodation/print', methods=['GET'])
def print_accommodation():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))
    
    campus = session.get('campus', '')
    year_filter = request.args.get('year')
    office_filter = request.args.get('office')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Base SQL query
        sql = "SELECT * FROM tblaccommodation WHERE Campus = %s"
        params = [campus]
        
        # Add filters if present
        if year_filter:
            sql += " AND YearTransact = %s"
            params.append(year_filter)
        if office_filter:
            sql += " AND Office = %s"
            params.append(office_filter)
        
        cursor.execute(sql, params)
        data = cursor.fetchall()
        
        return jsonify(data)  # Return the data as JSON
    
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)})
    
    finally:
        cursor.close()
        conn.close()

@app.route('/accommodation/download', methods=['GET'])
def download_accommodation_data():
    if 'loggedIn' not in session:
        return jsonify({"error": "User not logged in"}), 401

    campus = session.get('campus', '')
    year_filter = request.args.get('year')
    office_filter = request.args.get('office')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Base SQL query
        sql = "SELECT * FROM tblaccommodation WHERE Campus = %s"
        params = [campus]

        # Add filters if present
        if year_filter:
            sql += " AND YearTransact = %s"
            params.append(year_filter)
        if office_filter:
            sql += " AND Office = %s"
            params.append(office_filter)

        cursor.execute(sql, params)
        data = cursor.fetchall()

        return jsonify(data)  # Return data as JSON for download

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)})

    finally:
        cursor.close()
        conn.close()

@app.route('/accommodation/delete/<int:id>', methods=['DELETE'])
def delete_accommodation(id):
    # Ensure the user is logged in
    if 'loggedIn' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete the accommodation record with the specified ID
        sql = "DELETE FROM tblaccommodation WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()

        if cursor.rowcount > 0:
            response = {'success': True, 'message': 'Record deleted successfully'}
        else:
            response = {'success': False, 'message': 'Record not found'}

    except mysql.connector.Error as e:
        response = {'success': False, 'message': str(e)}

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

    return jsonify(response)
from datetime import datetime

from datetime import datetime

from datetime import datetime
from datetime import datetime

from datetime import datetime


@app.route('/procurement_dashboard')
def procurement_dashboard():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    selected_campus = request.args.get('campus', 'all')
    selected_year = int(request.args.get('year', datetime.now().year))
    selected_month = request.args.get('month', None)
    current_year = datetime.now().year

    # Initialize data lists for emissions (remove unused data)
    food_waste_data = [0] * 12
    lpg_data = [0] * 12

    current_emission_data = {
        "food_waste": 0,
        "lpg": 0,
    }

    month_to_index = {
        "January": 0, "February": 1, "March": 2, "April": 3, "May": 4, "June": 5,
        "July": 6, "August": 7, "September": 8, "October": 9, "November": 10, "December": 11
    }

    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Could not establish database connection.")

        cursor = conn.cursor(dictionary=True)

        # Queries for other data
        queries = [
            ("SELECT Month, SUM(GHGEmissionKGCO2e) AS total_emission FROM tblfoodwaste WHERE (%s = 'all' OR campus = %s) AND YearTransaction = %s GROUP BY Month", food_waste_data, "food_waste"),
            ("SELECT Month, SUM(GHGEmissionKGCO2e) AS total_emission FROM tbllpg WHERE (%s = 'all' OR campus = %s) AND YearTransact = %s GROUP BY Month", lpg_data, "lpg"),
        ]

        for query, data_list, category in queries:
            cursor.execute(query, (selected_campus, selected_campus, selected_year))
            for row in cursor.fetchall():
                month_index = month_to_index.get(row.get('Month'), -1)
                if month_index != -1:
                    emission_value = row.get('total_emission')
                    if emission_value is not None:
                        data_list[month_index] = float(emission_value)
                        current_emission_data[category] += float(emission_value)

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Forecast function using Prophet
    def forecast_prophet(data, periods):
        if all(v == 0 for v in data):  # Check if all data is zero
            return [0] * periods, 0  # Return a list of zeros with no R2 score

        try:
            df = pd.DataFrame({'ds': pd.date_range(start='2023-01-01', periods=len(data), freq='M'), 'y': data})
            df = df[df['y'] > 0]  # Only use non-zero data for modeling

            # Initialize Prophet model and fit data
            model = Prophet(yearly_seasonality=True)
            model.fit(df)

            # Make future predictions
            future = model.make_future_dataframe(periods=periods, freq='M')
            forecast = model.predict(future)

            # Calculate the R2 score for the training data
            r2 = r2_score(df['y'], model.predict(df)['yhat'])

            # Return the forecast and R2 score
            return forecast['yhat'][-periods:].tolist(), r2
        except Exception as e:
            flash(f"Forecast Error: {e}", "danger")
            return [0] * periods, 0

    forecast_data = {
        "food_waste_forecast": {
            "prophet": {
                "forecast": forecast_prophet(food_waste_data, periods=12)[0],  # Forecast data for 12 months
                "r2_score": forecast_prophet(food_waste_data, periods=12)[1],   # R2 score
            }
        },
        "lpg_forecast": {
            "prophet": {
                "forecast": forecast_prophet(lpg_data, periods=12)[0],  # Forecast data for 12 months
                "r2_score": forecast_prophet(lpg_data, periods=12)[1],   # R2 score
            }
        },
    }

    # Print R² scores for validation
    for key, value in forecast_data.items():
        print(f"{key.replace('_forecast', '').title()} Prophet R² Score:", value["prophet"]["r2_score"])

    # Month labels
    def get_month_labels(start_month, start_year, total_months):
        return [f"{(start_month + i) % 12 + 1:02d}/{(start_year + (start_month + i) // 12) % 100:02d}" for i in range(total_months)]

    labels = get_month_labels(0, selected_year, 12)

    # Render the template with forecast data
    return render_template(
        'procurement_dashboard.html',
        food_waste_data=food_waste_data,
        lpg_data=lpg_data,
        forecast_data=forecast_data,
        current_emission_data=current_emission_data,
        selected_year=selected_year,
        current_year=current_year,
        labels=labels
    )




@app.route('/pro_report', methods=['GET'])
def pro_report():
    # Retrieve campus from session
    campus = session.get('campus', '')

    # Redirect if no campus is found in the session
    if not campus:
        return redirect(url_for('login'))

    # Default values for pagination
    items_per_page = 15
    current_page_food_waste = int(request.args.get('foodWaste_page', 1))
    current_page_lpg = int(request.args.get('lpg_page', 1))

    try:
        # Connect to the database and create a cursor
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Query data from tblfoodwaste with pagination
        cursor.execute("SELECT COUNT(*) AS count FROM tblfoodwaste WHERE Campus = %s", (campus,))
        total_items_food_waste = cursor.fetchone()['count']
        total_pages_food_waste = (total_items_food_waste + items_per_page - 1) // items_per_page  # Ceiling division
        offset_food_waste = (current_page_food_waste - 1) * items_per_page
        
        cursor.execute("SELECT * FROM tblfoodwaste WHERE Campus = %s LIMIT %s OFFSET %s", (campus, items_per_page, offset_food_waste))
        result_food_waste = cursor.fetchall()

        # Query data from tbllpg with pagination
        cursor.execute("SELECT COUNT(*) AS count FROM tbllpg WHERE Campus = %s", (campus,))
        total_items_lpg = cursor.fetchone()['count']
        total_pages_lpg = (total_items_lpg + items_per_page - 1) // items_per_page  # Ceiling division
        offset_lpg = (current_page_lpg - 1) * items_per_page

        cursor.execute("SELECT * FROM tbllpg WHERE Campus = %s LIMIT %s OFFSET %s", (campus, items_per_page, offset_lpg))
        result_lpg = cursor.fetchall()

    except Exception as e:
        # Handle the error (you can log it or flash a message)
        print(f"Database error: {e}")
        result_food_waste = []
        result_lpg = []

    finally:
        cursor.close()
        conn.close()

    # Pass the queried data and pagination info to the template
    return render_template(
        'pro_report.html',
        campus=campus,
        result_food_waste=result_food_waste,
        total_pages_food_waste=total_pages_food_waste,
        current_page_food_waste=current_page_food_waste,
        result_lpg=result_lpg,
        total_pages_lpg=total_pages_lpg,
        current_page_lpg=current_page_lpg
    )


# Route to handle food consumption form submission and display
@app.route('/food_consumption', methods=['GET', 'POST'])
def food_consumption():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    campus = session.get('campus')  # Get the logged-in campus

    # Determine associated campuses based on the logged-in campus
    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        # For any other campus, include only that campus
        associated_campuses = [campus]

    # Pagination variables
    page_size = 15  # Number of records per page
    current_page = int(request.args.get('page', 1))  # Current page number from the query parameter
    offset = (current_page - 1) * page_size  # Offset for SQL query

    # Get filter parameters from the query string
    selected_year = request.args.get('year', None)
    selected_month = request.args.get('month', None)
    selected_office = request.args.get('office', None)

    if request.method == 'POST':
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Gather form data, including the specific campus from the form
            campus = request.form.get('campus')  # Get campus from the form input
            year = request.form.get('year')
            month = request.form.get('month')
            office = request.form.get('office')
            food_type = request.form.get('foodType')
            servings = float(request.form.get('servings'))

            # Food type emission factors
            food_factors = {
                "1 Standard Breakfast": 0.84,
                "1 Gourmet Breakfast": 2.33,
                "1 Hot Snack (burger and fries)": 2.77,
                "1 Cold or Hot Snack": 2.02,
                "1 Sandwich": 1.27,
                "1 Average Meal": 4.70,
                "Meal,Vegan": 1.69,
                "Meal,Vegetarian": 2.85,
                "Meal with Beef": 6.93,
                "Meal with Chicken": 3.39
            }

            # Calculate emissions
            factor = food_factors.get(food_type, 0)
            kgCO2e = servings * factor
            tCO2e = kgCO2e / 1000

            # Insert data into the database with the specific campus selected in the form
            cursor.execute("""INSERT INTO tblfoodwaste 
                              (Campus, YearTransaction, Month, Office, TypeOfFoodServed, QuantityOfServing, GHGEmissionKGCO2e, GHGEmissionTCO2e)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                           (campus, year, month, office, food_type, servings, kgCO2e, tCO2e))
            conn.commit()

            flash("Food consumption record added successfully.", "success")

        except mysql.connector.Error as e:
            flash(f"Database Error: {e}", 'danger')

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('food_consumption'))  # Redirect to the same page after submission

    # Fetch existing food data for the associated campuses with pagination and filters
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Base SQL query for fetching records with campus association
        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM tblfoodwaste WHERE Campus IN ({placeholders})"
        params = associated_campuses

        # Apply filters if they are provided
        if selected_year:
            sql += " AND YearTransaction = %s"
            params.append(selected_year)
        if selected_month:
            sql += " AND Month = %s"
            params.append(selected_month)
        if selected_office:
            sql += " AND Office = %s"
            params.append(selected_office)

        # Count total records for pagination
        count_sql = f"SELECT COUNT(*) AS total FROM ({sql}) AS filtered"
        cursor.execute(count_sql, params)
        total_records = cursor.fetchone()['total']
        total_pages = (total_records + page_size - 1) // page_size  # Calculate total pages

        # Fetch paginated food records with filters applied
        sql += " LIMIT %s OFFSET %s"
        params.extend([page_size, offset])
        cursor.execute(sql, params)
        food_data = cursor.fetchall()

        # Fetch distinct years and campuses for the filter options
        cursor.execute("SELECT DISTINCT YearTransaction FROM tblfoodwaste")
        years = [row['YearTransaction'] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT Campus FROM tblfoodwaste")
        campuses = [row['Campus'] for row in cursor.fetchall()]

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", 'danger')
        food_data, years, campuses = [], [], []
        total_pages = 1  # Default to 1 if an error occurs

    finally:
        cursor.close()
        conn.close()

    return render_template(
        'food_consumption.html',
        food_data=food_data,
        years=years,
        campuses=campuses,
        total_pages=total_pages,
        current_page=current_page,
        selected_year=selected_year,
        selected_month=selected_month,
        selected_office=selected_office
    )


@app.route('/food_consumption/all', methods=['GET'])
def food_consumption_all():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Get the logged-in campus from the session
    campus = session.get('campus')

    # Determine the associated campuses based on the logged-in campus
    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        # For any other campus, include only that campus
        associated_campuses = [campus]

    selected_month = request.args.get('month', None)
    selected_office = request.args.get('office', None)
    selected_year = request.args.get('year', None)

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Build SQL query with campus association and optional filters, but no pagination
        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM tblfoodwaste WHERE Campus IN ({placeholders})"
        params = associated_campuses

        if selected_month:
            sql += " AND Month = %s"
            params.append(selected_month)
        if selected_office:
            sql += " AND Office = %s"
            params.append(selected_office)
        if selected_year:
            sql += " AND YearTransaction = %s"
            params.append(selected_year)

        # Execute query to fetch all records
        cursor.execute(sql, params)
        all_food_reports = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        all_food_reports = []

    finally:
        cursor.close()
        conn.close()

    # Return data as JSON
    return jsonify(all_food_reports)






# Route to delete a food record by ID
@app.route('/delete_food_record/<int:record_id>', methods=['DELETE'])
def delete_food_record(record_id):
    if 'loggedIn' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete the record from the database by ID
        cursor.execute("DELETE FROM tblfoodwaste WHERE id = %s", (record_id,))
        conn.commit()

        # Check if a row was actually deleted
        if cursor.rowcount == 0:
            return jsonify({"success": False, "message": "Record not found"}), 404

        return jsonify({"success": True}), 200

    except mysql.connector.Error as e:
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/lpg_consumption', methods=['GET', 'POST'])
def lpg_consumption():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Get the logged-in campus from the session
    session_campus = session.get('campus')

    # Determine associated campuses for specific campuses
    if session_campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif session_campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [session_campus]

    items_per_page = 15
    current_page = request.args.get('page', 1, type=int)

    # Get filter parameters from the request
    selected_year = request.args.get('year')
    selected_month = request.args.get('month')
    selected_office = request.args.get('office')

    if request.method == 'POST':
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Gather form data, including the specific campus from the form
            campus = request.form.get('campus')  # Use campus from form input instead of session
            year = request.form.get('year')
            month = request.form.get('month')
            office = request.form.get('office')
            concessionaires = request.form.get('concessionaires')
            qty = float(request.form.get('qty'))
            tank_weight = float(request.form.get('tankWeight'))

            # Calculation logic
            factor = 2.95795 if concessionaires in ['Fuel', 'Diesel'] else 0
            tank_volume = 1.96 * tank_weight
            total_tank_vol = qty * tank_volume
            kgCO2e = factor * tank_weight
            tCO2e = kgCO2e / 1000

            # Insert into database
            cursor.execute("""INSERT INTO tbllpg (Campus, YearTransact, Month, Office, ConcessionariesType, TankQuantity, TankWeight, TankVolume, TotalTankVolume, GHGEmissionKGCO2e, GHGEmissionTCO2e)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                           (campus, year, month, office, concessionaires, qty, tank_weight, tank_volume, total_tank_vol, kgCO2e, tCO2e))
            conn.commit()

            flash("LPG consumption record added successfully.", "success")

        except mysql.connector.Error as e:
            flash(f"Database Error: {e}", 'danger')

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('lpg_consumption'))

    # Fetch existing LPG data for associated campuses with pagination and filtering
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Create SQL query with dynamic placeholders for associated campuses
        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM tbllpg WHERE Campus IN ({placeholders})"
        params = associated_campuses

        # Add filters to the query if they are provided
        if selected_year:
            sql += " AND YearTransact = %s"
            params.append(selected_year)
        if selected_month:
            sql += " AND Month = %s"
            params.append(selected_month)
        if selected_office:
            sql += " AND Office = %s"
            params.append(selected_office)

        # Fetch total record count for pagination calculation
        count_query = f"SELECT COUNT(*) as count FROM ({sql}) AS filtered"
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()['count']

        # Calculate total pages
        total_pages = (total_count + items_per_page - 1) // items_per_page

        # Offset calculation for current page
        offset = (current_page - 1) * items_per_page

        # Fetch data for the current page with LIMIT and OFFSET
        sql += " LIMIT %s OFFSET %s"
        params.extend([items_per_page, offset])
        cursor.execute(sql, params)
        lpg_data = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        lpg_data, total_pages = [], 1

    finally:
        cursor.close()
        conn.close()

    # Render the template with pagination and filtering information
    return render_template(
        'lpg_consumption.html', 
        lpg_data=lpg_data, 
        current_page=current_page, 
        total_pages=total_pages,
        selected_year=selected_year,
        selected_month=selected_month,
        selected_office=selected_office
    )

@app.route('/lpg_consumption/all', methods=['GET'])
def lpg_consumption_all():
    if 'loggedIn' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    session_campus = session.get('campus')

    # Determine associated campuses
    if session_campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif session_campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [session_campus]

    selected_year = request.args.get('year')
    selected_month = request.args.get('month')
    selected_office = request.args.get('office')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM tbllpg WHERE Campus IN ({placeholders})"
        params = associated_campuses

        if selected_year:
            sql += " AND YearTransact = %s"
            params.append(selected_year)
        if selected_month:
            sql += " AND Month = %s"
            params.append(selected_month)
        if selected_office:
            sql += " AND Office = %s"
            params.append(selected_office)

        cursor.execute(sql, params)
        all_lpg_data = cursor.fetchall()

    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

    return jsonify(all_lpg_data)




@app.route('/delete_lpg/<int:id>', methods=['DELETE'])
def delete_lpg(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbllpg WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)  # Success response
    except Exception as e:
        print("Error:", e)
        return jsonify(success=False)  # Failure response



# Route for the accommodation report
@app.route('/ea_report', methods=['GET'])
def ea_report():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))
    
    campus = session.get('campus', '')
    if not campus:
        flash("Campus information is missing. Please contact support.", "danger")
        return redirect(url_for('external_dashboard'))

    years = [str(year) for year in range(2020, 2025)]
    selected_year = request.args.get('year')
    selected_office = request.args.get('office')
    flight_page = int(request.args.get('flight_page', 1))
    accommodation_page = int(request.args.get('accommodation_page', 1))
    per_page = 10

    try:
        conn = get_db_connection()
        cursor_offices = conn.cursor(dictionary=True)
        cursor_flight = conn.cursor(dictionary=True)
        cursor_accommodation = conn.cursor(dictionary=True)

        # Fetch unique offices based on campus
        cursor_offices.execute("SELECT DISTINCT Office FROM tblflight WHERE Campus = %s", (campus,))
        offices = [row['Office'] for row in cursor_offices.fetchall()]

        # Base queries
        flight_query = "SELECT * FROM tblflight WHERE Campus = %s"
        accommodation_query = "SELECT * FROM tblaccommodation WHERE Campus = %s"
        params = [campus]

        # Apply year and office filters if selected
        if selected_year:
            flight_query += " AND Year = %s"
            accommodation_query += " AND YearTransact = %s"
            params.append(selected_year)

        if selected_office:
            flight_query += " AND Office = %s"
            accommodation_query += " AND Office = %s"
            params.append(selected_office)

        # Fetch total records for pagination
        cursor_flight.execute(flight_query, params)
        total_flight_records = cursor_flight.rowcount
        cursor_flight.fetchall()  # Clear fetched data for pagination query

        cursor_accommodation.execute(accommodation_query, params)
        total_accommodation_records = cursor_accommodation.rowcount
        cursor_accommodation.fetchall()  # Clear fetched data for pagination query

        # Apply pagination to the main query
        flight_query += " LIMIT %s OFFSET %s"
        accommodation_query += " LIMIT %s OFFSET %s"
        flight_offset = (flight_page - 1) * per_page
        accommodation_offset = (accommodation_page - 1) * per_page

        cursor_flight.execute(flight_query, params + [per_page, flight_offset])
        flight_data = cursor_flight.fetchall()

        cursor_accommodation.execute(accommodation_query, params + [per_page, accommodation_offset])
        accommodation_data = cursor_accommodation.fetchall()

        total_flight_pages = (total_flight_records + per_page - 1) // per_page
        total_accommodation_pages = (total_accommodation_records + per_page - 1) // per_page

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", 'danger')
        flight_data = []
        accommodation_data = []
        total_flight_pages = 0
        total_accommodation_pages = 0

    finally:
        cursor_offices.close()
        cursor_flight.close()
        cursor_accommodation.close()
        conn.close()

    # Render template with year and office filtering
    return render_template(
        'ea_report.html', 
        flight_data=flight_data,
        accommodation_data=accommodation_data,
        years=years,
        offices=offices,
        selected_year=selected_year,
        selected_office=selected_office,
        pagination_info={
            'flight_data': {
                'current_page': flight_page,
                'total_pages': total_flight_pages
            },
            'accommodation_data': {
                'current_page': accommodation_page,
                'total_pages': total_accommodation_pages
            }
        }
    )

@app.route('/download_excel', methods=['GET'])
def download_excel():
    # Get the parameters from the request
    year = request.args.get('year')
    consumption_type = request.args.get('consumption_type')

    # Determine the data source based on the consumption type
    if consumption_type == 'flightData':
        query = "SELECT * FROM flight_table"  # Replace 'flight_table' with your actual table name
    elif consumption_type == 'accommodationData':
        query = "SELECT * FROM accommodation_table"  # Replace 'accommodation_table' with your actual table name
    else:
        return jsonify({"error": "Invalid consumption type"}), 400

    try:
        # Connect to the database and fetch the data
        conn = get_db_connection()  # Replace with your database connection function
        df = pd.read_sql(query, conn)

        # Filter data by year if applicable
        if year:
            df = df[df['Year'] == int(year)]

        # Create an Excel file in memory
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Report', index=False)
        writer.save()
        output.seek(0)

        # Send the file to the client
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                         download_name=f'{consumption_type}_report.xlsx', as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()



@app.route('/user_dashboard')
def user_dashboard():
    return "User Dashboard"

# Route for logout
@app.route('/logout')
def logout():
    session.pop('loggedIn', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
