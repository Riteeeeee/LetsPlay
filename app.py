from flask import Flask,url_for,redirect,request,render_template;
import sqlite3
import jsonify

app=Flask(__name__)
# con=sqlite3.connect("registration.db")
# con.execute("create table registration(username VARCHAR,phone INTEGER,gender CHAR,blood VARCHAR,email TEXT)")
details=[]

@app.route("/")
def home():
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def index_func():
    if request.method == 'POST':
        return redirect(url_for('index.html'))
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register_func():
    if request.method == 'POST':
        return redirect(url_for('index.html'))
    return render_template('register.html')
@app.route('/check_sports', methods=['GET', 'POST'])
def checksports():
    if request.method == 'POST':
        return redirect(url_for('sports.html'))
    return render_template('sports.html')
@app.route('/check_free', methods=['GET', 'POST'])
def checkfreeslot():
    if request.method == 'POST':
        return redirect(url_for('cal.html'))
    return render_template('cal.html')
databases={'ritee':'123'}
@app.route('/books', methods=['GET', 'POST'])
def books():
    global tim
    tim=request.form['slot']
    print(tim)
    if request.method == 'POST':
        return render_template('register.html')

@app.route('/store-location', methods=['POST'])
def store_location():
    global location
    location = request.form['location']  # Get the location from the form
    print(f"Location stored: {location}")  # Print the location to the console (or handle it as needed)
    details.append(location)
    return render_template('sports.html')
    # You can store the location in a variable or database, or process it further here



@app.route('/submit-sports', methods=['POST'])  # Updated endpoint name
def submit_sports():
    global sports
    sports = request.form['sports']  # Get the sports from the form
    print(f"Sports stored: {sports}")  # Print the sports to the console (or handle it as needed)
    details.append(sports)
    # You can store the sports in a variable or database, or process it further here
    return render_template('court.html')

@app.route('/submit-courts', methods=['POST'])  # Updated endpoint name
def submit_courts():
    global courts
    courts = request.form['courts']  # Get the courts from the form
    print(f"courts stored: {courts}")  # Print the sports to the console (or handle it as needed)
    details.append(courts)
    # You can store the sports in a variable or database, or process it further here
    return render_template('cal.html')


@app.route('/form_login',methods=['POST','GET'])
def login():
    name=request.form['username']
    passwrd=request.form['password']
    print(name,passwrd)
    if name not in databases:
        return render_template('login.html')
    else:
        if databases[name]!=passwrd:
            return render_template('login.html')
        else:
                # Connect to the SQLite database
                conn = sqlite3.connect('registrations.db')
                cursor = conn.cursor()

                # Execute a query to retrieve data from the database
                cursor.execute('SELECT * FROM registration')
                data = cursor.fetchall()

                # Close the database connection
                cursor.close()
                conn.close()

                # Render the HTML template and pass the data to it
                return render_template('user_response.html', data=data)

registration=[]
@app.route('/form_register',methods=['POST','GET'])
def register():
   print("hello")
   if request.method=="POST":
      try:
        naam=request.form['username']
        number=request.form['phone']
        mail=request.form['email']
        action="REQUEST"
        with sqlite3.connect("registrations.db") as con:
            cur=con.cursor()
            cur.execute("INSERT into registration VALUES(?,?,?,?,?)",(naam,number,mail,sports,location))
            con.commit()
            print("OPERATION SUCCESSFUL")
        with sqlite3.connect("slotdetails.db") as con:
            cur=con.cursor()
            cur.execute("INSERT into slotdetails VALUES(?,?,?,?,?)",(location,sports,selected_date,tim,courts))
            con.commit()
            print("OPERATION SUCCESSFUL")

      except: con.rollback()
      finally:
          con.close()
          return render_template("index.html")
@app.route('/read_more', methods=['GET', 'POST'])
def read_more_func():
    if request.method == 'POST':
        return redirect(url_for('index.html'))
    return render_template('read_more.html')

@app.route('/FAQ_func', methods=['GET', 'POST'])
def FAQ_func():
    if request.method == 'POST':
        return redirect(url_for('index.html'))
    return render_template('FAQ.html')
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        return redirect(url_for('index.html'))
    return render_template('contact_us.html')
@app.route('/donation', methods=['GET', 'POST'])
def donation():
    if request.method == 'POST':
        return redirect(url_for('index.html'))
    return render_template('donation.html')
@app.route('/form_send',methods=['POST','GET'])
def Send():
    send_user=request.form['send_name']
    send_gmail=request.form['send_email']
    send_mess=request.form['send_mess']
    import smtplib
    send = "project.feedback.02@gmail.com"
    rec = "project.feedback.02@gmail.com"
    pas = "yzay obwk fisz kpcj"
    message = f"Subject: {send_gmail}\n\nMR/MRS {send_user} messaged you: {send_mess}"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(send, pas)
    server.sendmail(send, rec, message)


    return  render_template('index.html')


@app.route('/get_email', methods=['POST'])
def get_email():
    email = request.form.get('email_fetch')
    import smtplib
    send_gmail="DONATION REQUEST"
    send = "project.feedback.02@gmail.com"
    rec = email
    print(email,send)
    pas = "yzay obwk fisz kpcj"
    message = f"Subject: {send_gmail}\n\nThank you for registering for donation, We would like to inform you tht there is need for urgent stem cell donation.If you are interested in donation do contact us. Thanks and regards\n D visit us at https://wewin.onrender.com"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(send, pas)
    server.sendmail(send,rec,message)
    conn = sqlite3.connect('registration.db')
    cursor = conn.cursor()

    # Execute a query to retrieve data from the database
    cursor.execute('SELECT * FROM registration')
    data = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Render the HTML template and pass the data to it
    return render_template('user_response.html', data=data)

@app.route('/submit-date', methods=['POST'])
def submit_date():
    global selected_date
    selected_date = request.form['selected_date']
    print(selected_date)  # Debug: print the selected date

    # Connect to the SQLite database
    conn = sqlite3.connect('slotdetails.db')
    cursor = conn.cursor()
    print(location,sports)
    # Corrected SQL query (changed 'fROM' to 'FROM')
    cursor.execute('SELECT * FROM slotdetails')
    results = cursor.fetchall()  # Fetch all results
    conn.close()  # Close the database connection

    print(results)  # Debug: print the results from the database

    # Initialize available and booked slots
    available_slots = ['4PM-5PM', '5PM-6PM', '6PM-7PM', '7PM-8PM', '8PM-9PM', '9PM-10PM']
    booked_slots = [row[3] for row in results if row[2] == selected_date and row[0]==location and row[1]==sports and row[4]==courts]  # Ensure index matches your schema

    # Remove booked slots from available slots
    for slot in booked_slots:
        if slot in available_slots:
            available_slots.remove(slot)

    print(available_slots)  # Debug: print available slots after removal

    # Pass available slots to the template
    return render_template('cal.html', available_slots=available_slots)

