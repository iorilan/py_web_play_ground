from flask import jsonify
import traceback


def ok(obj=None):
    return jsonify({'status':200, 'error':'', 'data':obj})

def parameterError(kv):
    parameters = ''
    for k in kv:
        parameters += '({}:{})'.format(k, kv[k])
    return jsonify({'status':301, 'error':'invalid parameter. {}'.format(parameters)})

def duplicated():
    return jsonify({'status':202, 'error':'duplicated record '})

def internalServerError():
    print (traceback.format_exc())
    return jsonify({'status':500, 'error':'internal server error'})
