# Step 1 Create a new Flask project and set up a virtual environment:
#1.Create Flask Project
# mkdir fitness_center
# cd fitness_center
# python3 -m venv venv 
# venv\Scripts\activate

# 2.Install Dependencies:
# pip install Flask Flask-Marshmallow mysql-connector-python

# 3.Setup Database Connection and Models -  Use the Members and WorkoutSessions tables.

# Step 2 Implementing Flask Application.
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

# Database Configuration
app.config['DB_HOST'] = 'localhost'
app.config['DB_NAME'] = 'fitness_center_db'
app.config['DB_USER'] = 'root'
app.config['DB_PASSWORD'] = 'password'

# Database Connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=app.config['DB_HOST'], 
            database=app.config['DB_NAME'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'] 
        )
        return connection
    except Error as e:
        print(f"error connecting to MYSQL: {e}")
        return None
    
# Marshmallow Schema Definitions
class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'phone')
class WorkoutSessionsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'member_id', 'date', 'duration', 'type')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
session_schema = WorkoutSessionsSchema()
sessions_schema = WorkoutSessionsSchema(many=True)


# Task 2 Implementing CRUD Operations for Members
# Add a New Member
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    name, email, phone = data.get('name'), data.get('email'), data.get('phone')
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO Members (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        connection.commit()
        return jsonify({"message": "Member added successfully "}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()

# Retrieve Member by ID
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Members WHERE id = %s", (id,))
        member = cursor.fetchone()
        if member:
            return member_schema.jsonify(member), 200
        return jsonify({"error": "Member not found"}), 404
    except Error as e:
        return ({"error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()

# Update Member
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    name, email, phone = data.get('name'), data.get('email'), data.get('phone')
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE Members SET name = %s, email = %s, phone =%s", (name, email, phone, id))
        connection.commit()
        return jsonify({"message": "Member updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()

# Delete Member
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM Member WHERE id = %s", (id))
        connection.commit()
        return jsonify({"message": "Member deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()

# Task 3: Managing Workout Sessions
# Schedule a New Workout Session 
@app.route('/workouts', methods=['POST'])
def schedule_workout():
    data = request.get_json()
    member_id, date, duration, workout_type = data.get('member_id'), data.get('date'), date.get('duration'), data.get('type')
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO WorkoutSessions (member_id, date, duration, type)  VALUES (%s, %s, %s)", (member_id, date, duration, workout_type))
        connection.commit()
        return jsonify({"message": "Workout session Scheduled"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()

# Retrieve All Workout Session for a Member
@app.route('/workouts/<int:member_id>',  methods=['GET'])
def get_workouts_for_member(member_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
       cursor.execute("SELECT * FROM WorkoutSessions WHERE member_id = %s", (member_id,))
       sessions = cursor.fetchall()
       return sessions_schema.jsonify(sessions), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()

# update Workout Session
@app.route('/workouts/<int:id>',  methods=['PUT'])
def update_workout(id):
    data = request.get_json()
    date, duration, workout_type = data.get('date'), data.get('duration'), data.get('type')
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE WorkoutSessions SET date = %s, duration = $s, type = WHERE id = %s", (date, duration, workout_type, id))
        connection.commit()
        return jsonify({"message": "Workout session updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()
    

# Delete Workout Session
@app.route('/workouts/<int:id>',  methods=['DELETE'])
def delete_workout(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM  WorkoutSessions WHERE id = %s", (id,))
        connection.commit()
        return jsonify({"message": "Workout session deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
    
