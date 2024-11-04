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

# Route for root URL, redirecting to /login
@app.route('/')
def index():
    return redirect(url_for('login'))

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
        username = request.form['username']  # Capture the username from the form
        new_password = request.form['new-password']
        confirm_password = request.form['confirm-password']

        if new_password != confirm_password:
            alert_message = "Passwords do not match!"
        else:
            try:
                # Connect to the database
                conn = get_db_connection()
                cursor = conn.cursor()

                # Hash the new password for security
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

                # Update the password based on the username
                update_query = "UPDATE tblsignin SET password = %s WHERE username = %s"
                cursor.execute(update_query, (hashed_password, username))
                conn.commit()

                # Check if any rows were affected (to confirm the update)
                if cursor.rowcount > 0:
                    flash("Password updated successfully!", "success")
                    return redirect(url_for('login'))  # Redirect to the login page
                else:
                    alert_message = "Password update failed. Username may not exist or no changes were made."

            except mysql.connector.Error as e:
                alert_message = f"Database error: {str(e)}"
            except Exception as e:
                alert_message = f"An error occurred: {str(e)}"

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
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetching total items and calculating total pages for electricity
        cursor.execute("SELECT COUNT(*) AS count FROM electricity_consumption WHERE campus = %s", (session['campus'],))
        total_items = cursor.fetchone()['count']
        total_pages = math.ceil(total_items / items_per_page)
        current_page = int(request.args.get('electricity_page', 1))
        offset = (current_page - 1) * items_per_page
        pagination_info['electricity'] = {'current_page': current_page, 'total_pages': total_pages}

        cursor.execute("SELECT * FROM electricity_consumption WHERE campus = %s LIMIT %s OFFSET %s", (session['campus'], items_per_page, offset))
        results['electricity'] = cursor.fetchall()

        # Repeat similar process for each table with pagination

        # Water Consumption
        cursor.execute("SELECT COUNT(*) AS count FROM tblwater WHERE Campus = %s", (session['campus'],))
        total_items = cursor.fetchone()['count']
        total_pages = math.ceil(total_items / items_per_page)
        current_page = int(request.args.get('water_page', 1))
        offset = (current_page - 1) * items_per_page
        pagination_info['water'] = {'current_page': current_page, 'total_pages': total_pages}

        cursor.execute("SELECT * FROM tblwater WHERE Campus = %s LIMIT %s OFFSET %s", (session['campus'], items_per_page, offset))
        results['water'] = cursor.fetchall()

        # Unsegregated Solid Waste
        cursor.execute("SELECT COUNT(*) AS count FROM tblsolidwasteunsegregated WHERE Campus = %s", (session['campus'],))
        total_items = cursor.fetchone()['count']
        total_pages = math.ceil(total_items / items_per_page)
        current_page = int(request.args.get('unsegWaste_page', 1))
        offset = (current_page - 1) * items_per_page
        pagination_info['unsegWaste'] = {'current_page': current_page, 'total_pages': total_pages}

        cursor.execute("SELECT * FROM tblsolidwasteunsegregated WHERE Campus = %s LIMIT %s OFFSET %s", (session['campus'], items_per_page, offset))
        results['unsegWaste'] = cursor.fetchall()

        # Segregated Solid Waste
        cursor.execute("SELECT COUNT(*) AS count FROM tblsolidwastesegregated WHERE Campus = %s", (session['campus'],))
        total_items = cursor.fetchone()['count']
        total_pages = math.ceil(total_items / items_per_page)
        current_page = int(request.args.get('segWaste_page', 1))
        offset = (current_page - 1) * items_per_page
        pagination_info['segWaste'] = {'current_page': current_page, 'total_pages': total_pages}

        cursor.execute("SELECT * FROM tblsolidwastesegregated WHERE Campus = %s LIMIT %s OFFSET %s", (session['campus'], items_per_page, offset))
        results['segWaste'] = cursor.fetchall()

        # Treated Water
        cursor.execute("SELECT COUNT(*) AS count FROM tbltreatedwater WHERE Campus = %s", (session['campus'],))
        total_items = cursor.fetchone()['count']
        total_pages = math.ceil(total_items / items_per_page)
        current_page = int(request.args.get('treatedWater_page', 1))
        offset = (current_page - 1) * items_per_page
        pagination_info['treatedWater'] = {'current_page': current_page, 'total_pages': total_pages}

        cursor.execute("SELECT * FROM tbltreatedwater WHERE Campus = %s LIMIT %s OFFSET %s", (session['campus'], items_per_page, offset))
        results['treatedWater'] = cursor.fetchall()

        # Fuel Emissions
        cursor.execute("SELECT COUNT(*) AS count FROM fuel_emissions WHERE Campus = %s", (session['campus'],))
        total_items = cursor.fetchone()['count']
        total_pages = math.ceil(total_items / items_per_page)
        current_page = int(request.args.get('fuelEmissions_page', 1))
        offset = (current_page - 1) * items_per_page
        pagination_info['fuelEmissions'] = {'current_page': current_page, 'total_pages': total_pages}

        cursor.execute("SELECT * FROM fuel_emissions WHERE Campus = %s LIMIT %s OFFSET %s", (session['campus'], items_per_page, offset))
        results['fuelEmissions'] = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")

    finally:
        cursor.close()
        conn.close()

    # Pass the results dictionary and pagination info to the template
    return render_template('report.html', results=results, pagination_info=pagination_info)


