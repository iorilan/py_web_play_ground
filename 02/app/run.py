from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, not_
from datetime import datetime
import apiresult


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/todolist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    __tablename__ = 'todo'

    id = db.Column('id',db.Integer, primary_key = True)
    title = db.Column('title', db.String)
    desc = db.Column('description', db.String)
    created_on = db.Column('createdOn', db.DateTime, default=datetime.now())
    by_date = db.Column('bydate', db.DateTime)

    def __init__(self, json):
        self.title = json['title']
        self.desc = json['desc']
        self.created_on = datetime.now()
        self.by_date = json['bydate']

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title':self.title,
            'desc':self.desc,
            'created_on':self.created_on,
            'by_date':self.by_date
        }


@app.route("/all", methods=['GET'])
def all():
    records = ToDo.query.all()
    arr = [r.serialize for r in records]
    #print(arr)
    return apiresult.ok(arr)

@app.route('/detail/<id>', methods=['GET'])
def getById(id):
    record = ToDo.query.filter_by(id=id).first()

    return apiresult.ok(record.serialize)

@app.route("/search", methods=['POST'])
def search():
    p = request.json
    op = p['operation']
    title='%'
    if 'title' in p:
        title=f'%{p["title"]}%'
    desc='%'
    if 'desc' in p:
        desc=f'%{p["desc"]}%'
    cond = []
    cond.append(ToDo.title.like(title))
    cond.append(ToDo.desc.like(desc))
    records = []
    if op == 'and':
        records = ToDo.query.filter(and_(*cond))
    else: #default is or 
        records = ToDo.query.filter(or_(*cond))
    arr = [r.serialize for r in records]
    return apiresult.ok(arr)

@app.route("/create", methods=['POST'])
def create():
    json = request.json
    obj = ToDo(json)
    db.session.add(obj)
    db.session.commit()

    return apiresult.ok()

@app.route("/update/<id>", methods=['PUT'])
def update(id):
    json = request.json
    updating = ToDo.query.filter_by(id=id).first()

    if updating is not None:
        updating.title = json['title']
        updating.desc = json['desc']
        updating.bydate=json['bydate']
        db.session.commit()

    return apiresult.ok()
@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    json = request.json
    obj = ToDo.query.filter_by(id=id).first()
    if obj is not None:
        db.session.delete(obj)
        db.session.commit()
    return apiresult.ok()


if __name__ == "__main__":
    app.run(port=5546)