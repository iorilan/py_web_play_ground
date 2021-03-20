"""
manual create swagger json and generate the spec using apispec
"""

from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask
from marshmallow import Schema, fields
from flask.views import MethodView
from ma_schemas import ToDoListSchema, ItemSchema
from spec_helper import spec
import json

app = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "test"
    },
    oauth_config={
        "clientId":"test",
        "clientSecret":"",
        "appName":"test swagger",
        "scopeSeparator":"|"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)



todolist_schema = ToDoListSchema()
item_schema = ItemSchema()
_fake_db = {'name': "all", "items": [{"name":"item1","description":"test"},{"name":"item2","description":"test"}]}

class ToDoView(MethodView):

    def get(self):
        """
        get all todo list
        ---
        responses:
          200:
            content:
              application/json:
                schema: ToDoListSchema
        """

        dummy = _fake_db
        return todolist_schema.dump(dummy), 200



# load views into spec
todo_view = ToDoView.as_view('todo')
app.add_url_rule('/todo', view_func=todo_view)


# convert spec to swagger for each view 
with app.test_request_context():
    spec.path(view=todo_view)
    # load more views

print(dict(spec.to_dict()))

# save swagger
with open('static/swagger.json', 'w') as f:
    json.dump(spec.to_dict(), f)


app.run(debug=True)