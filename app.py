from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import mysql.connector
from mysql.connector import DatabaseError


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL user
    password="CommandO2411",  # Replace with your MySQL password
    database="ssts"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hardcoded check for admin credentials
        if username == 'admin' and password == 'admin':
            session['username'] = username
            session['role'] = 'admin'
            return redirect(url_for('courses'))

        # Check credentials for regular users
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('profile'))
        else:
            return "Invalid credentials"

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        cursor.close()

        if existing_user:
            return "Username already exists, please choose a different one."

        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, 'user')", (username, password))
        db.commit()
        cursor.close()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']

        # Check if the user exists
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user:
            session['reset_username'] = username
            cursor.close()
            return redirect(url_for('reset_password'))
        else:
            cursor.close()
            return "User not found. Please try again."

    return render_template('forgot_password.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_username' not in session:
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Check if the new password and confirm password match
        if new_password != confirm_password:
            return "Passwords do not match. Please try again."

        # Update the password in the database
        cursor = db.cursor()
        cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, session['reset_username']))
        db.commit()
        cursor.close()

        # Clear the session variable
        session.pop('reset_username', None)

        return redirect(url_for('login'))

    return render_template('reset_password.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/events', methods=['GET', 'POST'])
def events():
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    
    # Only admins can add events
    if request.method == 'POST' and session.get('role') == 'admin':
        event_title = request.form['event_name']
        event_date = request.form['event_date']
        event_location = request.form['event_location']
       
        event_img_url = request.form['img_url']

        cursor.execute(
            "INSERT INTO events (name, date, location, img_url) VALUES (%s, %s, %s, %s)",
            (event_title, event_date, event_location,  event_img_url)
        )
        db.commit()

    # Retrieve all events
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()

    # Get the current user’s subscribed events
    subscribed_event_ids = set()
    if 'username' in session:
        cursor.execute(
            "SELECT event_id FROM subscriptions WHERE user_id = (SELECT id FROM users WHERE username = %s)",
            (session['username'],)
        )
        subscribed_event_ids = {row['event_id'] for row in cursor.fetchall()}

    # Add a field to each event to check if the user is subscribed
    for event in events:
        event['is_subscribed'] = event['id'] in subscribed_event_ids

    cursor.close()
    return render_template('events.html', events=events, is_admin=(session.get('role') == 'admin'))


@app.route('/delete_event', methods=['POST'])
def delete_event():
    if 'username' not in session or session.get('role') != 'admin':
        return jsonify({'status': 'Access Denied'}), 403

    event_id = request.form['event_id']
    cursor = db.cursor()
    
    # Attempt to delete the event
    cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
    db.commit()
    cursor.close()
    
    # Return a valid JSON response indicating success
    return jsonify({'status': 'Event removed'})

   

