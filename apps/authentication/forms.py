# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, BooleanField, FloatField, IntegerField, DateField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])


class CourseRegistrationForm(FlaskForm):
    matricula = StringField('Matricula', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    tipo_cur = StringField('Tipo de Curso', validators=[DataRequired()])
    carga_hor = StringField('Carga Horária', validators=[DataRequired()])
    opcao_cur = StringField('Opção de Curso', validators=[DataRequired()])
    tit_curso = StringField('Título do Curso', validators=[DataRequired()])
    local_evento = StringField('Local do Evento', validators=[DataRequired()])
    email_evento = StringField('Email do Evento', validators=[DataRequired(), Email()])
    data_inicio = DateField('Data de Início', format='%Y-%m-%d', validators=[DataRequired()])
    hora_inicio = DateTimeField('Hora de Início', format='%Y-%m-%dT%H:%M')
    entidade = StringField('Entidade')
    municipio_comunidade = StringField('Município/Comunidade', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    data_fim = DateField('Data de Fim')
    hora_fim = DateTimeField('Hora de Fim', format='%Y-%m-%dT%H:%M')
    recur_unid = BooleanField('Recurso da Unidade')
    recur_unid_val = FloatField('Valor do Recurso da Unidade', default=0.0)
    data_limite = DateField('Data Limite', format='%Y-%m-%d', validators=[DataRequired()])
    val_apoio = FloatField('Valor de Apoio', default=0.0)
    val_ins = FloatField('Valor de Inscrição', default=0.0)
    val_trans = FloatField('Valor de Transporte', default=0.0)
    val_diarias = FloatField('Valor de Diárias', default=0.0)
    outra_entidade = StringField('Outra Entidade')
    outra_entidade_val = FloatField('Valor da Outra Entidade', default=0.0)
    outra_entidade_val_final = FloatField('Valor Final da Outra Entidade', default=0.0)
    autores = StringField('Autores')
    tit_completo = StringField('Título Completo')
    resumo = StringField('Resumo')
    palavras_chave = StringField('Palavras-chave')
    matricula_chefia = StringField('Matrícula da Chefia')
    matricula_dir = StringField('Matrícula do Diretor')
    prestacao_contas = BooleanField('Prestação de Contas')
    certificado_contas = BooleanField('Certificado de Contas')
    repositorio_dig = BooleanField('Repositório Digital')
    conhecimento_repassado = BooleanField('Conhecimento Repassado')
    numero_beneficiados = IntegerField('Número de Beneficiados', default=0)
    beneficiados_descricao = StringField('Descrição dos Beneficiados')
    forma_repasso = StringField('Forma de Repasso')
    justificativa = StringField('Justificativa')