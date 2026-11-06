from flask import Flask , request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db= SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer ,  primary_key=True)
    title = db.Column(db.String , nullable=False)
    description = db.Column(db.String(100) , nullable=False)
    completed = db.Column(db.Boolean , nullable=False)
    priority = db.Column(db.String(100) , nullable=False , default="medium")


with app.app_context():
    db.create_all()


@app.route('/tasks')
def get_tasks():
     tasks = Task.query.all()
     result = []
     for task in tasks:
        result.append({
            "id":task.id ,
            "title":task.title , 
            "description":task.description , 
            "completed":task.completed,
            "priority":task.priority
        })
     return{
        "tasks": result
    }

@app.route('/tasks/<int:task_id>' , methods=['GET'])
def get_one_task(task_id):
    tas = Task.query.filter_by(id=task_id).one_or_404()
    return{
        "id":tas.id ,
            "title":tas.title , 
            "description":tas.description , 
            "completed":tas.completed,
            "priority":tas.priority
    }

@app.route('/tasks' , methods=['POST'])
def create_task():
    data = request.get_json()

    if data is None:
        return{
            "error": "Invalid or missing JSON body"
        },400
    
    if not data :
        return{
            "error": "Request body is empty"
        },400

    if "title" not in data or data["title"] == "":
        return {
            "error": "title is missing or empty"
        },400
    if "description" not in data or data["description"] =="":
        return{
            "error": "description is missing or empty"
        },400

    t = Task(
        title =data["title"] ,
        description = data["description"] ,
        completed = False , 
    )
    db.session.add(t)
    db.session.commit()
    return{
         "id":t.id ,
            "title":t.title , 
            "description":t.description , 
            "completed":t.completed,
            "priority":t.priority
    }
    
@app.route('/tasks/<int:task_id>' , methods=['PUT'])
def update(task_id):
        exist_task = Task.query.filter_by(id=task_id).one_or_404()
        data = request.json

        if "title" not in data or data["title"] == "":
            return {
            "error": "title is missing or empty"
        },400
        if "description" not in data or data["description"] =="":
            return{
            "error": "description is missing or empty"
        },400
        if "completed" not in data or type(data["completed"]) is not bool:
             return{
            "error": "completed is missing or invalid data type"
        },400
        if "priority" not in data or data["priority"] not in ["low", "medium", "high"]:
             return{
            "error": "priority is missing or empty"
        },400

        exist_task.title = data["title"]
        exist_task.description = data["description"]
        exist_task.completed = data["completed"]
        exist_task.priority = data["priority"]
        db.session.commit()

       
        return{
             "id":exist_task.id ,
            "title":exist_task.title , 
            "description":exist_task.description , 
            "completed":exist_task.completed,
            "priority":exist_task.priority
        },200


@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def patch(task_id):
    update_exit_task = Task.query.filter_by(id=task_id).one_or_404()
    data = request.get_json()

    if data is None:
        return{
            "error": "Invalid or missing JSON body"
        },400
    
    if not data :
        return{
            "error": "Request body is empty"
        },400

    if "title" in data:
        if isinstance(data["title"], str) and data["title"] != "":
            update_exit_task.title = data["title"]
        else:
            return {"error": "Invalid title"}, 400


    if "description" in data:
        if isinstance(data["description"], str) and data["description"] != "":
            update_exit_task.description = data["description"]
        else:
            return {"error": "Invalid description"}, 400


    if "completed" in data:
        if type(data["completed"]) is bool :
            update_exit_task.completed = data["completed"]
        else:
            return {"error": "Invalid complete"}, 400


    if "priority" in data:
        if data["priority"] in ["low", "medium", "high"]:
            update_exit_task.priority = data["priority"]
        else:
            return {"error": "Invalid priority"}, 400
    
    db.session.commit()


    return{
             "id":update_exit_task.id ,
            "title":update_exit_task.title , 
            "description":update_exit_task.description , 
            "completed":update_exit_task.completed,
            "priority":update_exit_task.priority
    },200


@app.route('/tasks/<int:task_id>' , methods=['DELETE'])
def delete(task_id):
    dele = Task.query.filter_by(id = task_id).one_or_404()
    db.session.delete(dele)
    db.session.commit()
    
    return{
        "message": "This task has been deleted",
         "id":dele.id ,
            "title":dele.title , 
            "description":dele.description , 
            "completed":dele.completed,
            "priority":dele.priority

    }

def error_handl(e):
    return{
        "error": "Resource not found"
    },404


def http_err_handl(e):
    return{
        "error": "Bad request"
    },400


def unsupported_med_typ(e):
    return{
        "error": "Content-Type must be application/json"
    },415

app.register_error_handler(400,http_err_handl)
app.register_error_handler(404,error_handl)
app.register_error_handler(415,unsupported_med_typ)








if __name__ == "__main__":
    app.run(debug=True)