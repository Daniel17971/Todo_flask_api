from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, reqparse, Resource, fields, marshal_with, abort

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db' #configures databse path sqlite in this case
api=Api(app)
db=SQLAlchemy(app)


class TodoModel(db.Model): #data model 
    id= db.Column(db.Integer, primary_key=True)
    task_name=db.Column(db.Text, nullable=False)
    completed=db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Todo(task_name={self.task_name}, completed={self.completed})"  #This is a f-string representation of the data model

todo_args=reqparse.RequestParser() #parses the arguments for the todo list
todo_args.add_argument('task_name', type=str, required=True,) #parses the task name
todo_args.add_argument('completed', type=bool, required=True) #parses the completed task

#data need to be serialised before sending it to the client

todoFields={
    'id':fields.Integer,
    'task_name':fields.String,
    'completed':fields.Boolean
} #JSON serialisation, what we're sending to the client

#marshal_width is a decorator that serialises the data before sending it to the client

class Todos(Resource): 
    @marshal_with(todoFields)
    def get(self):
        todos=TodoModel.query.all()
        return todos
    @marshal_with(todoFields)
    def post(self):
        args= todo_args.parse_args() #parses the arguments
        todo=TodoModel(task_name=args['task_name'], completed=args['completed'])
        db.session.add(todo)
        db.session.commit()
        return TodoModel.query.all(), 201 #returns the todo list and the status code 201, default is 200
    
class Todo(Resource):
    @marshal_with(todoFields)
    def get(self, id):
        todo=TodoModel.query.filter_by(id=id).first()#filters the todo by id and get the first one
        if not todo:
            abort(404, message="Todo not found")
        return todo
    @marshal_with(todoFields)
    def patch(self,id):
        args=todo_args.parse_args()
        todo=TodoModel.query.filter_by(id=id).first()
        if not todo:
            abort(404, message="Todo not found")
        if args['task_name']:
            todo.task_name=args['task_name']
        if args['completed']:
            todo.completed=args['completed']
        db.session.commit()
        return todo
    @marshal_with(todoFields)
    def delete(self,id):
        todo=TodoModel.query.filter_by(id=id).first()
        if not todo:
            abort(404, message="Todo not found")
        db.session.delete(todo)
        db.session.commit()
        return todo

api.add_resource(Todos, '/todos')
api.add_resource(Todo, "/todos/<int:id>")

@app.route("/")
def home():
    return """<h1>Todo List API</h1>
    <p>Use the following endpoints to interact with the API:</p>
    """

if __name__== '__main__':
    app.run(debug=True)