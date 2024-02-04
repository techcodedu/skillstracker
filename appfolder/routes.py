import hashlib
from flask import render_template, request, redirect, url_for, session, flash
from appfolder import app, mysql

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if result > 0:
            data = cur.fetchone()
            password_hash = data['password_hash']
            user_id = data['user_id']
            role = data['role']

            # Debug print (remove this in production)
            print(f"DB hash: {password_hash}")
            print(f"User entered password: {password_candidate}")

            # Hash the candidate password using MD5 and compare
            hashed_candidate = hashlib.md5(password_candidate.encode()).hexdigest()
            if hashed_candidate == password_hash:
                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = user_id
                session['role'] = role

                cur.close()

                if role == 'trainer':
                    return redirect(url_for('trainer_dashboard'))
                elif role == 'student':
                    return redirect(url_for('student_dashboard'))
            else:
                flash('Invalid login')
        else:
            flash('Username not found')

        cur.close()

    return render_template('index.html')
 
 #trainer
@app.route('/trainer_dashboard')
def trainer_dashboard():
    if session.get('logged_in') and session.get('role') == 'trainer':
        # Trainer dashboard logic goes here
        return render_template('trainer_dashaboard.html')
    else:
        return redirect(url_for('login'))

# student
@app.route('/student_dashboard')
def student_dashboard():
    if session.get('logged_in') and session.get('role') == 'student':
        user_id = session.get('user_id')
        
        # Example: Fetch progress data and upcoming modules for the student from the database
        progress_data = get_student_progress(user_id)
        upcoming_modules = get_upcoming_modules(user_id)
        
        return render_template('student_dashboard.html', 
                               progress_data=progress_data, 
                               upcoming_modules=upcoming_modules)
    else:
        return redirect(url_for('login'))

def get_student_progress(user_id):
    # This function should query the database and return the student's progress data.
    # The data returned should be a list of dictionaries where each dictionary represents a competency and its completion percentage.
    
    # Connect to the database
    cur = mysql.connection.cursor()
    
    # Execute the query
    cur.execute("SELECT * FROM progress WHERE student_id = %s", (user_id,))
    
    # Fetch all the results
    progress_records = cur.fetchall()
    
    # Close the connection
    cur.close()
    
    # Process the records into the expected format
    progress_data = []
    for record in progress_records:
        progress_data.append({
            'competency_name': record['competency_name'],
            'percentage': record['completion_percentage']
        })
    
    return progress_data

def get_upcoming_modules(user_id):
    # This function should query the database and return the student's upcoming modules.
    # The data returned should be a list of dictionaries where each dictionary represents a module and its scheduled date.
    
    # Connect to the database
    cur = mysql.connection.cursor()
    
    # Execute the query
    cur.execute("SELECT * FROM modules WHERE student_id = %s AND date >= CURDATE()", (user_id,))
    
    # Fetch all the results
    modules_records = cur.fetchall()
    
    # Close the connection
    cur.close()
    
    # Process the records into the expected format
    upcoming_modules = []
    for record in modules_records:
        upcoming_modules.append({
            'module_name': record['module_name'],
            'date': record['scheduled_date'].strftime('%B %d, %Y') # Formatting the date
        })
    
    return upcoming_modules





@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('login'))
