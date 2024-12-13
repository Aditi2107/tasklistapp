from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Task
from sqlalchemy import and_
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://adititasklist.netlify.app"}})

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


@app.route('/tasks', methods=['GET'])
def get_tasks():
    date = request.args.get('date')
    entity_name = request.args.get('entity_name')
    task_type = request.args.get('task_type')
    contact_person = request.args.get('contact_person')
    status = request.args.get('status')

    filters = []
    if date:
        filters.append(Task.date == date)
    if entity_name:
        filters.append(Task.entity_name .like(f"%{entity_name}%"))
    if task_type:
        filters.append(Task.task_type == task_type)
    if contact_person:
        filters.append(Task.contact_person.like(f"%{contact_person}%"))
    if status:
        filters.append(Task.status == status)

    tasks = Task.query.filter(and_(*filters)).all() if filters else Task.query.all()

    return jsonify([task.to_dict() for task in tasks])


# @app.route('/tasks', methods=['GET'])
# def get_tasks():
#     """Get all tasks with optional filtering."""
#     filters = request.args
#     query = Task.query
    
#     if 'date' in filters:
#         query = query.filter_by(date=filters['date'])
#     if 'entity_name' in filters:
#         query = query.filter(Task.entity_name.contains(filters['entity_name']))
#     if 'task_type' in filters:
#         query = query.filter_by(task_type=filters['task_type'])
#     if 'status' in filters:
#         query = query.filter_by(status=filters['status'])
#     if 'contact_person' in filters:
#         query = query.filter(Task.contact_person.contains(filters['contact_person']))
    
#     tasks = query.all()
#     return jsonify([task.to_dict() for task in tasks])


@app.route('/tasks', methods=['POST'])
# def create_task():
#     """Create a new task."""
#     data = request.json
    
#     print("received request data ==> ",data)

#     new_task = Task(**data)
#     db.session.add(new_task)
#     db.session.commit()
#     return jsonify(new_task.to_dict()), 201
def create_task():
    """Create a new task."""
    data = request.json
    
    # Debugging: Print incoming data
    print("Received request data:", data)
    
    # Validate required fields
    required_fields = ['entity_name', 'status', 'date', 'time', 'task_type', 'contact_person']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Create the new task
        new_task = Task(
            entity_name=data['entity_name'],
            status=data['status'],
            date=data['date'],
            time=data['time'],
            task_type=data['task_type'],
            contact_person=data['contact_person'],
            notes=data.get('notes', '')  # Optional field
        )
        
        # Save to the database
        db.session.add(new_task)
        db.session.commit()
        
        # Return the created task as a dictionary
        return jsonify(new_task.to_dict()), 201

    except Exception as e:
        # Handle exceptions and rollback if needed
        db.session.rollback()
        print("Error while creating task:", e)
        return jsonify({'error': 'An error occurred while creating the task'}), 500


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    """Update a task."""
    task = Task.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(task, key, value)
    db.session.commit()
    return jsonify(task.to_dict())


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    """Delete a task."""
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
