from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ErrorLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    error_text = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    root_cause = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.String(20), nullable=False)
    fix = db.Column(db.Text, nullable=False)
    example_incorrect = db.Column(db.Text, nullable=False)
    example_correct = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
