from django.http import HttpResponse
import json


def bad_json(message=None, error=None, extradata=None):
    """
        Returns an invalid response on json data
    """
    data = {'result': 'bad'}

    if message:
        data.update({'message': message})
    if error:
        if error == 0:
            data.update({"message": 'Bad request'})
        elif error == 1:
            data.update({"message":'Error saving data'})
        elif error == 2:
            data.update({"message": 'Error updating data'})
        elif error == 3:
            data.update({"message": 'Error deleting data'})
        elif error == 4:
            data.update({"message": 'You do not have permission to perform this action'})
        elif error == 5:
            data.update({"message": 'Error generating the information'})
        else:
            data.update({"message": 'System error'})
    if extradata:
        data.update(extradata)
    return HttpResponse(json.dumps(data), content_type="application/json")


def ok_json(data=None):
    """
        Returns a valid response on json data
    """
    if data:
        if type(data) == dict and 'result' not in data.keys():
            data.update({"result": "ok"})
    else:
        data = {"result": "ok"}
    return HttpResponse(json.dumps(data), content_type="application/json")