# Route for the EMU dashboard
@app.route('/emu')
def emu_dashboard():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Retrieve the campus from session, default to 'default_campus' if not set
    campus = session.get('campus', 'default_campus')

    # Initialize report data
    electricity_data = []
    fuel_data = []
    waste_segregation_data = []
    waste_unsegregation_data = []
    treated_water_data = []
    water_data = []

    try:
        # Establish database connection
        conn = get_db_connection()
        if conn is None:
            raise Error("Could not establish database connection.")
        
        cursor = conn.cursor(dictionary=True)

        # Fetch data for the specific campus
        cursor.execute("SELECT consumption FROM electricity_consumption WHERE campus = %s", (campus,))
        electricity_data = [row['consumption'] for row in cursor.fetchall()]

        cursor.execute("SELECT total_emission FROM fuel_emissions WHERE campus = %s", (campus,))
        fuel_data = [row['total_emission'] for row in cursor.fetchall()]

        cursor.execute("SELECT QuantityInKG FROM tblsolidwastesegregated WHERE Campus = %s", (campus,))
        waste_segregation_data = [row['QuantityInKG'] for row in cursor.fetchall()]

        cursor.execute("SELECT QuantityInKG FROM tblsolidwasteunsegregated WHERE Campus = %s", (campus,))
        waste_unsegregation_data = [row['QuantityInKG'] for row in cursor.fetchall()]

        cursor.execute("SELECT TreatedWaterVolume FROM tbltreatedwater WHERE Campus = %s", (campus,))
        treated_water_data = [row['TreatedWaterVolume'] for row in cursor.fetchall()]

        cursor.execute("SELECT Consumption FROM tblwater WHERE Campus = %s", (campus,))
        water_data = [row['Consumption'] for row in cursor.fetchall()]

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        print(f"Database Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

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

    # Render the template and pass data
    return render_template('emu_index.html',
                           electricity_data=electricity_data,
                           fuel_data=fuel_data,
                           waste_segregation_data=waste_segregation_data,
                           waste_unsegregation_data=waste_unsegregation_data,
                           treated_water_data=treated_water_data,
                           water_data=water_data,
                           forecast_data=forecast_data)




#Route for Electricity Consumption
@app.route('/electricity_consumption', methods=['GET', 'POST'])
def electricity_consumption():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    # Set up pagination parameters
    page = request.args.get('page', 1, type=int)  # Get the current page number from the query string
    per_page = 15  # Number of records per page
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

        # Build the SQL query with optional filtering
        sql = "SELECT * FROM electricity_consumption WHERE campus = %s"
        params = [session['campus']]  # Use the logged-in campus from session

        if selected_month:
            sql += " AND month = %s"
            params.append(selected_month)

        if selected_quarter:
            sql += " AND quarter = %s"
            params.append(selected_quarter)

        if selected_year:
            sql += " AND year = %s"
            params.append(selected_year)

        # Get total records with filters
        cursor.execute(f"SELECT COUNT(*) FROM ({sql}) as total", params)
        total_records = cursor.fetchone()['COUNT(*)']
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

    campus = session.get('campus')
    selected_year = request.args.get('year')  # Get the selected year from query parameters
    selected_category = request.args.get('category')  # Get the selected category from query parameters
    current_page = request.args.get('page', 1, type=int)  # Get the current page, default is 1
    per_page = 15  # Number of records per page
    offset = (current_page - 1) * per_page

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

        # SQL base query with dynamic conditions based on the selected filters
        base_query = "SELECT * FROM tblwater WHERE Campus = %s"
        query_params = [campus]

        # If a year is selected, filter by that year (based on the YYYY-MM-DD format)
        if selected_year:
            base_query += " AND YEAR(Date) = %s"
            query_params.append(selected_year)

        # If a category is selected, filter by category
        if selected_category:
            base_query += " AND Category = %s"
            query_params.append(selected_category)

        # Count the total records with the current filters applied
        count_query = f"SELECT COUNT(*) FROM ({base_query}) as total_count"
        cursor.execute(count_query, query_params)
        total_records = cursor.fetchone()['COUNT(*)']
        total_pages = (total_records + per_page - 1) // per_page  # Calculate the total number of pages

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

    return render_template('water_consumption.html', 
                           reports=reports, 
                           selected_year=selected_year, 
                           selected_category=selected_category, 
                           current_page=current_page, 
                           total_pages=total_pages)

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
    if not campus:
        flash("No campus found in session.", "danger")
        return redirect(url_for('emu_dashboard'))  # Redirect if campus is missing

    page = request.args.get('page', 1, type=int)
    per_page = 15
    offset = (page - 1) * per_page

    if request.method == 'POST':
        # Print to confirm form submission
        print("Form submitted. Processing POST request...")

        # Get form data
        month = request.form.get('month')
        treated_volume = request.form.get('treatedVolume')
        reused_volume = request.form.get('reusedVolume')

        # Ensure values are provided and are valid numbers
        try:
            treated_volume = float(treated_volume)
            reused_volume = float(reused_volume)
        except ValueError:
            flash("Please enter valid numeric values for volumes.", "danger")
            return redirect(url_for('treated_water'))

        # Calculate additional fields
        effluent_volume = treated_volume - reused_volume
        co2_factor = 0.272  # Example emission factor
        kg_co2_e = effluent_volume * co2_factor
        t_co2_e = kg_co2_e / 1000

        # Calculate the price per liter based on kgCO2e/m³
        price_per_liter = kg_co2_e  # Assign kgCO2e as the price per liter

        # Debugging: print values being inserted
        print(f"Inserting into DB: Campus={campus}, Month={month}, TreatedVolume={treated_volume}, "
              f"ReusedVolume={reused_volume}, EffluentVolume={effluent_volume}, "
              f"CO2 (kg)={kg_co2_e}, CO2 (t)={t_co2_e}, PricePerLiter={price_per_liter}")

        try:
            # Attempt to connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert the record into the database
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

        # Redirect to the same page after insertion
        return redirect(url_for('treated_water'))

    # Fetch existing records for the logged-in campus with pagination
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get total record count for the campus
        cursor.execute("SELECT COUNT(*) FROM tbltreatedwater WHERE Campus = %s", (campus,))
        total_records = cursor.fetchone()['COUNT(*)']
        total_pages = (total_records + per_page - 1) // per_page

        # Fetch records for the campus with pagination
        cursor.execute("SELECT * FROM tbltreatedwater WHERE Campus = %s LIMIT %s OFFSET %s", (campus, per_page, offset))
        reports = cursor.fetchall()

        # Debugging: print fetched reports
        print(f"Reports fetched for campus {campus}: {reports}")

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        reports = []
        total_pages = 0

    finally:
        cursor.close()
        conn.close()

    # Render the template with the fetched data
    return render_template('treated_water.html', reports=reports, current_page=page, total_pages=total_pages)



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

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            # Process form submission
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
            quantity_liters = request.form.get('quantityLiters')
            total_amount = request.form.get('totalAmount')

            # Validate data
            if not (campus and date and driver and type and vehicle_equipment and plate_no and fuel_type and quantity_liters and total_amount):
                return jsonify({'success': False, 'message': 'Please fill out all required fields.'})

            # Calculate emissions based on quantity_liters
            co2_emission = float(quantity_liters) * 2.556     # CO2 Emission
            nh4_emission = float(quantity_liters) * 0.00275   # NH4 Emission
            n2o_emission = float(quantity_liters) * 0.044998  # N2O Emission
            total_emission = co2_emission + nh4_emission + n2o_emission  # Total Emission in kg CO2-e
            total_emission_t = total_emission / 1000           # Convert total emission to metric tons

            # Insert the new record into the database including the calculated emission values
            insert_query = """
            INSERT INTO fuel_emissions (campus, date, driver, type, vehicle_equipment, plate_no, category, fuel_type, item_description, transaction_no, odometer, quantity_liters, total_amount, co2_emission, nh4_emission, n2o_emission, total_emission, total_emission_t)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                campus, date, driver, type, vehicle_equipment, plate_no, category, fuel_type, 
                item_description, transaction_no, odometer, quantity_liters, total_amount, 
                co2_emission, nh4_emission, n2o_emission, total_emission, total_emission_t
            ))
            conn.commit()

            # Return the new record as JSON so it can be dynamically added to the table
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
                'co2_emission': co2_emission,
                'nh4_emission': nh4_emission,
                'n2o_emission': n2o_emission,
                'total_emission': total_emission,
                'total_emission_t': total_emission_t
            }

            return jsonify({'success': True, 'data': new_record})

        # Handle GET request for fetching and displaying data
        page = request.args.get('page', 1, type=int)
        per_page = 15
        offset = (page - 1) * per_page

        # Retrieve filters from query parameters
        year_filter = request.args.get('year', '')
        category_filter = request.args.get('category', '')
        fuel_type_filter = request.args.get('fuelType', '')

        # Retrieve campus from session
        user_campus = session.get('campus', None)
        if not user_campus:
            return redirect(url_for('login'))

        # Prepare SQL query
        sql = "SELECT * FROM fuel_emissions WHERE campus = %s"
        params = [user_campus]

        # Apply filters
        if year_filter:
            sql += " AND YEAR(date) = %s"
            params.append(year_filter)
        if category_filter:
            sql += " AND category = %s"
            params.append(category_filter)
        if fuel_type_filter:
            sql += " AND fuel_type = %s"
            params.append(fuel_type_filter)

        # Add pagination to the SQL query
        sql += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

        # Execute query to get total records for pagination
        cursor.execute("SELECT COUNT(*) AS total FROM fuel_emissions WHERE campus = %s", (user_campus,))
        total_records = cursor.fetchone()['total']
        total_pages = (total_records + per_page - 1) // per_page

        # Fetch filtered fuel consumption data
        cursor.execute(sql, tuple(params))
        reports = cursor.fetchall()

        # If no reports were found, initialize reports as an empty list
        if not reports:
            reports = []

        # Render the main template with the reports
        return render_template('emu_fuel.html', reports=reports, current_page=page, total_pages=total_pages)

    except mysql.connector.Error as e:
        return jsonify({'success': False, 'message': f'Database error: {e}'})

    finally:
        if cursor:
            cursor.close()
        if conn:
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
    # Define pagination variables
    page = request.args.get('page', 1, type=int)
    per_page = 15
    offset = (page - 1) * per_page

    # Get the logged-in user's campus from session
    campus = session.get('campus')

    # Handle POST request (form submission)
    if request.method == 'POST':
        try:
            # Retrieve form data
            year = request.form.get('year')
            month = request.form.get('month')
            quarter = request.form.get('quarter')
            main_category = request.form.get('mainCategory')
            sub_category = request.form.get('subCategory')
            quantity = float(request.form.get('quantity'))

            # Debugging: Print form data to check if values are correctly retrieved
            print(f"Form Data: Year={year}, Month={month}, Quarter={quarter}, Main Category={main_category}, Subcategory={sub_category}, Quantity={quantity}")

            # Define emission factors for each main category
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

            # Calculate GHG emissions using the selected emission factor
            emission_factor = emission_factors.get(main_category, {}).get(sub_category, 0)
            ghg_emission_kg = quantity * emission_factor
            ghg_emission_t = ghg_emission_kg / 1000

            # Debugging: Print calculated GHG emissions
            print(f"GHG Emission (kg): {ghg_emission_kg}, GHG Emission (t): {ghg_emission_t}")

            # Insert data into the database
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """INSERT INTO tblsolidwastesegregated 
                     (Campus, Year, Quarter, Month, MainCategory, SubCategory, QuantityInKG, GHGEmissionKGCO2e, GHGEmissionTCO2e)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (campus, year, quarter, month, main_category, sub_category, quantity, ghg_emission_kg, ghg_emission_t))
            conn.commit()

            # Debugging: Print success message after database commit
            print("Data inserted successfully.")

            flash("Waste segregation record added successfully.", "success")
        except mysql.connector.Error as e:
            # Log and flash database errors
            print(f"Database Error: {e}")
            flash(f"Database Error: {e}", "danger")
        except ValueError:
            flash("Invalid data entered. Please check the form fields.", "danger")
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('waste_segregation'))

    # Handle GET request (displaying reports with pagination)
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get total records for the logged-in user's campus
        cursor.execute("SELECT COUNT(*) FROM tblsolidwastesegregated WHERE Campus = %s", (campus,))
        total_records = cursor.fetchone()['COUNT(*)']
        total_pages = (total_records + per_page - 1) // per_page

        # Fetch reports only for the logged-in user's campus with pagination
        cursor.execute("SELECT * FROM tblsolidwastesegregated WHERE Campus = %s LIMIT %s OFFSET %s", (campus, per_page, offset))
        reports = cursor.fetchall()

        # Debugging: Print fetched reports to verify
        print(f"Fetched Reports: {reports}")

    except mysql.connector.Error as e:
        # Log and flash database errors
        print(f"Database Error: {e}")
        flash(f"Database Error: {e}", "danger")
        reports = []
        total_pages = 0
    finally:
        cursor.close()
        conn.close()

    return render_template('waste_segregation.html', reports=reports, current_page=page, total_pages=total_pages)



