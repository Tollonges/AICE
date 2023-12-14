# aicethethings/views.py
from django.shortcuts import render
# aicethethings/views.py
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        content = data['content']
        # Process the message as needed (save to database, etc.)
        # For simplicity, just print it for now
        print(f"Received message from {username}: {content}")
        return HttpResponse(status=200)
    return HttpResponse(status=400)


def about_us(request):
    return render(request, 'about_us.html')

def chat(request):
    return render(request, 'chat.html')

def home(request):
    return render(request, 'home.html')
