from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://[USERNAME]:[PASSWORD]@[HOSTNAME]:[PORT]/[DATABASE_NAME]'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()

class ToDo(db.Model):
    __tablename__ = 'todo'
    pk_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    complete_status = db.Column(db.Boolean, default=False)
    
    def __init__(self, title, complete_status=False):
        self.title = title
        self.complete_status = complete_status

@app.route("/")
def home():
    todo_list = ToDo.query.all()
    return render_template("index.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    baslik = request.form["title"]
    status = bool(request.form.get('status'))
    todo = ToDo(title=baslik, complete_status=status)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = ToDo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))



@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = ToDo.query.get(todo_id)
    if todo:
        todo.complete_status = not todo.complete_status
        db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)