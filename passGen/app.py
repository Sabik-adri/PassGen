from flask import Flask, render_template, request, redirect, url_for,session
from pymongo import MongoClient

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'


# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['PassGen']
collection = db['PasswordTable']
users_table = db['login']

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        form_data = dict(request.form)
        form_username = form_data["username"]
        form_password = form_data["password"]
        db_user = users_table.find_one({"username": form_username})
        if db_user is None:
            return "Username not found"
        if form_password != db_user["password"]:
            return "Password did not match"
        session["logged_in"] = True
        session["username"] = form_username
        return redirect("/index")  # Redirect to the dashboard after successful login
    if "logged_in" in session:
        return redirect("/index")  # If already logged in, redirect to the dashboard
    return render_template("login.html")


    
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect('/login')  # Redirect to the login page

@app.route('/index')
def dashboard():
    if "logged_in" in session:
        return render_template("index.html")
    return redirect('/login')  # Redirect to the login page if not logged in

@app.route('/index', methods=['GET', 'POST'])
def index():
    if  request.method == 'POST':
        id_val = request.form['id']
        location = request.form['location']
        client_name = request.form['clientName']
        phone = request.form['phone']
        anydesk = request.form['anydesk']
        generated_password = request.form['generatedPassword']

        data = {
            'id': id_val,
            'location': location,
            'client_name': client_name,
            'phone': phone,
            'anydesk': anydesk,
            'generated_password': generated_password
        }

        collection.insert_one(data)
#       return "Form data saved to MongoDB!"

        # if "logged_in" in session:
        #     return render_template("index.html")
        # return redirect('/login')
        return render_template('index.html')
    # else:
    #     return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def add_user():
    if request.method == "POST":
        form_data = dict(request.form)
        users_table.insert_one(form_data)
        return redirect(url_for('login'))
    return render_template('signup.html')



@app.route('/table')
def table():
    # Retrieve data from MongoDB
    data_from_mongo = list(collection.find())
    if "logged_in" in session:
            return render_template('table.html', data=data_from_mongo)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
