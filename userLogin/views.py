from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    # print(request.body)
    data = json.loads(request.body.decode('utf-8'))
    name, password = data.get('name'), data.get('password')
    # print(name, password)
    testName,testWord = "YBMK","bala123"
    if testName == name and testWord == password:
        return HttpResponse("Login Successful", status = 200)
    else:
        return HttpResponse("Bad Credentials", status = 404)
    # return HttpResponse(" bhoom")

