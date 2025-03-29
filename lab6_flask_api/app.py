from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Homepage route
@app.route('/')
def index():
    return " Flask API is running! Use Postman or visit /form to test."

# Route for HTML form
@app.route('/form')
def form():
    return render_template('form.html')

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Student model
class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    amount_due = db.Column(db.Float)

# POST route (form + JSON)
@app.route('/student', methods=['POST'])
def add_student():
    if request.is_json:
        data = request.json
    else:
        data = request.form
    student = Student(
        student_id=int(data['student_id']),
        first_name=data['first_name'],
        last_name=data['last_name'],
        dob=data['dob'],
        amount_due=float(data['amount_due'])
    )
    db.session.add(student)
    db.session.commit()
    return jsonify({'message': 'Student added'}), 201

# GET one student
@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify({
        'student_id': student.student_id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'dob': student.dob,
        'amount_due': student.amount_due
    })

# GET all students
@app.route('/students', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    return jsonify([
        {
            'student_id': s.student_id,
            'first_name': s.first_name,
            'last_name': s.last_name,
            'dob': s.dob,
            'amount_due': s.amount_due
        } for s in students
    ])

# UPDATE student
@app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(student, key, value)
    db.session.commit()
    return jsonify({'message': 'Student updated'})

# DELETE student
@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted'})

# Run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print(" Database ready.")
    print(" Flask app running at http://127.0.0.1:5000/")
    app.run(debug=True)
