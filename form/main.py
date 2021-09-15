from flask import request, render_template, Flask
import mysql.connector

app= Flask(__name__)

conn = mysql.connector.connect(host="localhost", user="root", password="", database="form")
cursor = conn.cursor()

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/add_users', methods=['POST'])
def add_user():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    phoneno = request.form.get('PhoneNo')
    address = request.form.get('address')
    email = request.form.get('email')
    pin = request.form.get('pin')
    cursor.execute(
        """INSERT INTO `form` (`firstname`,`lastname`,`phoneno`,`address`,`email`,`pin`) VALUES('{}','{}','{}',
              '{}','{}','{}')""".format(firstname, lastname, phoneno, address, email, pin))
    conn.commit()

    return "Registered successfully"
if __name__ == '__main__':
    app.run(debug=True)
