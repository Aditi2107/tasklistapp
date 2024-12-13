from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entity_name = db.Column(db.String(100), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)  # Call, Meeting, Video Call
    contact_person = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=False, default="open")  # Open or Closed
    notes = db.Column(db.Text, nullable=True)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "entity_name": self.entity_name,
            "task_type": self.task_type,
            "contact_person": self.contact_person,
            "status": self.status,
            "notes": self.notes,
            "date": self.date,
            "time": self.time
        }
