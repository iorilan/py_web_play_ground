from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields
from flask import Flask, abort, request, make_response, jsonify
from pprint import pprint
import json

from ma_schemas import ToDoListSchema, ItemSchema

spec = APISpec(
    title="ToDo",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(description="A Todo API"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)


spec.components.schema("Item", schema=ItemSchema)
spec.components.schema("ToDoList", schema=ToDoListSchema)


