from datetime import datetime, timezone
from app.extensions import db


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(60), nullable=False, default='Geral')
    status = db.Column(db.String(30), nullable=False, default='Em andamento')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    models3d = db.relationship('Model3D', backref='project', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Project {self.name}>'
