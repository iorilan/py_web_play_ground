from flask import jsonify
import traceback


def ok(obj=None):
    return jsonify({'status':200, 'error':'', 'data':obj})

def internalServerError():
    print (traceback.format_exc())
    return jsonify({'status':500, 'error':'internal server error'})