# Route for Waste Unsegregation
@app.route('/waste_unsegregation', methods=['GET'])
def waste_unsegregation():
    page = request.args.get('page', 1, type=int)  # Get the current page number, default to 1
    per_page = 15  # Number of records per page
    offset = (page - 1) * per_page  # Calculate the offset for SQL query

    # Get filters from query parameters (year and month)
    selected_year = request.args.get('year')
    selected_month = request.args.get('month')

    # Retrieve campus from session
    campus = session.get('campus')  # Assuming the user's campus is stored in the session

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Base SQL query
        sql = "SELECT * FROM tblsolidwasteunsegregated WHERE Campus = %s"
        count_sql = "SELECT COUNT(*) AS total FROM tblsolidwasteunsegregated WHERE Campus = %s"
        params = [campus]  # Start parameters with the campus filter

        # Apply year filter if selected
        if selected_year:
            sql += " AND Year = %s"
            count_sql += " AND Year = %s"
            params.append(selected_year)

        # Apply month filter if selected
        if selected_month:
            sql += " AND Month = %s"
            count_sql += " AND Month = %s"
            params.append(selected_month)

        # Get total record count for pagination
        cursor.execute(count_sql, params)
        total_records = cursor.fetchone()['total']
        total_pages = (total_records + per_page - 1) // per_page  # Calculate total pages

        # Fetch filtered results with pagination
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

    # Pass selected_year and selected_month to the template to retain the filters
    return render_template(
        'waste_unsegregation.html',
        reports=reports,
        current_page=page,
        total_pages=total_pages,
        selected_year=selected_year,
        selected_month=selected_month
    )



