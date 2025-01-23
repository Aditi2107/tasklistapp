from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Task
from sqlalchemy import and_
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://adititasklist1.netlify.app"}})  

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


# @app.route('/tasks/<int:id>', methods=['PUT'])
# def update_task(id):
#     """Update a task."""
#     task = Task.query.get_or_404(id)
#     data = request.json
#     for key, value in data.items():
#         setattr(task, key, value)
#     db.session.commit()
#     return jsonify(task.to_dict())

from flask import abort

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    """Update a task."""
    # Fetch task by ID
    print("line no 133")
    task = Task.query.get_or_404(id)
    print(task.id)
    print("in line no 136")

    # Extract data from request
    data = request.json
    print(data)
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # Validation
    required_fields = ['entity_name', 'status', 'date', 'time', 'task_type', 'contact_person']
    optional_fields = ['notes']

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    print("checking validation)")

    # Update the task in the database
    # task = db.session.query(Task).filter_by(id=task.id)
    # print(task)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    if 'status' in data and data['status'] not in ['open', 'closed']:
        abort(400, description="Invalid status. Must be 'open' or 'closed'.")

    # Update task fields
    print("updating task")
    # for key, value in data.items():
    #     if key in required_fields + optional_fields:
    #         setattr(task, key, value)
    #         print("updated key")
    #     else:
    #         abort(400, description=f"Unexpected field: {key}")
    task.entity_name = data.get("entity_name", task.entity_name)
    task.task_type = data.get("task_type", task.task_type)
    task.contact_person = data.get("contact_person", task.contact_person)
    task.status = data.get("status", task.status)
    task.notes = data.get("notes", task.notes)
    task.date = data.get("date", task.date)
    task.time = data.get("time", task.time)

    # Commit changes with error handling
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, description="An error occurred while updating the task.")

    return jsonify(task.to_dict())



@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    """Delete a task."""
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return '', 204


# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

