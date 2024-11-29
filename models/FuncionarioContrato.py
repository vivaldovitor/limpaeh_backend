from helpers.database import db

class FuncionarioContrato(db.Model):
    __tablename__ = 'funcionario_contrato'

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contratos.id'), primary_key=True)

    usuario = db.relationship('Usuario', backref=db.backref('funcionarios_contrato', lazy=True))
    contrato = db.relationship('Contrato', backref=db.backref('funcionarios_contrato', lazy=True))
