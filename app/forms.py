from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length
from app.models.domain import Prioridade, Status

class ChamadoCreateForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(min=5, max=100)])
    descricao = TextAreaField('Descrição', validators=[DataRequired(), Length(min=10)])
    prioridade = SelectField('Prioridade', choices=[(p.value, p.value) for p in Prioridade], validators=[DataRequired()])
    
    atribuicao_automatica = BooleanField('Distribuição Automática', default=True)
    responsavel_id = SelectField('Responsável Manual', coerce=int, choices=[])

    submit = SubmitField('Abrir Chamado')

class ChamadoUpdateForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(min=5, max=100)])
    descricao = TextAreaField('Descrição', validators=[DataRequired(), Length(min=10)])
    prioridade = SelectField('Prioridade', choices=[(p.value, p.value) for p in Prioridade], validators=[DataRequired()])
    status = SelectField('Status', choices=[(s.value, s.value) for s in Status], validators=[DataRequired()])

    submit = SubmitField('Salvar Alterações')