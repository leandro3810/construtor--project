from datetime import datetime, timezone
from app.extensions import db


class Model3D(db.Model):
    __tablename__ = 'models3d'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(60), nullable=False, default='Estrutura')
    file_name = db.Column(db.String(255), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Model3D {self.name}>'
