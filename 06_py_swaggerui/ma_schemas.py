from marshmallow import Schema, fields

class ItemSchema(Schema):
    name = fields.Str()
    description = fields.Str()

class ToDoListSchema(Schema):
    name = fields.Str()
    items = fields.Nested(ItemSchema, many=True)
