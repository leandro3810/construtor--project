from datetime import datetime, timezone
from app.extensions import db


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    client_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    responsible_engineer = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(60), nullable=False, default='Geral')
    status = db.Column(db.String(30), nullable=False, default='Em andamento')
    area_m2 = db.Column(db.Float, nullable=False, default=0.0)
    budget_brl = db.Column(db.Float, nullable=False, default=0.0)
    start_date = db.Column(db.Date, nullable=True)
    expected_end_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    models3d = db.relationship('Model3D', backref='project', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Project {self.name}>'