# Route for handling the addition of waste unsegregation data via POST request
@app.route('/add_waste_unsegregated', methods=['POST'])
def add_waste_unsegregated():
    # Retrieve form data
    campus = request.form.get('campus')
    year = request.form.get('year')
    month = request.form.get('month')
    waste_type = request.form.get('wasteType')
    quantity_kg = float(request.form.get('quantityKg'))
    sent_to_landfill_kg = float(request.form.get('sentToLandfillKg'))

    # Perform necessary calculations
    sent_to_landfill_tons = sent_to_landfill_kg / 1000
    percentage = (sent_to_landfill_kg / quantity_kg) * 100 if quantity_kg else 0
    ghg_emission_kg_co2e = sent_to_landfill_tons * 0.8 * 0.25 * 0.5 * 0.5 * 1.33
    ghg_emission_t_co2e = ghg_emission_kg_co2e / 1000

    try:
        # Insert data into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO tblsolidwasteunsegregated 
                 (Campus, Year, Month, WasteType, QuantityInKG, SentToLandfillKG, SentToLandfillTONS, Percentage, GHGEmissionKGCO2e, GHGEmissionTCO2e)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (campus, year, month, waste_type, quantity_kg, sent_to_landfill_kg, sent_to_landfill_tons, percentage, ghg_emission_kg_co2e, ghg_emission_t_co2e))
        conn.commit()

        flash("Waste unsegregated record added successfully.", "success")
        return redirect(url_for('waste_unsegregation'))

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        return redirect(url_for('waste_unsegregation'))

    finally:
        cursor.close()
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

    campus = request.args.get('campus', 'All Campuses')
    username = session.get('username')

    data = {
        'electricity': [],
        'fuel': [],
        'waste_segregation': [],
        'waste_unsegregation': [],
        'treated_water': [],
        'water': [],
        'lpg': [],
        'food_waste': [],
        'accommodation': [],
        'flight': []
    }

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        queries = {
            'electricity': "SELECT campus, SUM(consumption) as consumption FROM electricity_consumption",
            'fuel': "SELECT campus, SUM(consumption) as consumption FROM fuel_emissions",
            'waste_segregation': "SELECT campus, SUM(segregated_amount) as consumption FROM tblsolidwastesegregated",
            'waste_unsegregation': "SELECT campus, SUM(unsegregated_amount) as consumption FROM tblsolidwasteunsegregated",
            'treated_water': "SELECT campus, SUM(treated_water_volume) as consumption FROM tbltreatedwater",
            'water': "SELECT campus, SUM(consumption) as consumption FROM tblwater",
            'lpg': "SELECT campus, SUM(consumption) as consumption FROM tbllpg",
            'food_waste': "SELECT campus, SUM(consumption) as consumption FROM tblfoodwaste",
            'accommodation': "SELECT campus, SUM(consumption) as consumption FROM tblaccommodation",
            'flight': "SELECT campus, SUM(ghg_emission) as consumption FROM tblflight"
        }

        for key, query in queries.items():
            if campus == 'All Campuses':
                query += " GROUP BY campus"
            else:
                query += " WHERE campus = %s GROUP BY campus"
                cursor.execute(query, (campus,))
            cursor.execute(query)
            data[key] = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f"Database error: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    def get_consumption_values(data, key):
        return [row[key] for row in data if key in row]

    def forecast_consumption(data, periods=12):
        if len(data) > 0:
            try:
                model = ARIMA(data, order=(5, 1, 0))
                model_fit = model.fit()
                forecast = model_fit.forecast(steps=periods)
                return forecast.tolist()
            except Exception as e:
                flash(f"ARIMA Error: {e}", "danger")
                return [0] * periods
        else:
            return [0] * periods

    forecast_data = {
        "electricity_forecast": forecast_consumption(get_consumption_values(data['electricity'], 'consumption')),
        "fuel_forecast": forecast_consumption(get_consumption_values(data['fuel'], 'consumption')),
        "waste_segregation_forecast": forecast_consumption(get_consumption_values(data['waste_segregation'], 'consumption')),
        "waste_unsegregation_forecast": forecast_consumption(get_consumption_values(data['waste_unsegregation'], 'consumption')),
        "treated_water_forecast": forecast_consumption(get_consumption_values(data['treated_water'], 'consumption')),
        "water_forecast": forecast_consumption(get_consumption_values(data['water'], 'consumption')),
        "lpg_forecast": forecast_consumption(get_consumption_values(data['lpg'], 'consumption')),
        "food_waste_forecast": forecast_consumption(get_consumption_values(data['food_waste'], 'consumption')),
        "accommodation_forecast": forecast_consumption(get_consumption_values(data['accommodation'], 'consumption')),
        "flight_forecast": forecast_consumption(get_consumption_values(data['flight'], 'consumption'))
    }

    return render_template(
        'csd_dashboard.html',
        username=username,
        campus=campus,
        data=data,
        forecast_data=forecast_data
    )

