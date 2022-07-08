# from crypt import methods
import ipaddress
from re import A, X
from turtle import clear
from bson import ObjectId
import dbm
import json
from os import abort
from pickle import PUT
import MySQLdb
from flask import Flask, jsonify, render_template, url_for, session, request, redirect, sessions

from flask_mysqldb import MySQL
from pyrsistent import m
from sympy import re

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Configure db


app.config['MYSQL_HOST'] = 'db4free.net'
app.config['MYSQL_USER'] = 'id18976729_salam'
app.config['MYSQL_PASSWORD'] = '=?K->23]eWbzdg~d'
app.config['MYSQL_DB'] = 'drug-interaction'
mysql = MySQL(app)


# app.config['MYSQL_DATABASE_URI'] = 'mysql+pymysql://id18976729_salamtk : =?K->23]eWbzdg~d : id18976729_drug_interaction@localhost/https://databases.000webhost.com/sql.php?server=1&db=id18976729_drug_interaction'
# mysql = MySQL(app)

@app.route('/register', methods=['POST'])
def index():
    cur = mysql.connection.cursor()
    userDetails = request.json
    if 'username' not in userDetails or 'password' not in userDetails or 'f_name' not in userDetails or 'l_name' not in userDetails or 'phone' not in userDetails or 'gender' not in userDetails or 'day' not in userDetails or 'month' not in userDetails or 'year' not in userDetails or 'GPS' not in userDetails or 'address' not in userDetails or 'email' not in userDetails:
        return 'Please fill your data'

    f_name = userDetails.get('f_name')
    l_name = userDetails.get('l_name')
    password = userDetails.get('password')
    username = userDetails.get('username')
    address = userDetails.get('address')
    phone = userDetails.get('phone')
    day = userDetails.get('day')
    month = userDetails.get('month')
    year = userDetails.get('year')
    GPS = userDetails.get('GPS')
    gender = userDetails.get('gender')
    email = userDetails.get('email')
    # password = userDetails.get('password')
    cur.execute("SELECT * FROM user WHERE username = %s ", (username,))
    u = cur.fetchone()
    if u:
        print(u)
        return 'try another one, this already exist!'
    else:
        cur.execute(
            "INSERT INTO user( f_name,l_name,username, address,phone,gender,email,password,day,month,year,GPS) VALUES( %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (f_name, l_name, username, address, phone, gender, email, password, day, month, year, GPS))
        mysql.connection.commit()
        cur.close()
        return "success"
    # return redirect('/login')


# return render_template('index.html')
###########################
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if 'username' not in data or 'password' not in data:
        return 'Please provide username and passsword'
    # user.append(data)
    # if request.method == 'POST':
    username = data.get('username')
    password = data.get('password')
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM user WHERE username = %s AND  password = %s", (username, password,))
    user = cur.fetchone()
    cur.close()
    if user:
        # Create session data, we can access this data in other routes
        # session['loggedin'] = True
        session['username'] = user['username']
        session['password'] = user['password']
        # return user
        return 'Logged in successfully!'
    else:
        # Account doesnt exist or username/password incorrect
        msg = 'Incorrect username/password!'
        return msg


# return render_template('lo.html')
#
@app.route('/confirm', methods=['POST'])
def confirm():
    data = request.json
    if 'password' not in data:
        return 'Please provide   passsword'
    # user.append(data)
    # if request.method == 'POST':

    password = data.get('password')
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM user WHERE    password = %s", (password,))
    user = cur.fetchone()
    cur.close()
    if user:
        # Create session data, we can access this data in other routes
        # session['loggedin'] = True

        session['password'] = user['password']
        # return user
        return 'confirm successfully!'
    else:
        # Account doesnt exist or username/password incorrect
        msg = 'Incorrect password!'
        return msg


# /////////////////////////////////////////////////////////////////////////////
@app.route('/profile/<id>', methods=['GET'])
def profile(id):
    global user
    cur = mysql.connection.cursor()
    cur.execute("SELECT gender ,username,phone,email FROM user WHERE user_id=%s", id)
    user = cur.fetchone()
    # print(user('f_name'))
    cur.close()

    li = ["gender", "username", "phone", "email"]
    userDict = {key: value for key, value in zip(li, user)}
    print(userDict)
    return userDict


# //////////////////////////
@app.route('/users', methods=['GET'])
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user")
    userDetails = cur.fetchall()
    cur.close()
    print(userDetails)
    return jsonify({"users": userDetails})
    # print(userDetails)


# ////////////////////////////////////////////////
@app.route('/usernames', methods=['GET'])
def usernames():
    global idds
    cur = mysql.connection.cursor()
    cur.execute("SELECT  username  FROM user")
    usernames = cur.fetchall()
    # ///
    # res = {i: {w:  v[0] for w in v}
    # for i, v in enumerate(usernames)}
    # ///
    x = []
    for i in usernames:
        for j in i:
            x.append(j)
    # return x
    cur.close()

    print(len(x))
    # return res
    return jsonify({"all usernames": x})


# //////////////////
@app.route('/userid/<id>', methods=['GET'])
def userid(id):
    # global user
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE user_id=%s", id)
    user = cur.fetchone()
    # print(user('f_name'))
    cur.close()
    if user:
        li = ["id", "system_name", "f_name", "l_name", "username", "address", "phone", "GPS", "day", "month", "year",
              "gender", "email", "password"]
        userDict = {key: value for key, value in zip(li, user)}
        # new_user=dict(zip(li,user))
        # print(new_user)
        # user=new_user
        print(userDict)
        return userDict
    else:
        return "no user with this id " + id


# //////////////

@app.route('/userdeleteid/<id>', methods=['DELETE'])
def userdeleteid(id):
    cur = mysql.connection.cursor()

    try:
        cur.execute("SELECT * FROM user WHERE user_id=%s", id)
        user = cur.fetchone()
        if user:
            cur.execute("DELETE FROM user WHERE  user_id=%s", (id,))
            # user[id+1]=id
            # cur.execute("DELETE FROM user WHERE  user_id==id")
            # cur.close()
            mysql.connection.commit()
            return jsonify({"respons": "user deleted successfly"})
        else:
            return "no user with this id " + id
    except Exception as e:
        print(e)
    finally:
        cur.close()

    # //////////////////delete true


@app.route('/users_delete', methods=['DELETE'])
def user_delete():
    cur = mysql.connection.cursor()
    cur.execute(" DELETE  FROM user ")
    mysql.connection.commit()
    cur.close()
    return jsonify({"respons": " All user deleted successfly"})


# ////////////////////////////////////////////////

@app.route('/update_user/<id>', methods=['PUT'])
def update(id):
    cur = mysql.connection.cursor()
    # cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    h = userid(id)  # returned dictionary contains user data

    userDetails = request.json
    l_name = userDetails.get('l_name') or h.get('l_name')  # and so on
    password = userDetails.get('password') or h.get("password")
    f_name = userDetails.get('f_name') or h.get("f_name")
    username = userDetails.get('username') or h.get("username")
    address = userDetails.get('address') or h.get("address")
    phone = userDetails.get('phone') or h.get("phone")
    day = userDetails.get('day') or h.get("day")
    month = userDetails.get('month') or h.get("month")
    year = userDetails.get('year') or h.get("year")
    gps = userDetails.get('GPS') or h.get("GPS")
    gender = userDetails.get('gender') or h.get("gender")
    email = userDetails.get('email') or h.get("email")
    if h:
        cur.execute(""" UPDATE user SET
         f_name= %s, l_name=%s, password=%s, username=%s,address=%s,
         phone=%s,day=%s,month=%s,year=%s,GPS=%s,gender=%s,email=%s  
         WHERE user_id=%s """,
                    (f_name, l_name, password, username, address, phone, day, month, year, gps, gender, email, id))
        mysql.connection.commit()
        return userid(id)

    else:
        "no user with this id " + id
    cur.close()


#  return userid(id)


# /////////////
# diseases
# //////////true///[]  //////////////
@app.route('/registerdiseas', methods=['POST'])
def registerdiseas():
    diseasDetails = request.json
    if 'diseases_name' not in diseasDetails:
        return 'Please provide  diseases'
    diseases_name = diseasDetails.get('diseases_name')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO diseases (diseases_name) VALUES(%s)", (diseases_name))
    mysql.connection.commit()
    cur.close()
    return jsonify({"respons": " diseases added successfly"})


# ///////////////////////////trueeeeeeeeeeee///////////////////////////////////////////////////
@app.route('/diseases', methods=['GET'])
def diseases():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM diseases")
    rDetails = cur.fetchall()

    cur.close()
    print(rDetails)
    return jsonify({"result": rDetails})
    # print(userDetails)


# ///////////////////////////trueeeeeeeeee//////////////////////////////////////////////////
@app.route('/diseaesid/<id>', methods=['GET'])
def diseasesid(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM diseases WHERE diseases_id=%s", id)
    diseases = cur.fetchone()
    cur.close()
    if diseases:
        li = ["diseases_id", "diseases_name"]
        diseasesDict = {key: value for key, value in zip(li, diseases)}
        # return jsonify({"result":diseases})
        return diseasesDict
    else:
        return "No disease with this id " + id

    # ////////////// ///////////trueeeeeeeee///////////////////////////////////////////////


@app.route('/diseasesdeleteid/<id>', methods=['DELETE'])
def diseasesdeleteid(id):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM diseases WHERE diseases_id=%s", id)
    diseases = cur.fetchone()
    if diseases:
        cur.execute("DELETE FROM  diseases WHERE  diseases_id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"respons": "diseases deleted successfly"})
    else:
        return "No disease with this id " + id

        # return jsonify({"respons":"diseases deleted successfly"})


# /////////////////////////////trueeeeeeee///////////////////////////////////////////
@app.route('/update_diseases/<id>', methods=['PUT'])
def update_diseasse(id):
    cur = mysql.connection.cursor()
    # cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    h = diseasesid(id)  # returned dictionary contains diseases data
    diseasesDetails = request.json
    diseases_name = diseasesDetails.get('diseases_name') or h.get('diseases_name')  # and so on
    if h:
        cur.execute(""" UPDATE diseases SET
           diseases_name= %s 
           WHERE diseases_id=%s """, (diseases_name, id))
        mysql.connection.commit()
        cur.close()
        return diseasesid(id)
    else:
        return "No disease with this id " + id

    # //////////////////delete true


@app.route('/diseases_delete', methods=['DELETE'])
def diseases_delete():
    cur = mysql.connection.cursor()

    cur.execute(" DELETE  FROM diseases ")
    mysql.connection.commit()
    cur.close()
    return jsonify({"respons": " All diseases deleted successfly"})


# return diseases()
# ////////////////////////////////////////////////


# ////////////////////////////////////////////
# medicines_name /take_at///trueeeeeeeeeeeeeee////
@app.route('/add', methods=['POST'])
def add():
    Details = request.json
    # if 'medicines_name' not in Details   or 'take_at' not in  Details:
    #  return 'Please provide medicines_name and time '
    medicines_name = Details.get('medicines_name')
    take_at = Details.get('take_at')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO medicines ( take_at,medicines_name) VALUES(%s, %s )", (take_at, medicines_name))
    # cur.session.add(userDetails)
    # print("asm")
    mysql.connection.commit()
    cur.close()
    return "success"


# ///////////errroe/// Object of type timedelta is not JSON serializable//////////////////////////////////////
@app.route('/medicines', methods=['GET'])
def medicine():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM medicines")
    x = cur.fetchall()
    cur.close()
    print(x)
    return jsonify({"result": x})
    # print(userDetails)


# /////////////////////////////////////////////////////////////////////////////
# ////trueeeeeeeeeeeeeeeeeee///
@app.route('/medid/<id>', methods=['GET'])
def medid(id):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM  medicines WHERE  medicines_id=%s", id)
    medicine = cur.fetchone()
    cur.close()
    # print("s")
    if medicine:
        li = ["diseases_id", "medicine_id", "medicines_name", "take_at"]
        medDict = {key: value for key, value in zip(li, medicine)}
        print(medDict)
        return medDict
    else:
        return "No medicine with this id " + id
        #  return jsonify({"result":medicine})


# //////////////////////////////////////////////////////////////////
@app.route('/medeid', methods=['GET'])
def medeid():
    cur = mysql.connection.cursor()
    cur.execute("SELECT medicines_name FROM  medicines")
    medicine = cur.fetchone()
    cur.close()
    # print("s")
    li = ["medicines_name"]
    medDict = {key: value for key, value in zip(li, medicine)}
    print(medDict)
    return medDict


# ////////////// ////////trueeeeeee//////////////////////////////////////////////////
@app.route('/meddeleteid/<id>', methods=['DELETE'])
def meddeleteid(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM  medicines WHERE  medicines_id=%s", id)
    medicine = cur.fetchone()
    if medicine:
        cur.execute("DELETE FROM  medicines WHERE  medicines_id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"respons": "medicines deleted successfly"})
    else:
        return "No medicine with this id " + id


# /////////////////////////////////////////////////////////////////////
# ///////////////////////trueeeeeeee///////
@app.route('/update_medicine/<id>', methods=['PUT'])
def update_medicine(id):
    cur = mysql.connection.cursor()
    h = medid(id)  # returned dictionary contains medicine data

    medDetails = request.json
    medicines_name = medDetails.get('medicines_name') or h.get('medicines_name')
    take_at = medDetails.get('take_at') or h.get('take_at')  # and so on
    if h:
        cur.execute(""" UPDATE medicines SET
           medicines_name= %s , take_at= %s
           WHERE medicines_id=%s """, (medicines_name, take_at, id))
        mysql.connection.commit()
        cur.close()
        return medid(id)
    else:
        return "No medicine with this id " + id


# /////////////////////trueeeeeeeee//////////////////////////////////////
@app.route('/medicines_delete', methods=['DELETE'])
def medicines_delete():
    cur = mysql.connection.cursor()
    cur.execute(" DELETE  FROM medicines ")
    mysql.connection.commit()
    cur.close()
    return jsonify({"respons": " All medicines deleted successfly"})


# ///////////////////////////////
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


# /////////////////////////////////////////////////////

if __name__ == '__main__':
    app.run(debug=True)