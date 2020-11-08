from flask import Flask, request, jsonify
from bson import json_util, ObjectId
from pymongo import MongoClient
import os
import helper
import apiresult
import json 


app = Flask(__name__)
title = "TODO title"
heading = "TODO header"

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.admin
todos = db.ToDoList

@app.route("/all", methods=['GET'])
def all():
    res = helper.mongoJson(todos.find())
    print(res)
    return apiresult.ok(res)

@app.route("/search", methods=['POST'])
def search():
    p = request.json
    
    op = p['operation']
    cond = []
    if 'title' in p:
        title = p['title']
        cond.append({'title':{"$regex": ".*{}.*".format(title)}})
    if 'desc' in p:
        desc = p['desc']
        cond.append({'desc':{"$regex": ".*{}.*".format(desc)}})
    
    res = helper.mongoJson(todos.find(
        {
            f"${op}":cond
            # "$or":
            #     [
            #         {'desc':{"$regex": ".*{}.*".format(desc)}},
            #         {'title':{"$regex": ".*{}.*".format(title)}}
            #     ]
        }
        ))
    print(res)
    return apiresult.ok(res)

@app.route('/detail/<id>', methods=['GET'])
def getById(id):
    res = helper.mongoJson((todos.find_one({'_id':id})))
    return apiresult.ok(res)

@app.route("/create", methods=['POST'])
def create():
    try:
        json = request.json
        t = json['title']
        d = json['desc']
        if dupplicate(t,d):
            return apiresult.duplicated()

        json['createdon'] = helper.now()
        todos.insert(json)
        return apiresult.ok()
    except:
        return apiresult.internalServerError()
def dupplicate(title, desc):
    obj = todos.find_one({'title':title, 'desc':desc});
    print (obj)
    return obj != None


@app.route("/update/<id>", methods=['PUT'])
def update(id):
    try:
        obj = todos.find({'_id':id})
        if obj == None:
            return apiresult.parameterError({'id':id})
        
        content = request.json
        todos.update({'_id':ObjectId(id)},
            {
                '$set': {
                            'title':content['title'],
                            'desc':content['desc'],
                            'bydate':content['bydate']
                        }
            }
        )
        return apiresult.ok()
    except:
        return apiresult.internalServerError()

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    try:
        res = todos.delete_one({'_id':ObjectId(id)})
        return apiresult.ok()
    except:
        return apiresult.internalServerError()

if __name__ == "__main__":
    app.run(port=5545)