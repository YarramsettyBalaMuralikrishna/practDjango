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
    try:
        data = json.loads(request.body.decode('utf-8'))
        email, password = data.get('email'), data.get('password')
        try:
            user = User.objects.get(email = email, password = password)
            serializer = userSerializer(user) 
            response = Response(serializer.data, status=200) # return user data

            # Sending cookie to user
            response.set_cookie('user_logged_in', user.email, max_age=3600, httponly=True)

            return response
        except User.DoesNotExist:
            return Response("Invalid Credentials", status=404)

    except Exception as e:
        return Response(f"Error : {e}", status=404)


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
    try:
        # print("1")
        user_email = request.COOKIES.get('user_logged_in') # getting cookie
        # print("2")
        if not user_email:
            return Response({"detail": "Authentication required"}, status = 401)
        # print("3")
        recievedData = json.loads(request.body.decode('utf-8'))
        # print(recievedData, " reciedev data")
        # print("4")

        try:
            currentUser = User.objects.get(email = recievedData['email']) # get the user
            # print("5")
        except User.DoesNotExist:
            # print("6")
            return Response({"detail": "User not found"}, status=404)
        # print(currentUser)
        # print(user_email)
        # print("7")
        if currentUser.email != user_email:
            # print("8")
            return Response({"detail": "Unauthorized"}, status=403) #check if the user is authorized.
        # print("9")
        try:
            currentUser.userName = recievedData.get('name', currentUser.userName) #update the user data.
            currentUser.password = recievedData.get('password', currentUser.password)
            currentUser.mobile = recievedData.get('mobile', currentUser.mobile)
            # print("10")
            currentUser.save()
        except Exception as e:
            # print("11")
            return Response(f"error in saving details {e}", status=404)
            
        # print("11")
        return Response("updated successfully", status=200)

    except json.JSONDecodeError:
        # print("12")
        return Response({"detail": "Invalid JSON"}, status=400)
    except Exception as e:
        # print("513")
        return Response(f"An error occurred: {e}", status=500)
        
@api_view(['POST'])
def signOut(request):
    response = Response({"Signed Out successfully"}, status=200)
    response.delete_cookie('user_logged_in')
    return response