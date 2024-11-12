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

# Route for the EMU dashboard
@app.route('/emu')
def emu_dashboard():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Retrieve the campus from session, default to 'default_campus' if not set
    campus = session.get('campus', 'default_campus')

    # Initialize report and emission data
    electricity_data = []
    fuel_data = []
    waste_segregation_data = []
    waste_unsegregation_data = []
    treated_water_data = []
    water_data = []
    current_emission_data = {"electricity": 0, "fuel": 0, "water": 0}  # Store current emissions

    try:
        # Establish database connection
        conn = get_db_connection()
        if conn is None:
            raise Error("Could not establish database connection.")
        
        cursor = conn.cursor(dictionary=True)

        # Fetch data for the specific campus
        cursor.execute("SELECT consumption FROM electricity_consumption WHERE campus = %s", (campus,))
        electricity_data = [float(row['consumption']) for row in cursor.fetchall()]

        cursor.execute("SELECT total_emission FROM fuel_emissions WHERE campus = %s", (campus,))
        fuel_data = [float(row['total_emission']) for row in cursor.fetchall()]

        cursor.execute("SELECT QuantityInKG FROM tblsolidwastesegregated WHERE Campus = %s", (campus,))
        waste_segregation_data = [float(row['QuantityInKG']) for row in cursor.fetchall()]

        cursor.execute("SELECT QuantityInKG FROM tblsolidwasteunsegregated WHERE Campus = %s", (campus,))
        waste_unsegregation_data = [float(row['QuantityInKG']) for row in cursor.fetchall()]

        cursor.execute("SELECT TreatedWaterVolume FROM tbltreatedwater WHERE Campus = %s", (campus,))
        treated_water_data = [float(row['TreatedWaterVolume']) for row in cursor.fetchall()]

        cursor.execute("SELECT Consumption FROM tblwater WHERE Campus = %s", (campus,))
        water_data = [float(row['Consumption']) for row in cursor.fetchall()]

        # Fetch current emissions for each type and convert to float
        cursor.execute("SELECT current_emission FROM electricity_emissions WHERE campus = %s ORDER BY date DESC LIMIT 1", (campus,))
        current_emission_data["electricity"] = float(cursor.fetchone()['current_emission']) if cursor.rowcount else 0

        cursor.execute("SELECT current_emission FROM fuel_emissions WHERE campus = %s ORDER BY date DESC LIMIT 1", (campus,))
        current_emission_data["fuel"] = float(cursor.fetchone()['current_emission']) if cursor.rowcount else 0

        cursor.execute("SELECT current_emission FROM water_emissions WHERE campus = %s ORDER BY date DESC LIMIT 1", (campus,))
        current_emission_data["water"] = float(cursor.fetchone()['current_emission']) if cursor.rowcount else 0

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        print(f"Database Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Compute the total emissions across all categories
    total_emission = (
        float(current_emission_data["electricity"]) +
        float(current_emission_data["fuel"]) +
        float(current_emission_data["water"]) +
        float(waste_segregation_data[-1] if waste_segregation_data else 0) +
        float(waste_unsegregation_data[-1] if waste_unsegregation_data else 0) +
        float(treated_water_data[-1] if treated_water_data else 0) +
        float(water_data[-1] if water_data else 0)
    )

    # Function to forecast using ARIMA
    def forecast_consumption(data, periods=14):  # Forecast for the next 14 periods
        if len(data) > 0:
            try:
                data = np.array(data, dtype=float)  # Ensure data is numeric
                model = ARIMA(data, order=(5, 1, 0))
                model_fit = model.fit()
                forecast = model_fit.forecast(steps=periods)
                return forecast.tolist()
            except Exception as e:
                flash(f"ARIMA Error: {e}", "danger")
                print(f"ARIMA Error: {e}")
                return [0] * periods
        else:
            return [0] * periods

    # Forecast data for all parameters
    forecast_data = {
        "electricity_forecast": forecast_consumption(electricity_data),
        "fuel_forecast": forecast_consumption(fuel_data),
        "waste_segregation_forecast": forecast_consumption(waste_segregation_data),
        "waste_unsegregation_forecast": forecast_consumption(waste_unsegregation_data),
        "treated_water_forecast": forecast_consumption(treated_water_data),
        "water_forecast": forecast_consumption(water_data),
    }

    # Print forecast data for debugging
    print("Forecast Data for Campus:", campus, forecast_data)
    print("Current Emission Data:", current_emission_data)
    print("Total Emission:", total_emission)

    # Render the template and pass data
    return render_template('emu_index.html',
                           electricity_data=electricity_data,
                           fuel_data=fuel_data,
                           waste_segregation_data=waste_segregation_data,
                           waste_unsegregation_data=waste_unsegregation_data,
                           treated_water_data=treated_water_data,
                           water_data=water_data,
                           forecast_data=forecast_data,
                           current_emission_data=current_emission_data,
                           total_emission=total_emission)



# Route for Electricity Consumption
@app.route('/electricity_consumption', methods=['GET', 'POST'])
def electricity_consumption():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Get the logged-in campus from the session
    campus = session.get('campus')

    # Determine associated campuses
    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [campus]

    # Set up pagination parameters
    page = request.args.get('page', 1, type=int)  # Current page number
    per_page = 20  # Records per page
    offset = (page - 1) * per_page  # Offset for SQL

    # Get filter parameters from query string
    selected_month = request.args.get('month')
    selected_quarter = request.args.get('quarter')
    selected_year = request.args.get('year')

    results = {}  # Store calculation results if POST method

    if request.method == 'POST':
        # Handle form submission for adding electricity data
        campus = request.form.get('campus')
        category = request.form.get('category')
        month = request.form.get('month')
        quarter = request.form.get('quarter')
        year = request.form.get('year')

        try:
            prev_reading = float(request.form.get('prevReading'))
            current_reading = float(request.form.get('currentReading'))
            multiplier = float(request.form.get('multiplier'))
            total_amount = float(request.form.get('totalAmount'))

            # Calculate consumption and validate
            consumption = (current_reading - prev_reading) * multiplier
            if consumption < 0:
                flash("Consumption cannot be negative. Check your readings.", "danger")
                return redirect(url_for('electricity_consumption'))

            # Calculated metrics
            price_per_kwh = round(total_amount / consumption, 2) if consumption != 0 else 0
            kg_co2_per_kwh = round(0.7122 * consumption, 2)
            t_co2_per_kwh = round(kg_co2_per_kwh / 1000, 2)

            # Store results for display
            results = {
                'consumption': consumption,
                'price_per_kwh': price_per_kwh,
                'kg_co2_per_kwh': kg_co2_per_kwh,
                't_co2_per_kwh': t_co2_per_kwh
            }

            # Insert into database
            conn = get_db_connection()
            cursor = conn.cursor()

            sql = """
                INSERT INTO electricity_consumption 
                (campus, category, month, quarter, year, prev_reading, current_reading, multiplier, total_amount, consumption, price_per_kwh, kg_co2_per_kwh, t_co2_per_kwh)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (campus, category, month, quarter, year, prev_reading, current_reading, multiplier, total_amount, consumption, price_per_kwh, kg_co2_per_kwh, t_co2_per_kwh))
            conn.commit()

            flash("Electricity consumption record inserted successfully.", "success")

        except (ValueError, TypeError) as e:
            flash(f"Invalid input data: {e}", "danger")
        except mysql.connector.Error as e:
            flash(f"Database Error: {e}", "danger")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

        return redirect(url_for('electricity_consumption'))

    # Fetch existing data with pagination
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Build SQL query with optional filtering
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

        # Get total record count for pagination
        count_sql = f"SELECT COUNT(*) AS total FROM electricity_consumption WHERE campus IN ({placeholders})"
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
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

    return render_template(
        'electricity_consumption.html',
        reports=reports,
        current_page=page,
        total_pages=total_pages,
        selected_month=selected_month,
        selected_quarter=selected_quarter,
        selected_year=selected_year,
        results=results
    )

# Route to fetch all or filtered electricity consumption data for printing
@app.route('/electricity_consumption/all', methods=['GET'])
def electricity_consumption_all():
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
        sql = f"SELECT * FROM electricity_consumption WHERE campus IN ({placeholders})"
        params = associated_campuses

        if selected_year:
            sql += " AND year = %s"
            params.append(selected_year)

        if selected_month:
            sql += " AND month = %s"
            params.append(selected_month)

        cursor.execute(sql, params)
        records = cursor.fetchall()

        return jsonify(records)

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)})

    finally:
        cursor.close()
        conn.close()


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
    campus = session.get('campus')

    # Determine associated campuses for specific campuses
    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [campus]

    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page

    selected_month = request.args.get('month', '')

    if request.method == 'POST':
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

    campus = session.get('campus')

    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [campus]

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

        # Create SQL query with dynamic placeholders for associated campuses
        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM tblsolidwastesegregated WHERE Campus IN ({placeholders})"
        params = associated_campuses

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

        # Get total records count for pagination
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

    month_filter = request.args.get('month')
    quarter_filter = request.args.get('quarter')
    year_filter = request.args.get('year')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM tblsolidwastesegregated WHERE Campus IN ({placeholders})"
        params = associated_campuses

        if month_filter:
            sql += " AND Month = %s"
            params.append(month_filter)
        if quarter_filter:
            sql += " AND Quarter = %s"
            params.append(quarter_filter)
        if year_filter:
            sql += " AND Year = %s"
            params.append(year_filter)

        cursor.execute(sql, params)
        records = cursor.fetchall()

        return jsonify(records)

    except mysql.connector.Error as e:
        return jsonify({"error": f"Database Error: {e}"}), 500
    finally:
        cursor.close()
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

# Route for the Central Sustainable Dashboard
# Route for the Central Sustainable Dashboard
# Import additional libraries

@app.route('/csd_dashboard')
def csd_dashboard():
    if 'loggedIn' not in session:
        flash("You need to be logged in to access this page.", "warning")
        return redirect(url_for('login'))

    # Retrieve campus filter from request arguments
    selected_campus = request.args.get('campus', 'all')
    print(f"Fetching data for campus: {selected_campus}")

    # Initialize report data
    electricity_data = []
    fuel_data = []
    waste_segregation_data = []
    waste_unsegregation_data = []
    treated_water_data = []
    water_data = []
    lpg_data = []
    food_waste_data = []
    accommodation_data = []
    flight_data = []

    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Could not establish database connection.")
        
        cursor = conn.cursor(dictionary=True)

        # Function to execute campus-specific or general query
        def fetch_data(query, params=None):
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()

        # SQL queries with optional filtering by campus
        if selected_campus == 'all':
            electricity_data = fetch_data("SELECT * FROM electricity_consumption")
            fuel_data = fetch_data("SELECT * FROM fuel_emissions")
            waste_segregation_data = fetch_data("SELECT * FROM tblsolidwastesegregated")
            waste_unsegregation_data = fetch_data("SELECT * FROM tblsolidwasteunsegregated")
            treated_water_data = fetch_data("SELECT * FROM tbltreatedwater")
            water_data = fetch_data("SELECT * FROM tblwater")
            lpg_data = fetch_data("SELECT * FROM tbllpg")
            food_waste_data = fetch_data("SELECT * FROM tblfoodwaste")
            accommodation_data = fetch_data("SELECT * FROM tblaccommodation")
            flight_data = fetch_data("SELECT * FROM tblflight")
        else:
            query_filter = " WHERE campus = %s"
            electricity_data = fetch_data("SELECT * FROM electricity_consumption" + query_filter, (selected_campus,))
            fuel_data = fetch_data("SELECT * FROM fuel_emissions" + query_filter, (selected_campus,))
            waste_segregation_data = fetch_data("SELECT * FROM tblsolidwastesegregated" + query_filter, (selected_campus,))
            waste_unsegregation_data = fetch_data("SELECT * FROM tblsolidwasteunsegregated" + query_filter, (selected_campus,))
            treated_water_data = fetch_data("SELECT * FROM tbltreatedwater" + query_filter, (selected_campus,))
            water_data = fetch_data("SELECT * FROM tblwater" + query_filter, (selected_campus,))
            lpg_data = fetch_data("SELECT * FROM tbllpg" + query_filter, (selected_campus,))
            food_waste_data = fetch_data("SELECT * FROM tblfoodwaste" + query_filter, (selected_campus,))
            accommodation_data = fetch_data("SELECT * FROM tblaccommodation" + query_filter, (selected_campus,))
            flight_data = fetch_data("SELECT * FROM tblflight" + query_filter, (selected_campus,))

    except Exception as e:
        print(f"Database Error: {e}")
        flash(f"Database Error: {e}", "danger")
        return render_template("error.html", message=f"Database Error: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

    # Helper functions to extract and sum consumption values
    def get_consumption_values(data, key):
        values = [float(row[key]) for row in data if key in row and row[key] is not None]
        return values

    def calculate_total_per_office(data, key):
        return sum(get_consumption_values(data, key))

    # Calculate total consumption for each category
    overall_consumption = {
        "electricity": calculate_total_per_office(electricity_data, 'consumption'),
        "fuel": calculate_total_per_office(fuel_data, 'quantity_liters'),
        "waste_segregation": calculate_total_per_office(waste_segregation_data, 'QuantityInKG'),
        "waste_unsegregation": calculate_total_per_office(waste_unsegregation_data, 'QuantityInKG'),
        "treated_water": calculate_total_per_office(treated_water_data, 'TreatedWaterVolume'),
        "water": calculate_total_per_office(water_data, 'Consumption'),
        "lpg": calculate_total_per_office(lpg_data, 'TotalTankVolume'),
        "food_waste": calculate_total_per_office(food_waste_data, 'QuantityOfServing'),
        "accommodation": calculate_total_per_office(accommodation_data, 'NumOccupiedRoom'),
        "flight": calculate_total_per_office(flight_data, 'GHGEmissionKGC02e')
    }

    # Forecast consumption function
    def forecast_consumption(data, periods=14):
        if len(data) > 1:
            try:
                model = ARIMA(data, order=(5, 1, 0))
                model_fit = model.fit()
                forecast = model_fit.forecast(steps=periods)
                return forecast.tolist()
            except Exception as e:
                print(f"ARIMA Error: {e}")
                flash(f"ARIMA Error: {e}", "danger")
                avg_value = sum(data) / len(data)
                return [avg_value] * periods
        else:
            print("Insufficient Data for ARIMA, Returning Zeros")
            return [0] * periods

    # Generate forecasts for 14 periods
    forecast_data = {
        "electricity_forecast": forecast_consumption(get_consumption_values(electricity_data, 'consumption'), periods=14),
        "fuel_forecast": forecast_consumption(get_consumption_values(fuel_data, 'quantity_liters'), periods=14),
        "waste_segregation_forecast": forecast_consumption(get_consumption_values(waste_segregation_data, 'QuantityInKG'), periods=14),
        "waste_unsegregation_forecast": forecast_consumption(get_consumption_values(waste_unsegregation_data, 'QuantityInKG'), periods=14),
        "treated_water_forecast": forecast_consumption(get_consumption_values(treated_water_data, 'TreatedWaterVolume'), periods=14),
        "water_forecast": forecast_consumption(get_consumption_values(water_data, 'Consumption'), periods=14),
        "lpg_forecast": forecast_consumption(get_consumption_values(lpg_data, 'TotalTankVolume'), periods=14),
        "food_waste_forecast": forecast_consumption(get_consumption_values(food_waste_data, 'QuantityOfServing'), periods=14),
        "accommodation_forecast": forecast_consumption(get_consumption_values(accommodation_data, 'NumOccupiedRoom'), periods=14),
        "flight_forecast": forecast_consumption(get_consumption_values(flight_data, 'GHGEmissionKGC02e'), periods=14)
    }

    return render_template(
        'csd_dashboard.html',
        electricity_data=electricity_data,
        fuel_data=fuel_data,
        waste_segregation_data=waste_segregation_data,
        waste_unsegregation_data=waste_unsegregation_data,
        treated_water_data=treated_water_data,
        water_data=water_data,
        lpg_data=lpg_data,
        food_waste_data=food_waste_data,
        accommodation_data=accommodation_data,
        flight_data=flight_data,
        overall_consumption=overall_consumption,
        forecast_data=forecast_data,
        selected_campus=selected_campus
    )



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

    
@app.route('/sdo_dashboard')
def sdo_dashboard():
    # Check if the user is logged in by verifying the session variable
    if 'loggedIn' not in session:
        # Ensure 'login' is the correct endpoint for redirection
        return redirect(url_for('login'))  # Redirect to login if user is not logged in

    # Retrieve the campus from session and handle any missing data
    campus = session.get('campus')  # Use get to avoid KeyError if 'campus' is not set

    # Debugging: Ensure the campus is correctly identified
    print(f"Fetching data for campus: {campus}")
    
    if not campus:
        flash("Campus not set. Please log in again.", "danger")
        return redirect(url_for('login'))

    # Initialize report data
    electricity_data = []
    fuel_data = []
    waste_segregation_data = []
    waste_unsegregation_data = []
    treated_water_data = []
    water_data = []
    lpg_data = []
    food_waste_data = []
    accommodation_data = []
    flight_data = []

    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Could not establish database connection.")
        
        cursor = conn.cursor(dictionary=True)

        # Fetch data from the database
        cursor.execute("SELECT * FROM electricity_consumption WHERE campus = %s", (campus,))
        electricity_data = cursor.fetchall()

        cursor.execute("SELECT * FROM fuel_emissions WHERE campus = %s", (campus,))
        fuel_data = cursor.fetchall()

        cursor.execute("SELECT * FROM tblsolidwastesegregated WHERE Campus = %s", (campus,))
        waste_segregation_data = cursor.fetchall()

        cursor.execute("SELECT * FROM tblsolidwasteunsegregated WHERE Campus = %s", (campus,))
        waste_unsegregation_data = cursor.fetchall()

        cursor.execute("SELECT * FROM tbltreatedwater WHERE Campus = %s", (campus,))
        treated_water_data = cursor.fetchall()

        cursor.execute("SELECT * FROM tblwater WHERE Campus = %s", (campus,))
        water_data = cursor.fetchall()

        cursor.execute("SELECT * FROM tbllpg WHERE Campus = %s", (campus,))
        lpg_data = cursor.fetchall()

        cursor.execute("SELECT * FROM tblfoodwaste WHERE Campus = %s", (campus,))
        food_waste_data = cursor.fetchall()

        cursor.execute("SELECT * FROM tblaccommodation WHERE Campus = %s", (campus,))
        accommodation_data = cursor.fetchall()

        cursor.execute("SELECT * FROM tblflight WHERE Campus = %s", (campus,))
        flight_data = cursor.fetchall()

    except Exception as e:
        print(f"Database Error: {e}")  # Debugging
        flash(f"Database Error: {e}", "danger")
        return render_template("error.html", message=f"Database Error: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

    # Function to extract values and convert to float
    def get_consumption_values(data, key):
        values = [float(row[key]) for row in data if key in row and row[key] is not None]
        print(f"Extracted Values for {key}: {values}")  # Debugging
        return values

    # Function to forecast consumption using ARIMA
    def forecast_consumption(data, periods=14):
        if len(data) > 1:  # Ensure there is enough data for ARIMA
            try:
                model = ARIMA(data, order=(5, 1, 0))  # Adjust order based on data pattern
                model_fit = model.fit()
                forecast = model_fit.forecast(steps=periods)
                return forecast.tolist()
            except Exception as e:
                print(f"ARIMA Error: {e}")  # Debugging
                flash(f"ARIMA Error: {e}", "danger")
                avg_value = sum(data) / len(data)
                return [avg_value] * periods
        else:
            print("Insufficient Data for ARIMA, Returning Zeros")  # Debugging
            return [0] * periods

    # Extract values
    electricity_values = get_consumption_values(electricity_data, 'consumption')
    fuel_values = get_consumption_values(fuel_data, 'quantity_liters')
    waste_segregation_values = get_consumption_values(waste_segregation_data, 'QuantityInKG')
    waste_unsegregation_values = get_consumption_values(waste_unsegregation_data, 'QuantityInKG')
    treated_water_values = get_consumption_values(treated_water_data, 'TreatedWaterVolume')
    water_values = get_consumption_values(water_data, 'Consumption')
    lpg_values = get_consumption_values(lpg_data, 'TotalTankVolume')
    food_waste_values = get_consumption_values(food_waste_data, 'QuantityOfServing')
    accommodation_values = get_consumption_values(accommodation_data, 'NumOccupiedRoom')
    flight_values = get_consumption_values(flight_data, 'GHGEmissionKGC02e')

    # Calculate Total Emission
    total_emission = sum([
        sum(electricity_values),
        sum(fuel_values),
        sum(waste_segregation_values),
        sum(waste_unsegregation_values),
        sum(treated_water_values),
        sum(water_values),
        sum(lpg_values),
        sum(food_waste_values),
        sum(accommodation_values),
        sum(flight_values)
    ])
    print(f"Total Emission: {total_emission}")  # Debugging

    # Get Current Emission Data
    current_emission_data = {
        "electricity": electricity_values[-1] if electricity_values else 0,
        "fuel": fuel_values[-1] if fuel_values else 0,
        "waste_segregated": waste_segregation_values[-1] if waste_segregation_values else 0,
        "waste_unsegregated": waste_unsegregation_values[-1] if waste_unsegregation_values else 0,
        "treated_water": treated_water_values[-1] if treated_water_values else 0,
        "water": water_values[-1] if water_values else 0,
        "lpg": lpg_values[-1] if lpg_values else 0,
        "food_waste": food_waste_values[-1] if food_waste_values else 0,
        "accommodation": accommodation_values[-1] if accommodation_values else 0,
        "flight": flight_values[-1] if flight_values else 0
    }
    print("Current Emission Data:", current_emission_data)  # Debugging

    # Forecast data for 14 periods
    forecast_data = {
        "electricity_forecast": forecast_consumption(electricity_values, periods=14),
        "fuel_forecast": forecast_consumption(fuel_values, periods=14),
        "waste_segregation_forecast": forecast_consumption(waste_segregation_values, periods=14),
        "waste_unsegregation_forecast": forecast_consumption(waste_unsegregation_values, periods=14),
        "treated_water_forecast": forecast_consumption(treated_water_values, periods=14),
        "water_forecast": forecast_consumption(water_values, periods=14),
        "lpg_forecast": forecast_consumption(lpg_values, periods=14),
        "food_waste_forecast": forecast_consumption(food_waste_values, periods=14),
        "accommodation_forecast": forecast_consumption(accommodation_values, periods=14),
        "flight_forecast": forecast_consumption(flight_values, periods=14)
    }

    # Render the dashboard template with additional data
    return render_template(
        'sdo_dashboard.html',
        electricity_data=electricity_data,
        fuel_data=fuel_data,
        waste_segregation_data=waste_segregation_data,
        waste_unsegregation_data=waste_unsegregation_data,
        treated_water_data=treated_water_data,
        water_data=water_data,
        lpg_data=lpg_data,
        food_waste_data=food_waste_data,
        accommodation_data=accommodation_data,
        flight_data=flight_data,
        forecast_data=forecast_data,
        total_emission=total_emission,
        current_emission_data=current_emission_data
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


from decimal import Decimal
@app.route('/external_dashboard')
def external_dashboard():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in

    campus = session.get('campus', 'default_campus')  # Ensure a default campus value

    # Initialize report data
    flight_data = []
    accommodation_data = []

    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Could not establish database connection.")

        cursor = conn.cursor(dictionary=True)

        # Fetch flight emissions data for the specified campus
        cursor.execute("SELECT * FROM tblflight WHERE Campus = %s", (campus,))
        flight_data = cursor.fetchall()
        print(f"Flight Data for {campus}: {flight_data}")  # Debug output

        # Fetch accommodation emissions data for the specified campus
        cursor.execute("SELECT * FROM tblaccommodation WHERE Campus = %s", (campus,))
        accommodation_data = cursor.fetchall()
        print(f"Accommodation Data for {campus}: {accommodation_data}")  # Debug output

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        print(f"Database Error: {e}")
        # Return an error page if a database error occurs
        return render_template('error_page.html', error_message=str(e))
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

    # Function to extract values from the data
    def get_consumption_values(data, key):
        return [row[key] for row in data if key in row and row[key] is not None]

    # Function to forecast consumption using ARIMA
    def forecast_consumption(data, periods=12):
        if len(data) > 0:
            try:
                model = ARIMA(data, order=(5, 1, 0))  # Adjust the ARIMA order based on your data
                model_fit = model.fit()
                forecast = model_fit.forecast(steps=periods)
                return forecast.tolist()
            except Exception as e:
                flash(f"ARIMA Error: {e}", "danger")
                print(f"ARIMA Error: {e}")
                return [0] * periods  # Return a list of zeros instead
        else:
            return [0] * periods  # Return a list of zeros if no data is available

    # Extract values for ARIMA forecast using the correct field names
    flight_values = get_consumption_values(flight_data, 'GHGEmissionKGC02e')
    accommodation_values = get_consumption_values(accommodation_data, 'GHGEmissionKGC02e')

    # Convert flight and accommodation emissions to floats or Decimals for correct addition
    flight_values = [float(val) if isinstance(val, Decimal) else val for val in flight_values]
    accommodation_values = [float(val) if isinstance(val, Decimal) else val for val in accommodation_values]

    # Calculate total emissions
    total_flight_emissions = sum(flight_values)
    total_accommodation_emissions = sum(accommodation_values)
    total_emissions = total_flight_emissions + total_accommodation_emissions

    # Forecast data
    forecast_data = {
        "flight_forecast": forecast_consumption(flight_values),
        "accommodation_forecast": forecast_consumption(accommodation_values),
        "total_flight_emissions": total_flight_emissions,
        "total_accommodation_emissions": total_accommodation_emissions,
        "total_emissions": total_emissions
    }

    # Print forecast data for debugging
    print("Forecast Data:", forecast_data)

    # Render the template and pass data
    return render_template(
        'external_dashboard.html',
        flight_data=flight_data,
        accommodation_data=accommodation_data,
        forecast_data=forecast_data
    )

@app.route('/flight', methods=['GET', 'POST'])
def flight():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Get the logged-in campus from the session
    campus = session.get('campus')

    # Determine associated campuses for specific campuses
    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [campus]

    if request.method == 'POST':
        # Handle flight data submission
        try:
            # Extract form data
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

    # Get current page and year filter from request arguments
    current_page = int(request.args.get('page', 1))
    selected_year = request.args.get('year')

    # Build the base query for fetching flight data with associated campuses
    placeholders = ', '.join(['%s'] * len(associated_campuses))
    query = f"SELECT * FROM tblflight WHERE Campus IN ({placeholders})"
    params = associated_campuses

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

    # Count total records for pagination
    count_query = f"SELECT COUNT(*) FROM tblflight WHERE Campus IN ({placeholders})" + (" AND Year = %s" if selected_year else "")
    cursor.execute(count_query, associated_campuses + ([selected_year] if selected_year else []))
    total_records = cursor.fetchone()['COUNT(*)']
    total_pages = (total_records // limit) + (1 if total_records % limit > 0 else 0)

    cursor.close()
    conn.close()

    return render_template('flight.html', flight_data=flight_data, total_pages=total_pages, 
                           current_page=current_page, selected_year=selected_year)

@app.route('/flight/all', methods=['GET'])
def get_all_flight_data():
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

    # Get filter parameters
    year_filter = request.args.get('year')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        placeholders = ', '.join(['%s'] * len(associated_campuses))
        sql = f"SELECT * FROM tblflight WHERE Campus IN ({placeholders})"
        params = associated_campuses

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
    campus = session.get('campus', '')

    # Determine associated campuses for specific campuses
    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [campus]

    # Retrieve filters from request arguments
    selected_year = request.args.get('year')
    selected_office = request.args.get('office')

    # Pagination variables
    current_page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of records per page

    if request.method == 'POST':
        # Retrieve form data
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
        count_params = associated_campuses

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
    
    campus = session.get('campus', '')

    # Determine associated campuses
    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [campus]

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


@app.route('/procurement_dashboard')
def procurement_dashboard():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in

    campus = session.get('campus')  # Use get to avoid KeyError if 'campus' is not set

    # Initialize report data
    food_waste_data = []
    lpg_data = []
    current_emission_data = {"food": 0, "lpg": 0}
    total_emission = 0  # Initialize total emission

    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Could not establish database connection.")

        cursor = conn.cursor(dictionary=True)

        # Fetch food waste data
        if campus:  # If campus is specified, filter by campus
            cursor.execute("SELECT * FROM tblfoodwaste WHERE Campus = %s", (campus,))
        else:  # If campus is not specified, fetch all data
            cursor.execute("SELECT * FROM tblfoodwaste")
        food_waste_data = cursor.fetchall()
        print("Food Waste Data Length:", len(food_waste_data))  # Debugging

        # Fetch LPG data
        if campus:  # If campus is specified, filter by campus
            cursor.execute("SELECT * FROM tbllpg WHERE Campus = %s", (campus,))
        else:  # If campus is not specified, fetch all data
            cursor.execute("SELECT * FROM tbllpg")
        lpg_data = cursor.fetchall()
        print("LPG Data Length:", len(lpg_data))  # Debugging

        # Fetch current emissions for food waste and LPG, if available
        cursor.execute("SELECT current_emission FROM food_emissions WHERE campus = %s ORDER BY date DESC LIMIT 1", (campus,))
        current_emission_data["food"] = float(cursor.fetchone()['current_emission']) if cursor.rowcount else 0

        cursor.execute("SELECT current_emission FROM lpg_emissions WHERE campus = %s ORDER BY date DESC LIMIT 1", (campus,))
        current_emission_data["lpg"] = float(cursor.fetchone()['current_emission']) if cursor.rowcount else 0

        # Compute the total emissions across food and LPG
        total_emission = (
            float(current_emission_data["food"]) +
            float(current_emission_data["lpg"])
        )

    except Exception as e:
        print(f"Database Error: {e}")  # Debugging
        flash(f"Database Error: {e}", "danger")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

    # Function to extract values from the data
    def get_consumption_values(data, key):
        values = [float(row.get(key, 0)) for row in data if row.get(key) is not None]
        print(f"Extracted Values for {key}: {values}")  # Debugging
        return values

    # Function to forecast consumption using ARIMA
    def forecast_consumption(data, periods=14):
        if len(data) > 1:  # Ensure there is enough data for ARIMA
            try:
                model = ARIMA(data, order=(5, 1, 0))  # Adjust the ARIMA order based on your data
                model_fit = model.fit()
                forecast = model_fit.forecast(steps=periods)
                print(f"Forecast Generated: {forecast.tolist()}")  # Debugging
                return forecast.tolist()
            except Exception as e:
                print(f"ARIMA Error: {e}")  # Debugging
                flash(f"ARIMA Error: {e}", "danger")
                return [0] * periods  # Return a list of zeros instead
        else:
            print("Insufficient Data for ARIMA, Returning Zeros")  # Debugging
            return [0] * periods  # Return a list of zeros if insufficient data

    # Extract values for food waste and LPG
    food_waste_values = get_consumption_values(food_waste_data, 'QuantityOfServing')
    lpg_values = get_consumption_values(lpg_data, 'TotalTankVolume')

    # Forecast data for both food waste and LPG
    food_waste_forecast = forecast_consumption(food_waste_values)
    lpg_forecast = forecast_consumption(lpg_values)

    # Separate forecast data for the frontend
    forecast_data = {
        "food_waste_forecast": food_waste_forecast,
        "lpg_forecast": lpg_forecast,
    }

    # Debugging: Print forecast data to check values
    print("Forecast Data:", forecast_data)
    print("Current Emission Data:", current_emission_data)
    print("Total Emission:", total_emission)

    # Render template and pass data
    return render_template(
        'procurement_dashboard.html',
        food_waste_data=food_waste_data,
        lpg_data=lpg_data,
        forecast_data=forecast_data,
        current_emission_data=current_emission_data,
        total_emission=total_emission
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


@app.route('/food_consumption', methods=['GET', 'POST'])
def food_consumption():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Get the logged-in campus from the session
    campus = session.get('campus')

    # Determine associated campuses for specific campuses
    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
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

            # Gather form data
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

            # Insert data into the database
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

    # Fetch existing food data for associated campuses with pagination and filters
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Create SQL query with dynamic placeholders for associated campuses
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


@app.route('/fetch_consumption_data', methods=['GET'])
def fetch_consumption_data():
    table = request.args.get('table')

    # Dictionary mapping table IDs to SQL queries
    queries = {
        'foodWasteData': "SELECT * FROM tblfoodwaste",
        'lpgData': "SELECT * FROM tbllpgconsumption",
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
    campus = session.get('campus')

    # Determine associated campuses for specific campuses
    if campus.lower() == 'alangilan':
        associated_campuses = ['Alangilan', 'Lobo', 'Mabini', 'Balayan']
    elif campus.lower() == 'pablo borbon':
        associated_campuses = ['Pablo Borbon', 'Lemery', 'San Juan', 'Rosario', 'Central']
    else:
        associated_campuses = [campus]

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

            # Gather form data
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
