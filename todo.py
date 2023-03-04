from flask import Flask ,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__) # create the app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/Lenovo/OneDrive/Masaüstü/TD_App/todo.db" 
db = SQLAlchemy(app) # create the extension

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) #ID otomatik olarak artsın diye pri_key kullandık
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    todos = Todo.query.all()

    return render_template("index.html",todos = todos) #Index için 'Bootstrap 4 cdn'

@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first() #Idsini seçtiğimiz veriyi almamızı sağlar
    todo.complete = not todo.complete #İstersen if ile de yazabilirsin
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/add",methods = ["POST"]) #Get request istemediğimiz için POST yazdık yalnızca
def addTodo():
    title = request.form.get("title") 
    newTodo = Todo(title = title,complete = False)
    db.session.add(newTodo) #Oluşturduğumuz objeyi SQL'e eklemek için kullandık
    db.session.commit() #Ekleme yaptığımız için commit kullandık

    return redirect(url_for("index"))

@app.route("/delete/<string:id>")

def deleteTodo(id): #Todo listten veri silmek için kullandık
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

with app.app_context():
    db.create_all()
    
if __name__ == "__main__":
    app.run(debug=True)
