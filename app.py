from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from model import predict_car_type
import time
import re

# ---------- Allowed Image Extensions ----------
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------- App Configuration ----------
app = Flask(__name__)
app.secret_key = 'd2f58ed4aadc92faae0c29e02bfa5b56bd9235458c4fd273'
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.permanent_session_lifetime = timedelta(days=30)

# ---------- DB Helper ----------
def get_db_connection():
    conn = sqlite3.connect('admin.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Home ----------
@app.route('/')
def home():
    return render_template('home.html')

# ---------- Prediction ----------
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('upload.html')

    image = request.files.get('image')
    if not image or not allowed_file(image.filename):
        flash('Invalid file type. Please upload a valid image file.', 'danger')
        return redirect(request.url)

    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    try:
        start_time = time.time()
        prediction = predict_car_type(filepath)
        end_time = time.time()
        duration = round(end_time - start_time, 3)
    except Exception as e:
        flash(f"Prediction failed: {str(e)}", 'danger')
        return redirect(request.url)

    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO predictions (filename, result, timestamp, duration) VALUES (?, ?, ?, ?)",
        (filename, prediction, datetime.now(), duration)
    )
    conn.commit()
    conn.close()

    return render_template('prediction.html', filename=filename, result=prediction)

# ---------- Manager Dashboard ----------
@app.route('/manager')
def manager():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    class_filter = request.args.get('class')
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    query = "SELECT filename, result, timestamp, duration FROM predictions"
    conditions = []
    params = []

    if class_filter and class_filter != 'All':
        conditions.append("result = ?")
        params.append(class_filter)

    if start_date:
        conditions.append("DATE(timestamp) >= ?")
        params.append(start_date)

    if end_date:
        conditions.append("DATE(timestamp) <= ?")
        params.append(end_date)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY timestamp DESC"

    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    predictions = cursor.fetchall()

    cursor.execute("SELECT DISTINCT result FROM predictions")
    all_classes = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT result, COUNT(*) FROM predictions GROUP BY result")
    class_distribution = cursor.fetchall()

    cursor.execute("SELECT DATE(timestamp), COUNT(*) FROM predictions GROUP BY DATE(timestamp)")
    date_counts = cursor.fetchall()

    cursor.execute("""
        SELECT DATE(timestamp), result, COUNT(*) 
        FROM predictions 
        GROUP BY DATE(timestamp), result 
        ORDER BY DATE(timestamp)
    """)
    class_per_day = cursor.fetchall()

    cursor.execute("SELECT result, COUNT(*) as total FROM predictions GROUP BY result ORDER BY total DESC LIMIT 5")
    top_classes = cursor.fetchall()

    conn.close()

    return render_template(
        'manager.html',
        predictions=predictions,
        all_classes=all_classes,
        class_distribution=class_distribution or [('No Data', 1)],
        date_counts=date_counts or [('No Data', 1)],
        class_per_day=class_per_day or [('No Data', 'None', 1)],
        top_classes=top_classes or [('No Data', 1)],
        current_class=class_filter or 'All',
        current_start=start_date or '',
        current_end=end_date or ''
    )

# ---------- Signup ----------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        if len(username) < 5:
            flash('Username must be at least 5 characters long.', 'danger')
            return render_template('signup.html')

        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
        if not re.match(password_pattern, password):
            flash('Password must contain uppercase, lowercase, number, and symbol.', 'danger')
            return render_template('signup.html')

        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO admins (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            flash('Account created successfully.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'danger')
        finally:
            conn.close()

    return render_template('signup.html')

# ---------- Login ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember')

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['admin_logged_in'] = True
            session['username'] = username
            if remember:
                session.permanent = True
            return redirect(url_for('manager'))
        else:
            error = 'Invalid username or password.'

    return render_template('login.html', error=error)

# ---------- Logout ----------
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('username', None)
    return redirect(url_for('home'))

# ---------- Run ----------
if __name__ == '__main__':
    app.run(debug=True)
