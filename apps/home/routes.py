# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, redirect, url_for, jsonify, Response
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import db
from apps.authentication.models import Class, Attendance
from io import StringIO, BytesIO
from itertools import cycle
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import random
import string

@blueprint.route('/index')
@login_required
def index():
    classes = Class.query.filter_by(archived=False).all()
    class_attendance_counts = db.session.query(
        Class.course_code,
        Class.course_class,
        db.func.count(Attendance.matricula)
    ).join(
        Attendance,
        db.and_(Class.course_code == Attendance.course_code, Class.course_class == Attendance.course_class),
        isouter=True
    ).filter(Class.archived == False).group_by(Class.course_code, Class.course_class).all()

    # Convert class_attendance_counts to a dictionary for easy access in the template
    attendance_dict = {(course_code, course_class): count for course_code, course_class, count in class_attendance_counts}

    # Possible color classes and icons
    color_classes = ['bg-gradient-primary', 'bg-gradient-secondary', 'bg-gradient-info', 'bg-gradient-success', 'bg-gradient-warning', 'bg-gradient-danger']
    icons = ['weekend', 'school', 'landscape', 'home', 'flight', 'pets']

    # Create cyclers
    color_cycler = cycle(color_classes)
    icon_cycler = cycle(icons)

    # Assign color and icon to each class in sequence
    for cls in classes:
        cls.color_class = next(color_cycler)
        cls.icon = next(icon_cycler)

    return render_template('home/index.html', segment='index', classes=classes, attendance_dict=attendance_dict)

@blueprint.route('/add_class', methods=['GET', 'POST'])
@login_required
def add_class():
    if request.method == 'POST':
        class_name = request.form['name']
        #generate a unique secret code 4 to 8 digits long, including numbers and letter
        secret_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        #secret_code = request.form['secret']
        course_code = request.form['course_code']
        course_class = request.form['course_class']
        new_class = Class(name=class_name, secret_code=secret_code, course_code=course_code, course_class=course_class)
        db.session.add(new_class)
        db.session.commit()
        return redirect(url_for('home_blueprint.index'))                
    return render_template('home/add_class.html', segment='add_class')


@blueprint.route('/attend/<unique_link>', methods=['GET', 'POST'])
def attend(unique_link):
    course = Class.query.filter_by(unique_link=unique_link).first_or_404()
    messages = {}  # Initialize an empty message

    if request.method == 'POST':
        matricula = request.form['matricula']
        email = request.form['email']  # Assuming you want to capture the email
        secret = request.form['secret']
        if secret == course.secret_code:
            attendance = Attendance(course_code=course.course_code, course_class=course.course_class, emp=1, matricula=matricula, email=email)
            db.session.add(attendance)
            db.session.commit()
            messages['success'] = 'Registro feito com sucesso!'
            # Generate PDF
            # Obter data e hora atual
            agora = datetime.now()
            hora_atual = agora.strftime("%Y-%m-%d %H:%M:%S")

            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            c.drawString(100, 750, f"Confirmação de Presença para {request.form['course_name']}")
            c.drawString(100, 735, f"Data e Hora: {hora_atual}")
            c.drawString(100, 720, f"Email do Estudante: {request.form['email']}")
            c.drawString(100, 705, f"Matrícula: {request.form['matricula']}")
            c.drawString(100, 690, f"Link Único: {unique_link}")
            c.save()

            # Return PDF
            pdf_buffer.seek(0)
            return Response(pdf_buffer, mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=attendance_confirmation.pdf'})
        else:
            messages['error'] = 'Código secreto inválido.'
            # Note: For API-like responses, consider handling errors differently

    return render_template('/home/attendance_form.html', course=course, messages=messages)

@blueprint.route('/attendance_data/<course_code>/<course_class>')
@login_required
def filtered_attendance_data(course_code, course_class):
    attendances = Attendance.query.filter_by(course_code=course_code, course_class=course_class).all()
    return render_template('home/attendance_data.html', attendances=attendances, course_code=course_code, course_class=course_class)

@blueprint.route('/export_attendance_csv/<course_code>/<course_class>')
@login_required
def export_attendance_csv(course_code, course_class):
    # Filter attendance records by course_code and course_class
    attendances = Attendance.query.filter_by(course_code=course_code, course_class=course_class).all()

    def generate():
        data = StringIO()
        csv_writer = csv.writer(data)

        # Write the header
        csv_writer.writerow(["01", "CURSO", "TURMA", "EMP", "MATRICULA", "DATA"])

        # Write the data rows
        for attendance in attendances:
            csv_writer.writerow([
                "02",
                attendance.course_code,
                attendance.course_class,
                "1",  # EMP is always 1
                attendance.matricula,
                attendance.date.strftime('%d/%m/%Y')  # Format the date
            ])
            data.seek(0)
            yield data.read()
            data.seek(0)
            data.truncate(0)

    # Generate the CSV file
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": f"attachment;filename=attendance_data_{course_code}_{course_class}.csv"})

@blueprint.route('/archive_class/<int:class_id>', methods=['POST'])
@login_required
def archive_class(class_id):
    class_to_archive = Class.query.get_or_404(class_id)
    class_to_archive.archived = True
    db.session.commit()
    return jsonify({'success': 'Class archived successfully'}), 200

@blueprint.route('/archived')
@login_required
def archived_classes():
    classes = Class.query.filter_by(archived=True).all()
    class_attendance_counts = db.session.query(
        Class.course_code,
        Class.course_class,
        db.func.count(Attendance.matricula)
    ).join(
        Attendance,
        db.and_(Class.course_code == Attendance.course_code, Class.course_class == Attendance.course_class),
        isouter=True
    ).filter(Class.archived == True).group_by(Class.course_code, Class.course_class).all()

    # Convert class_attendance_counts to a dictionary for easy access in the template
    attendance_dict = {(course_code, course_class): count for course_code, course_class, count in class_attendance_counts}

    return render_template('home/archived_classes.html', classes=classes, attendance_dict=attendance_dict)

@blueprint.route('/delete_class/<int:class_id>', methods=['POST'])
@login_required
def delete_class(class_id):
    try:
        # Query to find the class with the given ID
        class_to_delete = Class.query.get_or_404(class_id)

        # Delete related attendance records
        Attendance.query.filter_by(course_code=class_to_delete.course_code, course_class=class_to_delete.course_class).delete()

        # Delete the class itself
        db.session.delete(class_to_delete)

        # Commit the changes to the database
        db.session.commit()

        # Return a success message (adjust according to your frontend needs)
        print(f'Class and related attendance records successfully deleted.')
        return redirect(url_for('home_blueprint.index'))
    except Exception as e:
        db.session.rollback()
        # Log the error and return an error message
        # Adjust logging according to your application's logging setup
        print(f'Error deleting class with ID {class_id}: {e}')
        return render_template('home/page-403.html'), 403
    
@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
