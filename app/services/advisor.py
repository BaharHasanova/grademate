from flask import jsonify, request
from app.models.advisor import Advisor
from app.models.student import Student
from app.models.semester import Semester
from app.models.program import Program
from app.models.subject import Subject
from app import db
from sqlalchemy import select
from flask_jwt_extended import JWTManager, jwt_required, create_access_token



def register_advisor(**kwargs):
    if not request.json:
        return jsonify(400, "Request must be JSON")

    _email = request.json.get("email")
    _password = request.json.get("password")
    _advisor_id = request.json.get("advisor_id")
    _full_name = request.json.get("full_name")

    advisor_exist = db.session.execute(select(Advisor).where(Advisor.email == _email)).scalars().first()

    if advisor_exist:
        return jsonify(400, "Advisor already exists")

    new_advisor = Advisor(
        advisor_id = _advisor_id,
        email = _email,
        full_name = _full_name
    )

    new_advisor.set_password(password=_password)

    db.session.add(new_advisor)
    db.session.commit()

    return jsonify(new_advisor.serialize())



def login_advisor(**kwargs):
    if not request.json:
        return jsonify({"message":"Request must be JSON"}), 400

    _email = request.json.get("email")
    _password = request.json.get("password")

    advisor_exist = db.session.execute(select(Advisor).where(Advisor.email == _email)).scalars().first()

    if not advisor_exist:
        return jsonify({"message":"Advisor doesn't exist"}), 404

    if advisor_exist and advisor_exist.check_password_hash(password=_password):
        additional_claims = {"email": _email, "name": advisor_exist.full_name, "advisor_id": advisor_exist.advisor_id}
        access_token = create_access_token(identity=_email, additional_claims= additional_claims)
        return jsonify(
            {
                "advisor": advisor_exist.serialize(),
                "token": access_token
            }
        )
    else:
        return jsonify({"message":"Incorrect email or password"}), 400



def get_advisor_students(**kwargs):
    advisor_id = request.args.get("advisor_id")

    advisor_exist = db.session.execute(select(Advisor).where(Advisor.advisor_id == advisor_id)).scalars().first()

    if not advisor_exist:
        return jsonify({"message": "Advisor not found"}), 404
    
    advisor_students = db.session.execute(select(Student).where(Student.advisor_id == advisor_id)).scalars().all()

    if not advisor_students:
        return jsonify([])

    
    advisor_students_serialized = [advisor_student.serialize() for advisor_student in advisor_students]

    return jsonify(advisor_students_serialized), 200



def get_advisor_student_semester(**kwargs):
    student_id = request.args.get("student_id")

    student_exist = db.session.execute(select(Student).where(Student.student_id== student_id)).scalars().first()

    if not student_exist:
        return jsonify({"message":"Student not found"}), 404

    student_semesters = db.session.execute(
        select(Semester)
        .join(Program, Semester.program_id == Program.program_id)
        .join(Student, Program.program_id == Student.program_id)
        .where(Student.student_id == student_id)
        ).scalars().all()

    if not student_semesters:
        return jsonify([])

    student_semesters_serialized = [student_semester.serialize() for student_semester in student_semesters]

    return jsonify(student_semesters_serialized), 200


def get_advisor_student_semester_class(**kwargs):
    semester_id = request.args.get("semester_id")

    semester_exist = db.session.execute(select(Semester).where(Semester.semester_id == semester_id)).scalars().first()

    if not semester_exist:
        return jsonify({"message":"Semester not found"}), 404
    
    semester_subjects = db.session.execute(select(Subject).where(Subject.semester_id == semester_id)).scalars().all()

    if not semester_subjects:
        return jsonify([]), 200

    semester_subjects_serialized = [semester_subject.serialize() for semester_subject in semester_subjects]

    return jsonify(semester_subjects_serialized), 200