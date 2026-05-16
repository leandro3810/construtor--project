from datetime import datetime, timezone
from app.extensions import db


class Model3D(db.Model):
    __tablename__ = 'models3d'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(60), nullable=False, default='Estrutura')
    discipline = db.Column(db.String(60), nullable=False, default='Arquitetura')
    version = db.Column(db.String(20), nullable=False, default='v1.0')
    format = db.Column(db.String(20), nullable=False, default='GLB')
    author_name = db.Column(db.String(120), nullable=False, default='Equipe Técnica')
    validation_status = db.Column(db.String(30), nullable=False, default='Em revisão')
    file_size_mb = db.Column(db.Float, nullable=False, default=0.0)
    file_name = db.Column(db.String(255), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Model3D {self.name}>'