@app.route('/fetch_forecast_data', methods=['GET'])
def fetch_csd_forecast_data():
    campus = request.args.get('campus', 'All Campuses')  # Get the campus from the request
    year = request.args.get('year', '2023')  # Optional year filtering
    view_type = request.args.get('view_type', 'monthly')  # View type (monthly/yearly)

    # Initialize forecast data
    forecast_data = {
        "electricity_forecast": [],
        "fuel_forecast": [],
        "waste_segregation_forecast": [],
        "waste_unsegregation_forecast": [],
        "treated_water_forecast": [],
        "water_forecast": [],
        "lpg_forecast": [],
        "food_waste_forecast": [],
        "accommodation_forecast": [],
        "flight_forecast": []
    }

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        queries = {
            'electricity': "SELECT campus, SUM(consumption) as consumption FROM electricity_consumption",
            'fuel': "SELECT campus, SUM(consumption) as consumption FROM fuel_emissions",
            'waste_segregation': "SELECT campus, SUM(segregated_amount) as consumption FROM tblsolidwastesegregated",
            'waste_unsegregation': "SELECT campus, SUM(unsegregated_amount) as consumption FROM tblsolidwasteunsegregated",
            'treated_water': "SELECT campus, SUM(treated_water_volume) as consumption FROM tbltreatedwater",
            'water': "SELECT campus, SUM(consumption) as consumption FROM tblwater",
            'lpg': "SELECT campus, SUM(consumption) as consumption FROM tbllpg",
            'food_waste': "SELECT campus, SUM(consumption) as consumption FROM tblfoodwaste",
            'accommodation': "SELECT campus, SUM(consumption) as consumption FROM tblaccommodation",
            'flight': "SELECT campus, SUM(ghg_emission) as consumption FROM tblflight"
        }

        for key, query in queries.items():
            if campus == 'All Campuses':
                cursor.execute(query + " GROUP BY campus")
            else:
                cursor.execute(query + " WHERE campus = %s GROUP BY campus", (campus,))

            # Fetch and forecast the data
            data = [row['consumption'] for row in cursor.fetchall()]
            forecast_data[f"{key}_forecast"] = forecast_consumption(data) or [0] * 12  # Monthly forecast

    except Exception as e:
        print(f"Error fetching forecast data: {e}")
        forecast_data = {key: [0] * 12 for key in forecast_data}  # Default to zeros if error

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return jsonify(forecast_data)


# Route for the Center for Sustainable Development Report
@app.route('/csd_report', methods=['GET'])
def csd_report():
    # Retrieve the selected campus, office, and page from the request arguments
    campus = request.args.get('campus', 'All Campuses')
    selected_office = request.args.get('office', 'all_offices')
    
    # Default values for pagination
    page_size = 15  # Number of records per page
    reports = {}
    pagination_info = {}

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
            # Retrieve the current page number for each table
            page = int(request.args.get(f"{key}_page", 1))
            offset = (page - 1) * page_size

            # Build query with pagination and optional campus filtering
            base_query = tables[key]
            if campus and campus != "All Campuses":
                # Apply campus filter if a specific campus is selected
                query = f"{base_query} WHERE campus = %s LIMIT %s OFFSET %s"
                cursor.execute(query, (campus, page_size, offset))
            else:
                # No campus filter, retrieve paginated data
                query = f"{base_query} LIMIT %s OFFSET %s"
                cursor.execute(query, (page_size, offset))

            # Fetch paginated data and total record count for each table
            data = cursor.fetchall()
            reports[key] = data
            
            # Calculate total records for pagination
            count_query = f"SELECT COUNT(*) as count FROM ({base_query}) as total_count"
            if campus and campus != "All Campuses":
                count_query += " WHERE campus = %s"
                cursor.execute(count_query, (campus,))
            else:
                cursor.execute(count_query)
            total_records = cursor.fetchone()['count']
            total_pages = (total_records + page_size - 1) // page_size  # Calculate total pages

            # Store pagination info for each table
            pagination_info[key] = {
                'current_page': page,
                'total_pages': total_pages,
                'total_records': total_records
            }

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        return "An error occurred while fetching the data."

    finally:
        # Close cursor and database connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.close()

    # Render the report page with the filtered reports data and pagination info
    return render_template(
        'csd_report.html',
        reports=reports,
        pagination_info=pagination_info,
        selected_campus=campus,
        selected_office=selected_office
    )
    