@app.route('/subscribe_event/<int:event_id>', methods=['POST'])
def subscribe_event(event_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
    user = cursor.fetchone()

    if user:
        user_id = user['id']
        try:
            # Insert into the subscription table (trigger will prevent duplicates)
            cursor.execute("INSERT INTO subscriptions (user_id, event_id) VALUES (%s, %s)", (user_id, event_id))
            db.commit()
        except mysql.connector.errors.DatabaseError as e:
            # If the trigger prevents a duplicate subscription, show the appropriate message
            if 'Duplicate subscription not allowed' in str(e):
                flash('You have already subscribed to this event!', 'error')
            else:
                flash('An error occurred while processing your subscription.', 'error')
            db.rollback()
        
        cursor.close()
        return redirect(url_for('events'))
    else:
        return "User not found", 404



    cursor.close()
    return redirect(url_for('profile'))


@app.route('/courses', methods=['GET', 'POST'])
def courses():
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    
    # Only admins can add courses
    if request.method == 'POST' and session.get('role') == 'admin':
        course_title = request.form['course_name']
        course_url = request.form['course_url']

        try:
            cursor.execute(
                "INSERT INTO courses (title, course_url) VALUES (%s, %s)", 
                (course_title, course_url)
            )
            db.commit()
        except mysql.connector.Error as err:
            if "Duplicate entry" in str(err):
                error_message = "Course already exists. Cannot add duplicate course."
            else:
                error_message = f"An error occurred: {err}"
            cursor.close()
            return render_template('courses.html', error_message=error_message)

    # Retrieve all courses
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    # Get the current user's subscribed courses
    subscribed_course_ids = set()
    if 'username' in session:
        cursor.execute(
            "SELECT course_id FROM course_subscriptions WHERE user_id = (SELECT id FROM users WHERE username = %s)",
            (session['username'],)
        )
        subscribed_course_ids = {row['course_id'] for row in cursor.fetchall()}

    # Add a field to each course to check if the user is subscribed
    for course in courses:
        course['is_subscribed'] = course['id'] in subscribed_course_ids

    cursor.close()
    return render_template('courses.html', courses=courses, is_admin=(session.get('role') == 'admin'))



@app.route('/delete_course', methods=['POST'])
def delete_course():
    if 'username' not in session or session.get('role') != 'admin':
        return jsonify({'status': 'Access Denied'}), 403

    course_id = request.form['course_id']  # Changed from 'title' to 'course_id'
    cursor = db.cursor()
    cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
    db.commit()
    cursor.close()

    return jsonify({'status': 'Course removed'})


@app.route('/subscribe_course/<int:course_id>', methods=['POST'])
def subscribe_course(course_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
    user = cursor.fetchone()

    if user:
        user_id = user['id']
        try:
            # Insert into the course_subscriptions table (trigger will prevent duplicates)
            cursor.execute("INSERT INTO course_subscriptions (user_id, course_id) VALUES (%s, %s)", (user_id, course_id))
            db.commit()
        except mysql.connector.errors.DatabaseError as e:
            # If the trigger prevents a duplicate subscription, show the appropriate message
            if 'Duplicate subscription not allowed' in str(e):
                flash('You have already subscribed to this course!', 'error')
            else:
                flash('An error occurred while processing your subscription.', 'error')
            db.rollback()
        
        cursor.close()
        return redirect(url_for('courses'))
    else:
        return "User not found", 404
    cursor.close()
    return redirect(url_for('profile'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
        user_result = cursor.fetchone()

        if not user_result:
            return "User not found", 404
        user_id = user_result['id']

        # Fetch subscribed events
        cursor.execute("""
            SELECT events.id, events.name, events.date, events.location, events.img_url
            FROM events
            JOIN subscriptions ON events.id = subscriptions.event_id
            WHERE subscriptions.user_id = %s
        """, (user_id,))
        subscribed_events = cursor.fetchall()

        # Fetch subscribed courses
        cursor.execute("""
            SELECT courses.id, courses.title, courses.course_url
            FROM courses
            JOIN course_subscriptions ON courses.id = course_subscriptions.course_id
            WHERE course_subscriptions.user_id = %s
        """, (user_id,))
        subscribed_courses = cursor.fetchall()

        # Fetch counts of subscribed events and courses
        cursor.execute("""
            SELECT COUNT(*) AS event_count FROM subscriptions WHERE user_id = %s
        """, (user_id,))
        event_count = cursor.fetchone()['event_count']

        cursor.execute("""
            SELECT COUNT(*) AS course_count FROM course_subscriptions WHERE user_id = %s
        """, (user_id,))
        course_count = cursor.fetchone()['course_count']

        # Add a new project if a project name is provided
        if request.method == 'POST':
            project_name = request.form['project']
            cursor.execute("INSERT INTO projects (user_id, project_name) VALUES (%s, %s)", (user_id, project_name))
            db.commit()

        return render_template('profile.html', 
                               subscribed_events=subscribed_events, 
                               subscribed_courses=subscribed_courses,
                               event_count=event_count, 
                               course_count=course_count)

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        db.rollback()
        return f"An error occurred: {e}", 500

    finally:
        cursor.close()




@app.route('/delete_account', methods=['POST'])
def delete_account():
    user_id = request.json.get('user_id')

    if user_id:
        try:
            cursor = db.cursor()

            # Delete from subscriptions table
            cursor.execute("DELETE FROM subscriptions WHERE user_id = %s", (user_id,))
            
            # Delete from course_subscriptions table
            cursor.execute("DELETE FROM course_subscriptions WHERE user_id = %s", (user_id,))
            
            # Delete user from the users table
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

            # Commit changes
            db.commit()

            # Clear session by popping specific keys
            session.pop('username', None)
            session.pop('user_id', None)
            session.pop('role', None)

            return jsonify({"message": "Account deleted successfully"}), 200

        except Exception as e:
            db.rollback()
            return jsonify({"message": str(e)}), 500

    return jsonify({"message": "User ID not found"}), 400



if __name__ == '__main__':
    app.run(debug=True)
