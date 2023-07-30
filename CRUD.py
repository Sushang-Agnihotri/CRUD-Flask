from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'student_data'
app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 

mysql = MySQL(app)

#Create a student
@app.route('/api/students', methods=['GET','POST'])
def create_student():
    data = request.get_json()

    stu_id = data.get('stu_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    dob = data.get('dob')
    amount_due = data.get('amount_due')

    if not stu_id or not first_name or not last_name or not dob or not amount_due:
        return jsonify({'error': 'All fields are required.'}), 400

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO stu (stu_id, first_name, last_name, dob, amount_due) VALUES (%s, %s, %s, %s, %s)",
        (stu_id, first_name, last_name, dob, amount_due)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Student created successfully.'}), 201


#Getting a student data from id
@app.route('/api/students/<int:stu_id>', methods=['GET'])
def get_student(stu_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stu WHERE stu_id = %s", (stu_id,))
    student = cur.fetchone()
    cur.close()

    if not student:
        return jsonify({'error': 'Student not found.'}), 404

    return jsonify(student), 200


#Updating a student record
@app.route('/api/students/<int:stu_id>', methods=['PUT'])
def update_student(stu_id):
    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    dob = data.get('dob')
    amount_due = data.get('amount_due')

    if not first_name or not last_name or not dob or not amount_due:
        return jsonify({'error': 'All fields are required.'}), 400

    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE stu SET first_name = %s, last_name = %s, dob = %s, amount_due = %s WHERE stu_id = %s",
        (first_name, last_name, dob, amount_due, stu_id)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Student updated successfully.'}), 200

#Deleting a student record
@app.route('/api/students/<int:stu_id>', methods=['DELETE'])
def delete_student(stu_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM stu WHERE stu_id = %s", (stu_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Student deleted successfully.'}), 200


#Fetching all student records
@app.route('/api/students', methods=['GET'])
def get_all_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stu")
    students = cur.fetchall()
    cur.close()

    if not students:
        return jsonify({'message': 'No students found.'}), 404

    return jsonify(students), 200


if __name__ == '__main__':
    app.run(debug=True)
