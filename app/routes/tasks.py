from flask import Blueprint, request
from ..models import Task, User
from .. import db

tasks_bp = Blueprint('tasks' , __name__)


@tasks_bp.route('/tasks')
def get_tasks():
     sort_options = {
        "id": Task.id , 
        "title": Task.title ,
        "priority": Task.priority
     }
     order_param = request.args.get('order' , 'asc')
     
     #order validation
     if order_param not in ('asc' , 'desc'):
        return{
            "error": "Invalid order"
        },400

     sort_param = request.args.get('sort' , 'id')
     
     #sort parameter validation
     if sort_param not in sort_options:
        return{
            "error": "Invalid sort field"
        },400

     sort_col = sort_options[sort_param]
     if order_param == 'asc':
        sorting  = sort_col.asc()
     else:
        sorting = sort_col.desc()

     completed = request.args.get('completed')
     priority = request.args.get('priority')
     search_param = request.args.get('search')
     page = request.args.get('page' , 1)
     per_page = request.args.get('per_page' , 10)
     


     try:
        page = int(page)
        per_page = int(per_page)
     except ValueError:
        return{"error": "Page and per_page must be integers "} , 400
     if page <= 0 or per_page <= 0:
        return{"error": "Page and per_page must be greater than 0"} , 400
     
     
     query = Task.query
     query = query.order_by(sorting)
     offset = (page-1)* per_page
     result = []
     print("GET /tasks called")

     print("Completed:", completed)

      #validation
     if completed not in (None, "true", "false"):
        return {"error": "Invalid completed"}, 400

     if priority is not None and priority not in {"high", "medium", "low"}:
        return {"error": "Invalid priority"}, 400

        
     if completed == "true":
        completed = True
     if completed == "false":
        completed = False

     if completed is not None:
        query = query.filter_by(completed = completed)
     if priority is not None:
        query = query.filter_by(priority = priority)

       
     if search_param is not None:
         query = query.filter(Task.title.like(f"%{search_param}%"))

     
     query = query.offset(offset).limit(per_page)


     tasks = query.all()
   
    
    

     for task in tasks:
        result.append({
            "id":task.id ,
            "title":task.title , 
            "description":task.description , 
            "completed":task.completed,
            "priority":task.priority
        })
     return{
        "tasks": result,
    }

    
    
@tasks_bp.route('/tasks/<int:task_id>' , methods=['GET'])
def get_one_task(task_id):
    tas = Task.query.filter_by(id=task_id).one_or_404()
    return{
        "id":tas.id ,
            "title":tas.title , 
            "description":tas.description , 
            "completed":tas.completed,
            "priority":tas.priority
    }



@tasks_bp.route('/tasks' , methods=['POST'])
def create_task():
    data = request.get_json()
    user = db.session.get(User , data['user_id'])
    

    if 'user_id' not in data:
        return{
            "error": "user_id is required"
        },400
    
    if not isinstance(data['user_id'], int) or isinstance(data['user_id'], bool):
        return{
            "error": "Incorrect user_id data type , must be INT"
        },400
    
    if user is None:
        return{
            "error": "user_id not found in database"
        },404
    
    
    

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
        user = user, 
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

    


@tasks_bp.route('/tasks/<int:task_id>' , methods=['PUT'])
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


@tasks_bp.route('/tasks/<int:task_id>', methods=['PATCH'])
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

@tasks_bp.route('/tasks/<int:task_id>/complete' , methods=['PATCH'])
def complete_task(task_id):
    comp_task = Task.query.filter_by(id = task_id).one_or_404()
    comp_task.completed = True
    db.session.commit()

    return {
        "id":comp_task.id,
        "title":comp_task.title,
        "completed":comp_task.completed,
        "priority":comp_task.priority
    },200



@tasks_bp.route('/users/<int:user_id>/tasks' , methods=['GET'])
def usr_task(user_id):
    user_exists = db.session.get(User , user_id)

    if user_exists is None:
        return{
            "error": "User doesnt exist in database"
        },404
    
    user_tasks = user_exists.tasks

    tasks_data = [{
        "id":task.id,
        "title":task.title,
        "description":task.description,
        "completed":task.completed,
        "priority":task.priority
    }
    for task in user_tasks
    ]
    return{
        "tasks":tasks_data
    }


@tasks_bp.route('/tasks/<int:task_id>' , methods=['DELETE'])
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

tasks_bp.register_error_handler(400,http_err_handl)
tasks_bp.register_error_handler(404,error_handl)
tasks_bp.register_error_handler(415,unsupported_med_typ)




