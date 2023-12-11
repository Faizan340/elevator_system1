from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

def get_elevator_object_or_404(pk, model):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise Http404

def success_response(data=None, message=None):
    return {
        'success': True,
        'message': message,
        'data': data,
    }

def error_response(message, status_code):
    return {
        'success': False,
        'message': message,
    }, status_code
