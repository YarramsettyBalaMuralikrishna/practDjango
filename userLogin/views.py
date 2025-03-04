from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .models import User
from .serializers import userSerializer
from django.shortcuts import get_object_or_404
# Create your views here.

@csrf_exempt
@api_view(['POST'])
def login(request):
    print(request.body)
    data = json.loads(request.body.decode('utf-8'))
    name, password = data.get('name'), data.get('password')
    # print(name, password)
    # testName,testWord = "YBMK","bala123"
    # if testName == name and testWord == password:
    #     return HttpResponse("Login Successful", status = 200)
    # else:
    #     return HttpResponse("Bad Credentials", status = 404)

    allUsers = User.objects.all()
    # print(allUsers)
    serializer = userSerializer(allUsers, many = True)
    # print(serializer.data)
    allData = serializer.data
    for data in allData:
        print(data['userName'])
        if data['userName'] == name and data['password'] == password:
            return Response(f" Hello {name}")
    else:
        return Response(" Bhoom Bad credentials")

    # return Response(" bhoom")

def validateUserData(*args, **kwargs):
    print(args)
    if args:
        data = args[0]
        print(data)
        # assuming name, password, mobile are validated at the front end
        allUserData = User.objects.all()
        serializer = userSerializer(allUserData, many = True)
        allUsersInfo = serializer.data
        print(allUserData)
        for user in allUsersInfo:
            if user['email'] == data['email']:
                return False
        else:
            return True
    else:
        return -1

@csrf_exempt
@api_view(['POST'])
def signUp(request):
    # print(request.body)
    if(len(request.body) == 0 ):
        return Response(f"Enter all mandatory field values", status=404)
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    check = validateUserData(data)
    print(check)
    if check == 1:
        newUser = User(
            userName = data['name'],
            password = data['password'],
            mobile = data['mobile'],
            email = data['email']
        )
        newUser.save()
        return Response(f"signUp Successful", status=200)
    elif check ==0 :
        return Response(f"already registered", status=404) 
    else:
        return Response(f"Enter all mandatory field values", status=500)
    # return Resp onse(f"{check}",)

@api_view(['PUT'])
def update(request):
    recievedData = json.loads(request.body.decode('utf-8'))
    print(recievedData)
    allUserData = User.objects.all()
    serializer = userSerializer(allUserData, many = True)
    userData = serializer.data
    for data in userData:
        if data['email'] == recievedData['email']:
            # return Response("updated successfully")
            # tempData = data
            # tempData['name'] = recievedData['name']
            # tempData['mobile'] = recievedData['mobile']
            # print(tempData)
            newUser = User(
                userName = recievedData['name'],
            password = recievedData['password'],
            mobile = recievedData['mobile'],
            email = recievedData['email']
            )
            newUser.save()
            return Response("updated successfully", status=200)
    else:
        return Response("BHoom", status=404)
    # try:
    #     prod = get_object_or_404(allUserData, )