@app.route('/export_data', methods=['POST'])
def export_data():
    try:
        # Get the selected consumption type, format, and layout from the form
        consumption_type = request.form.get('consumption_type', 'all')
        export_format = request.form.get('export_format', 'pdf')
        print_layout = request.form.get('print_layout', 'portrait')  # Default to portrait

        # Define queries for each table
        tables_to_export = {
            'electricity': "SELECT * FROM electricity_consumption",
            'water': "SELECT * FROM tblwater",
            'waste_unsegregation': "SELECT * FROM tblsolidwasteunsegregated",
            'waste_segregation': "SELECT * FROM tblsolidwastesegregated",
            'fuel_emissions': "SELECT * FROM fuel_emissions",
            'food_data': "SELECT * FROM tblfoodwaste",
            'lpg_data': "SELECT * FROM tbllpg",
            'flight_data': "SELECT * FROM tblflight",
            'accommodation_data': "SELECT * FROM tblaccommodation"
        }

        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor(dictionary=True)

        # Retrieve data for selected consumption type(s)
        selected_data = {}
        for key, query in tables_to_export.items():
            if consumption_type == 'all' or consumption_type == key:
                cursor.execute(query)
                records = cursor.fetchall()
                if records:
                    df = pd.DataFrame(records)
                    if 'id' in df.columns:
                        df = df.drop(columns=['id'])  # Drop 'id' column if exists
                    selected_data[key] = df
        
        cursor.close()
        db_connection.close()

        # Set the report title based on the selected consumption type
        if consumption_type == 'all':
            report_title = "Full Consumption Report"
        else:
            report_title = f"{consumption_type.replace('_', ' ').title()} Consumption Report"
        
        # Paths to logos (assuming the images are in static/images)
        bsu_logo_path = 'static/images/bsu.png'
        csd_logo_path = 'static/images/CSD.png'

        # Export to Excel if selected
        if export_format == 'excel':
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for sheet_name, df in selected_data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=2)  # Start at row 2 to add header

                    # Get the worksheet and workbook objects
                    worksheet = writer.sheets[sheet_name]
                    workbook = writer.book

                    # Add the report title at the top
                    worksheet.merge_range('A1:D1', report_title, workbook.add_format({
                        'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'
                    }))

                    # Insert logos
                    try:
                        worksheet.insert_image('A1', bsu_logo_path, {'x_scale': 0.15, 'y_scale': 0.15})
                        worksheet.insert_image('D1', csd_logo_path, {'x_scale': 0.15, 'y_scale': 0.15})
                    except FileNotFoundError:
                        print("Error: One or both image files not found for Excel export.")

                    # Format headers
                    header_format = workbook.add_format({
                        'bold': True, 'bg_color': '#D9E1F2', 'border': 1, 'align': 'center'
                    })
                    for col_num, value in enumerate(df.columns.values):
                        worksheet.write(2, col_num, value, header_format)  # Write headers below title and logos

                    # Adjust column widths
                    for i, col in enumerate(df.columns):
                        max_col_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                        worksheet.set_column(i, i, max_col_width)

            output.seek(0)
            return send_file(
                output, as_attachment=True, download_name=f'{report_title.replace(" ", "_").lower()}.xlsx',
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        # Export to PDF if selected
        elif export_format == 'pdf':
            class CustomPDF(FPDF):
                def __init__(self, title, layout):
                    # Set the layout (orientation) based on user selection
                    super().__init__(orientation=layout)
                    self.title = title
                    self.layout = layout

                def header(self):
                    # Adjust logo positions based on layout
                    if self.layout == 'P':  # Portrait mode
                        # Logos for portrait mode
                        self.image(bsu_logo_path, 10, 8, 25)  # Adjust as needed
                        self.image(csd_logo_path, 180, 8, 25)  # Adjust as needed
                    else:
                        # Logos for landscape mode
                        self.image(bsu_logo_path, 10, 8, 20)  # Adjust as needed
                        self.image(csd_logo_path, 270, 8, 20)  # Adjust as needed

                    # Add the report title
                    self.set_font('Arial', 'B', 12)
                    self.cell(0, 10, self.title, align='C', ln=True)
                    self.ln(10)

            # Set PDF layout to 'P' (portrait) or 'L' (landscape) based on the selection
            pdf_layout = 'P' if print_layout == 'portrait' else 'L'
            pdf = CustomPDF(title=report_title, layout=pdf_layout)
            pdf.set_auto_page_break(auto=True, margin=10)
            pdf.add_page()
            pdf.set_font("Arial", size=10)

            # Add each DataFrame as a section in the PDF
            for sheet_name, df in selected_data.items():
                pdf.set_font("Arial", size=8)

                # Calculate column widths to fit within the page
                page_width = pdf.w - 20  # Page width minus margins
                num_columns = len(df.columns)
                col_width = page_width / num_columns

                # Add table header with a light background color
                headers = df.columns.tolist()
                pdf.set_fill_color(217, 225, 242)
                for header in headers:
                    pdf.cell(col_width, 10, header, border=1, align='C', fill=True)
                pdf.ln()

                # Add table rows
                for _, row in df.iterrows():
                    for col in headers:
                        pdf.cell(col_width, 10, str(row[col]), border=1, align='C')
                    pdf.ln()

                pdf.add_page()  # Add a new page between tables

            # Send the PDF output as a downloadable file
            pdf_output = BytesIO()
            pdf_output.write(pdf.output(dest='S').encode('latin1'))
            pdf_output.seek(0)
            return send_file(
                pdf_output, as_attachment=True, download_name=f'{report_title.replace(" ", "_").lower()}.pdf', 
                mimetype='application/pdf'
            )

    except Exception as e:
        # Print the error stack trace to console for debugging
        print("An error occurred during export:")
        traceback.print_exc()
        flash("An error occurred while exporting the data. Please check server logs.", "danger")
        return render_template("csd_report.html")
    

@app.route('/sdo_dashboard')
def sdo_dashboard():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in

    campus = session['campus']  # Retrieve the campus from session

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
        cursor = conn.cursor(dictionary=True)

        # Fetch electricity data
        cursor.execute("SELECT * FROM electricity_consumption WHERE campus = %s", (campus,))
        electricity_data = cursor.fetchall()

        # Fetch fuel data
        cursor.execute("SELECT * FROM fuel_emissions WHERE campus = %s", (campus,))
        fuel_data = cursor.fetchall()

        # Fetch waste segregation data
        cursor.execute("SELECT * FROM tblsolidwastesegregated WHERE campus = %s", (campus,))
        waste_segregation_data = cursor.fetchall()

        # Fetch waste unsegregation data
        cursor.execute("SELECT * FROM tblsolidwasteunsegregated WHERE campus = %s", (campus,))
        waste_unsegregation_data = cursor.fetchall()

        # Fetch treated water data
        cursor.execute("SELECT * FROM tbltreatedwater WHERE campus = %s", (campus,))
        treated_water_data = cursor.fetchall()

        # Fetch water consumption data
        cursor.execute("SELECT * FROM tblwater WHERE campus = %s", (campus,))
        water_data = cursor.fetchall()

        # Fetch LPG consumption data
        cursor.execute("SELECT * FROM tbllpg WHERE campus = %s", (campus,))
        lpg_data = cursor.fetchall()

        # Fetch food waste data
        cursor.execute("SELECT * FROM tblfoodwaste WHERE campus = %s", (campus,))
        food_waste_data = cursor.fetchall()

        # Fetch accommodation data
        cursor.execute("SELECT * FROM tblaccommodation WHERE campus = %s", (campus,))
        accommodation_data = cursor.fetchall()

        # Fetch flight emissions data
        cursor.execute("SELECT * FROM tblflight WHERE campus = %s", (campus,))
        flight_data = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Function to extract values from the data
    def get_consumption_values(data, key):
        return [row[key] for row in data if key in row]

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
                return [0] * periods  # Return a list of zeros instead of Undefined
        else:
            return [0] * periods  # Return a list of zeros if no data is available

    # Extract values for ARIMA forecast
    electricity_values = get_consumption_values(electricity_data, 'consumption')
    fuel_values = get_consumption_values(fuel_data, 'consumption')
    waste_segregation_values = get_consumption_values(waste_segregation_data, 'segregated_amount')
    waste_unsegregation_values = get_consumption_values(waste_unsegregation_data, 'unsegregated_amount')
    treated_water_values = get_consumption_values(treated_water_data, 'treated_water_volume')
    water_values = get_consumption_values(water_data, 'consumption')
    lpg_values = get_consumption_values(lpg_data, 'consumption')
    food_waste_values = get_consumption_values(food_waste_data, 'consumption')
    accommodation_values = get_consumption_values(accommodation_data, 'consumption')
    flight_values = get_consumption_values(flight_data, 'ghg_emission')

    # Forecast data
    forecast_data = {
        "electricity_forecast": forecast_consumption(electricity_values),
        "fuel_forecast": forecast_consumption(fuel_values),
        "waste_segregation_forecast": forecast_consumption(waste_segregation_values),
        "waste_unsegregation_forecast": forecast_consumption(waste_unsegregation_values),
        "treated_water_forecast": forecast_consumption(treated_water_values),
        "water_forecast": forecast_consumption(water_values),
        "lpg_forecast": forecast_consumption(lpg_values),
        "food_waste_forecast": forecast_consumption(food_waste_values),
        "accommodation_forecast": forecast_consumption(accommodation_values),
        "flight_forecast": forecast_consumption(flight_values)
    }

    # Render template and pass data
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
        forecast_data=forecast_data
    )


