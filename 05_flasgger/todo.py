"""
CRUD sample for Flask ,Marshmallow, flask_restful, swagger 
"""

from flask import Flask,  request
from flask_marshmallow import Marshmallow
from flasgger import Swagger, Schema, fields, SwaggerView
from flask_restful import Api, Resource
from webargs.flaskparser import use_kwargs

import json 

app = Flask(__name__)
swagger = Swagger(app)

class ItemSchema(Schema):
    name = fields.Str()
    description = fields.Str()

class ToDoListSchema(Schema):
    name = fields.Str()
    items = fields.Nested(ItemSchema, many=True)

todolist_schema = ToDoListSchema()
item_schema = ItemSchema()
_fake_db = {'name': "all", "items": [{"name":"item1","description":"test"},{"name":"item2","description":"test"}]}

class ToDoView(SwaggerView):
    
    responses = {
        200: {
            "description": "desc",
            "schema": ToDoListSchema
        }
    }

    def get(self):
        """
        get all todo list
        ---
        responses:
          '200':
            description: call successful
            content:
            application/json:
              schema: ToDoListSchema
        """

        dummy = _fake_db
        return todolist_schema.dump(dummy), 200

class ToDoItemView(SwaggerView):

    responses = {
        200: {
            "description": "desc",
            "schema": ItemSchema
        }
    }


    def get(self, name):
        """
        get item by name
        ---
        parameters:
        - name: name
          in: path
          type: string
          required: true
        responses:
          '200':
            description: call successful
            content:
            application/json:
              schema: ItemSchema
        """
        item = [i for i in _fake_db.get('items') if i.get('name') == name]
        res = item[0] if item else {}
        return item_schema.dump(res), 200
    
    def put(self, name):
        """
        update item by name
        ---
        parameters:
        - name: name
          in: path
          type: string
          required: true
        - name: data
          in: body
          required: true
          schema:
            id: ItemSchema
        responses:
          '200':
            description: call successful
            content:
            application/json:
              schema: ItemSchema
        """
        item = [i for i in _fake_db.get('items') if i.get('name') == name]
        if not item :
            return '', 301

        data = request.json
        _fake_db['items'].remove(item[0])
        _fake_db['items'].append(data)
        return item_schema.dump(data), 200
    
    def delete(self, name):
        """
        delete item by name
        ---
        parameters:
        - name: name
          in: path
          type: string
          required: true
        responses:
          204:
            description: call successful
        """
        item = [i for i in _fake_db.get('items') if i.get('name') == name]
        if not item :
            return '', 301
            
        _fake_db['items'].remove(item[0])
        return '', 204
    

class ToDoItemCreateView(SwaggerView):

    responses = {
        200: {
            "description": "desc",
            "schema": ItemSchema
        }
    }

    
    def post(self):
        """
        add todo 
        ---
        parameters:
        - name: data
          in: body
          required: true
          schema:
            id: ItemSchema
        responses:
          200:
            description: call successful
            content:
              application/json:
                schema: ItemSchema
        """
        data = request.json
        _fake_db['items'].append(data)
        return item_schema.dump(data), 200


class UploadTestView(SwaggerView):
    def post(self, id):
        """
        upload a file
        ---
        parameters:
        - name: id
          in: path
          type: string
          required: true
        - name: file
          in: formData
          required: true
          type: file
          
        responses:
          200:
            description: call successful
        """

        file = request.files.getlist('file')[0]
        return f"Uploaded file is {file.filename}" , 200


app.add_url_rule('/todo', view_func=ToDoView.as_view('todo'))
app.add_url_rule('/todoitem', view_func=ToDoItemCreateView.as_view('todoItemCreate'))
app.add_url_rule('/todoitem/<name>', view_func=ToDoItemView.as_view('todoItem'))
app.add_url_rule('/upload/<id>', view_func=UploadTestView.as_view('uploadTest'))


app.run(debug=True)