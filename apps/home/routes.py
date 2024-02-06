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
from io import StringIO
from itertools import cycle
import csv


@blueprint.route('/index')
@login_required
def index():
    classes = Class.query.all()
    class_attendance_counts = db.session.query(
        Class.course_code,
        Class.course_class,
        db.func.count(Attendance.matricula)
    ).outerjoin(
        Attendance,
        db.and_(Class.course_code == Attendance.course_code, Class.course_class == Attendance.course_class)
    ).group_by(Class.course_code, Class.course_class).all()

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
        secret_code = request.form['secret']
        course_code = request.form['course_code']
        course_class = request.form['course_class']
        new_class = Class(name=class_name, secret_code=secret_code, course_code=course_code, course_class=course_class)
        db.session.add(new_class)
        db.session.commit()
        return redirect(url_for('home_blueprint.index'))                
    return render_template('home/add_class.html', segment='add_class')


@blueprint.route('/frequencia/attend/<unique_link>', methods=['GET', 'POST'])
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
        else:
            messages['error'] = 'Código secreto inválido.'
            # Note: For API-like responses, consider handling errors differently

    return render_template('/home/attendance_form.html', course=course, messages=messages)

@blueprint.route('/frequencia/attendance_data/<course_code>/<course_class>')
@login_required
def filtered_attendance_data(course_code, course_class):
    attendances = Attendance.query.filter_by(course_code=course_code, course_class=course_class).all()
    return render_template('home/attendance_data.html', attendances=attendances, course_code=course_code, course_class=course_class)

@blueprint.route('/frequencia/export_attendance_csv/<course_code>/<course_class>')
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
