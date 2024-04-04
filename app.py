from flask import Flask
from flask import render_template
from flask import request
import mysql.connector
from flask_cors import CORS
import json
mysql = mysql.connector.connect(user='web', password='webPass',
  host='127.0.0.1',
  database='student')

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change the HOST IP and Password to match your instance configurations

@app.route("/test")#URL leading to method
def test(): # Name of the method
 return("Hello World!<BR/>THIS IS ANOTHER TEST!") #indent this line

@app.route("/yest")#URL leading to method
def yest(): # Name of the method
 return("Hello World!<BR/>THIS IS YET ANOTHER TEST!") #indent this line

@app.route("/add", methods=['GET', 'POST']) #Add Student
def add():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    print(name,email)
    cur = mysql.cursor() #create a connection to the SQL instance
    s='''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,email)
    app.logger.info(s)
    cur.execute(s)
    mysql.commit()
  else:
    return render_template('add.html')

  return '{"Result":"Success"}'

# Route for updating an item
@app.route("/update", methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        # Retrieve form data
        item_id = request.form['id']
        new_name = request.form['name']
        new_email = request.form['email']
        
        # Connect to MySQL
        cur = mysql.cursor()
        
        # Update the item in the database
        update_query = "UPDATE students SET studentName = %s, email = %s WHERE studentID = %s"
        cur.execute(update_query, (new_name, new_email, item_id))
        mysql.commit()
        mysql.close()

        return '{"Result":"Success"}'
    else:
        # Fetch data to populate the dropdown list
        cursor = mysql.cursor(dictionary=True)
        cursor.execute("SELECT studentID, studentName FROM students")
        results = cursor.fetchall()
        mysql.close()

        return render_template('update.html', results=results)

@app.route("/") #Default - Show Data
def hello(): # Name of the method
  cur = mysql.cursor() #create a connection to the SQL instance
  cur.execute('''SELECT * FROM students''') # execute an SQL statment
  rv = cur.fetchall() #Retreive all rows returend by the SQL statment
  Results=[]
  for row in rv: #Format the Output Results and add to return string
    Result={}
    Result['Name']=row[0].replace('\n',' ')
    Result['Email']=row[1]
    Result['ID']=row[2]
    Results.append(Result)
  response={'Results':Results, 'count':len(Results)}
  ret=app.response_class(
    response=json.dumps(response),
    status=200,
    mimetype='application/json'
  )
  return ret #Return the data in a string format


if __name__ == "__main__":
  #app.run(host='0.0.0.0',port='8080') #Run the flask app at port 8080
  app.run(host='0.0.0.0',port='8080', ssl_context=('cert.pem', 'privkey.pem')) #Run the flask app at port 8080