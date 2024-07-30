# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import uuid

from flask_login import UserMixin

from apps import db, login_manager
import pytz
from datetime import datetime

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    secret_code = db.Column(db.String(20), nullable=True)
    course_code = db.Column(db.Integer, nullable=True)
    course_class = db.Column(db.String(20), nullable=True)
    unique_link = db.Column(db.String(100), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    archived = db.Column(db.Boolean, default=False, nullable=False)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(50))
    course_class = db.Column(db.String(50))
    emp = db.Column(db.Integer)
    matricula = db.Column(db.Integer)
    email = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('America/Sao_Paulo')))

class CourseRegistration(db.Model):
    __tablename__ = 'course_registrations'

    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    tipo_cur = db.Column(db.String(2), nullable=False)
    carga_hor = db.Column(db.String(3), nullable=False)
    opcao_cur = db.Column(db.String(1), nullable=False)
    tit_curso = db.Column(db.String(255), nullable=False)
    local_evento = db.Column(db.String(255))
    email_evento = db.Column(db.String(100))
    data_inicio = db.Column(db.Date)
    hora_inicio = db.Column(db.DateTime)
    entidade = db.Column(db.String(255))
    municipio_comunidade = db.Column(db.String(255))
    telefone = db.Column(db.String(20))
    data_fim = db.Column(db.Date)
    hora_fim = db.Column(db.DateTime)
    recur_unid = db.Column(db.Boolean, default=False)
    recur_unid_val = db.Column(db.Float, default=0)
    data_limite = db.Column(db.Date) 
    val_apoio = db.Column(db.Float, default=0)
    val_ins = db.Column(db.Float, default=0)
    val_trans = db.Column(db.Float, default=0)
    val_diarias = db.Column(db.Float, default=0)
    outra_entidade = db.Column(db.String(255))
    outra_entidade_val = db.Column(db.Float, default=0)
    outra_entidade_val_final = db.Column(db.Float, default=0)
    autores = db.Column(db.String(255))  
    tit_completo = db.Column(db.String(255))
    resumo = db.Column(db.Text)
    palavras_chave = db.Column(db.String(255))  
    matricula_chefia = db.Column(db.String(10))
    matricula_dir = db.Column(db.String(10))
    prestacao_contas = db.Column(db.Boolean, default=False)
    certificado_contas = db.Column(db.Boolean, default=False)
    repositorio_dig = db.Column(db.Boolean, default=False)
    conhecimento_repassado = db.Column(db.Boolean, default=False)
    numero_beneficiados = db.Column(db.Integer, default=0)
    beneficiados_descricao = db.Column(db.Text)
    forma_repasso = db.Column(db.Text)
    justificativa = db.Column(db.Text)
    beneficiados_area = db.Column(db.Text)
    justificativa_nao = db.Column(db.Text)
 
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)

    def __repr__(self):
        return f"<CourseRegistration {self.matricula}>"
