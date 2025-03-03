from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
@require_http_methods(["POST"])
def home(request):
    return HttpResponse("hello user welcome to our calci app")

@require_http_methods(["GET"])
def sum(request, num1, num2):
    n= num1+ num2
    return HttpResponse(f"Sum is {n}")