# Route to fetch updated forecast data
@app.route('/fetch_forecast_data', methods=['GET'])
def fetch_sdo_forecast_data():
    campus = session.get('campus', 'Lipa')  # Assume 'Lipa' as default campus

    # Initialize forecast data
    forecast_data = {
        "electricity_forecast": [],
        "fuel_forecast": [],
        "waste_segregation_forecast": [],
        "waste_unsegregation_forecast": [],
        "treated_water_forecast": [],
        "water_forecast": [],
        "lpg_forecast": [],
        "food_waste_forecast": [],
        "accommodation_forecast": [],
        "flight_forecast": []
    }

    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch data for electricity
        cursor.execute("SELECT consumption FROM electricity_consumption WHERE campus = %s", (campus,))
        electricity_data = [row['consumption'] for row in cursor.fetchall()]

        # Fetch data for fuel consumption
        cursor.execute("SELECT consumption FROM fuel_emissions WHERE campus = %s", (campus,))
        fuel_data = [row['consumption'] for row in cursor.fetchall()]

        # Fetch data for waste segregation
        cursor.execute("SELECT segregated_amount FROM tblsolidwastesegregated WHERE campus = %s", (campus,))
        waste_segregation_data = [row['segregated_amount'] for row in cursor.fetchall()]

        # Fetch data for waste unsegregation
        cursor.execute("SELECT unsegregated_amount FROM tblsolidwasteunsegregated WHERE campus = %s", (campus,))
        waste_unsegregation_data = [row['unsegregated_amount'] for row in cursor.fetchall()]

        # Fetch data for treated water
        cursor.execute("SELECT treated_water_volume FROM treated_water WHERE campus = %s", (campus,))
        treated_water_data = [row['treated_water_volume'] for row in cursor.fetchall()]

        # Fetch data for water consumption
        cursor.execute("SELECT consumption FROM water_consumption WHERE campus = %s", (campus,))
        water_data = [row['consumption'] for row in cursor.fetchall()]

        # Fetch data for LPG consumption
        cursor.execute("SELECT consumption FROM tbllpg WHERE campus = %s", (campus,))
        lpg_data = [row['consumption'] for row in cursor.fetchall()]

        # Fetch data for food waste
        cursor.execute("SELECT consumption FROM tblfoodwaste WHERE campus = %s", (campus,))
        food_waste_data = [row['consumption'] for row in cursor.fetchall()]

        # Fetch data for accommodation
        cursor.execute("SELECT consumption FROM tblaccommodation WHERE campus = %s", (campus,))
        accommodation_data = [row['consumption'] for row in cursor.fetchall()]

        # Fetch data for flight emissions
        cursor.execute("SELECT ghg_emission FROM tblflight WHERE campus = %s", (campus,))
        flight_data = [row['ghg_emission'] for row in cursor.fetchall()]

        # Generate forecast for each data set
        forecast_data = {
            "electricity_forecast": forecast_consumption(electricity_data) or [0] * 6,
            "fuel_forecast": forecast_consumption(fuel_data) or [0] * 6,
            "waste_segregation_forecast": forecast_consumption(waste_segregation_data) or [0] * 6,
            "waste_unsegregation_forecast": forecast_consumption(waste_unsegregation_data) or [0] * 6,
            "treated_water_forecast": forecast_consumption(treated_water_data) or [0] * 6,
            "water_forecast": forecast_consumption(water_data) or [0] * 6,
            "lpg_forecast": forecast_consumption(lpg_data) or [0] * 6,
            "food_waste_forecast": forecast_consumption(food_waste_data) or [0] * 6,
            "accommodation_forecast": forecast_consumption(accommodation_data) or [0] * 6,
            "flight_forecast": forecast_consumption(flight_data) or [0] * 6
        }

    except Exception as e:
        print(f"Error fetching forecast data: {e}")  # Log the error
        forecast_data = {key: [0] * 6 for key in forecast_data}  # Default values

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return jsonify(forecast_data)


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

    # Forecast data
    forecast_data = {
        "flight_forecast": forecast_consumption(flight_values),
        "accommodation_forecast": forecast_consumption(accommodation_values),
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

# Route for flight data submission and display
@app.route('/flight', methods=['GET', 'POST'])
def flight():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    campus = session.get('campus')

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

            # Insert flight data into tblflight
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

    # Modify query to filter by campus and selected_year if provided
    query = "SELECT * FROM tblflight WHERE Campus = %s"
    params = [campus]

    if selected_year:
        query += " AND Year = %s"
        params.append(selected_year)

    # Apply pagination
    limit = 10
    offset = (current_page - 1) * limit
    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    # Execute query
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)

    flight_data = cursor.fetchall()

    # Calculate total pages for pagination
    cursor.execute("SELECT COUNT(*) FROM tblflight WHERE Campus = %s" + (" AND Year = %s" if selected_year else ""), 
                   [campus] + ([selected_year] if selected_year else []))
    total_records = cursor.fetchone()['COUNT(*)']
    total_pages = (total_records // limit) + (1 if total_records % limit > 0 else 0)

    cursor.close()
    conn.close()

    # Pass flight_data, total_pages, current_page, and selected_year to the template
    return render_template('flight.html', flight_data=flight_data, total_pages=total_pages, 
                           current_page=current_page, selected_year=selected_year)


@app.route('/delete_flight/<int:flight_id>', methods=['DELETE'])
def delete_flight(flight_id):
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute delete statement
        cursor.execute("DELETE FROM tblflight WHERE id = %s", (flight_id,))
        conn.commit()

        # Return success response
        return jsonify({"message": "Flight record deleted successfully"}), 200
    except mysql.connector.Error as e:
        print(f"Database Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


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

    campus = session.get('campus', '')

    # Pagination variables
    current_page = request.args.get('page', 1, type=int)  # Get current page from URL query, default to 1
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

    # For GET requests, fetch paginated accommodation data only for the user's campus
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get the total count of records for pagination
        cursor.execute("SELECT COUNT(*) AS total FROM tblaccommodation WHERE Campus = %s", (campus,))
        total_records = cursor.fetchone()['total']
        total_pages = (total_records + per_page - 1) // per_page  # Calculate total pages

        # Fetch data with LIMIT and OFFSET for current page
        offset = (current_page - 1) * per_page
        sql = "SELECT * FROM tblaccommodation WHERE Campus = %s LIMIT %s OFFSET %s"
        cursor.execute(sql, (campus, per_page, offset))
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

    # Render the template for GET requests with pagination data
    return render_template('accommodation.html', 
                           accommodation_data=accommodation_data, 
                           current_page=current_page, 
                           total_pages=total_pages)

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

    # Render template and pass data
    return render_template(
        'procurement_dashboard.html',
        food_waste_data=food_waste_data,
        lpg_data=lpg_data,
        forecast_data=forecast_data
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

    # Pagination variables
    page_size = 10  # Number of records per page
    current_page = int(request.args.get('page', 1))  # Current page number from the query parameter
    offset = (current_page - 1) * page_size  # Offset for SQL query

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

    # Fetch existing food data for the logged-in campus with pagination
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Count total records for pagination
        cursor.execute("SELECT COUNT(*) AS total FROM tblfoodwaste WHERE Campus = %s", (campus,))
        total_records = cursor.fetchone()['total']
        total_pages = (total_records + page_size - 1) // page_size  # Calculate total pages

        # Fetch paginated food records for the logged-in campus
        sql = "SELECT * FROM tblfoodwaste WHERE Campus = %s LIMIT %s OFFSET %s"
        cursor.execute(sql, (campus, page_size, offset))
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
        current_page=current_page
    )



@app.route('/lpg_consumption', methods=['GET', 'POST'])
def lpg_consumption():
    if 'loggedIn' not in session:
        return redirect(url_for('login'))

    campus = session.get('campus')  # Get the logged-in campus

    # Set the number of items per page
    items_per_page = 10
    current_page = request.args.get('page', 1, type=int)

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

    # Fetch existing LPG data for the logged-in campus with pagination
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch total record count for pagination calculation
        count_query = "SELECT COUNT(*) as count FROM tbllpg WHERE Campus = %s"
        cursor.execute(count_query, (campus,))
        total_count = cursor.fetchone()['count']
        
        # Calculate total pages
        total_pages = (total_count + items_per_page - 1) // items_per_page  # Ceiling division

        # Offset calculation for current page
        offset = (current_page - 1) * items_per_page

        # Fetch data for the current page
        sql = "SELECT * FROM tbllpg WHERE Campus = %s LIMIT %s OFFSET %s"
        cursor.execute(sql, (campus, items_per_page, offset))
        lpg_data = cursor.fetchall()

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}", "danger")
        lpg_data, total_pages = [], 1

    finally:
        cursor.close()
        conn.close()

    # Render the template with pagination information
    return render_template(
        'lpg_consumption.html', 
        lpg_data=lpg_data, 
        current_page=current_page, 
        total_pages=total_pages
    )

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

        cursor_offices.execute("SELECT DISTINCT Office FROM tblflight WHERE Campus = %s", (campus,))
        offices = [row['Office'] for row in cursor_offices.fetchall()]

        flight_query = "SELECT * FROM tblflight WHERE Campus = %s"
        accommodation_query = "SELECT * FROM tblaccommodation WHERE Campus = %s"
        params = [campus]

        if selected_year:
            flight_query += " AND Year = %s"
            accommodation_query += " AND YearTransact = %s"
            params.append(selected_year)

        if selected_office:
            flight_query += " AND Office = %s"
            accommodation_query += " AND Office = %s"
            params.append(selected_office)

        cursor_flight.execute(flight_query, params)
        total_flight_records = cursor_flight.rowcount
        cursor_flight.fetchall()

        cursor_accommodation.execute(accommodation_query, params)
        total_accommodation_records = cursor_accommodation.rowcount
        cursor_accommodation.fetchall()

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

    return render_template(
        'ea_report.html', 
        flight_data=flight_data,
        accommodation_data=accommodation_data,
        years=years,
        offices=offices,
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

@app.route('/download_excel')
def download_excel():
    # Get filter values
    campus = session.get('campus', '')
    selected_year = request.args.get('year')
    selected_office = request.args.get('office')
    consumption_type = request.args.get('consumption_type')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Determine which table to query based on consumption type
        if consumption_type == 'flight':
            query = "SELECT * FROM tblflight WHERE Campus = %s"
        elif consumption_type == 'accommodation':
            query = "SELECT * FROM tblaccommodation WHERE Campus = %s"
        else:
            return "Invalid consumption type", 400  # Error if consumption type is not valid
        
        params = [campus]

        # Add filters for year and office if provided
        if selected_year:
            if consumption_type == 'flight':
                query += " AND Year = %s"
            elif consumption_type == 'accommodation':
                query += " AND YearTransact = %s"
            params.append(selected_year)
        
        if selected_office:
            query += " AND Office = %s"
            params.append(selected_office)

        # Execute query
        cursor.execute(query, params)
        data = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    # Convert data to pandas DataFrame
    df = pd.DataFrame(data)

    # Create a new Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        sheet_name = 'Flight Data' if consumption_type == 'flight' else 'Accommodation Data'
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    output.seek(0)

    # Send the Excel file to the client
    return send_file(output, as_attachment=True, download_name="Consumption_Report.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')




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
