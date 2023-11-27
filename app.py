from flask import Flask, request, jsonify
from database import Database, CursorFromConnectionFromPool
import os

app = Flask(__name__)

@app.route('/')
def initialise():
 with app.app_context():
     Database.initialise(user='postgres', password='19930214', 
                      database='iot', host='localhost', port='5432')
     return jsonify({'message': 'Database initialized successfully'}), 200

@app.route('/fetch', methods=['GET'])
def get_schools():
 with CursorFromConnectionFromPool() as cursor:
     cursor.execute('SELECT * FROM schools')
     data = cursor.fetchall()
     print(data) # Print the data to the console
     return jsonify(data), 200

@app.route('/', methods=['POST'])
def add_school():
 name = request.json['name']
 location = request.json['location']
 with CursorFromConnectionFromPool() as cursor:
     cursor.execute('INSERT INTO schools (name, address) VALUES (%s, %s)', 
                 (name, location))
     return jsonify({'message': 'Successfully added school'}), 200

@app.route('/setup', methods=['GET'])
def setup():
 Database.initialise(user='postgres', password='19930214', 
                database='iot', host='localhost', port='5432')
 with CursorFromConnectionFromPool() as cursor:
    cursor.execute('''CREATE TABLE schools( 
                id SERIAL PRIMARY KEY, 
                name VARCHAR(100), 
                address VARCHAR(100))''')
    return jsonify({'message': 'Successfully created table'}), 200

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=os.getenv('PORT', 3000))










# from flask import Flask, request, jsonify
# from database import Database, CursorFromConnectionFromPool
# import os

# app = Flask(__name__)

# @app.route('/')
# def initialise():
#    with app.app_context():
#        Database.initialise(user='postgres', password='19930214', 
#                           database='iot', host='localhost', port='5432')

# @app.route('/', methods=['GET'])
# def get_schools():
#    with CursorFromConnectionFromPool() as cursor:
#        cursor.execute('SELECT * FROM schools')
#        data = cursor.fetchall()
#        return jsonify(data), 200

# @app.route('/', methods=['POST'])
# def add_school():
#    name = request.json['name']
#    location = request.json['location']
#    with CursorFromConnectionFromPool() as cursor:
#        cursor.execute('INSERT INTO schools (name, address) VALUES (%s, %s)', 
#                      (name, location))
#        return jsonify({'message': 'Successfully added school'}), 200

# @app.route('/setup', methods=['GET'])
# def setup():
#   Database.initialise(user='postgres', password='19930214', 
#                     database='iot', host='localhost', port='5432')
#   with CursorFromConnectionFromPool() as cursor:
#       cursor.execute('''CREATE TABLE schools( 
#                     id SERIAL PRIMARY KEY, 
#                     name VARCHAR(100), 
#                     address VARCHAR(100))''')
#       return jsonify({'message': 'Successfully created table'}), 200


# if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=os.getenv('PORT', 3000))
