# aicethethings/urls.py
from django.urls import path
from .views import about_us, chat, home

urlpatterns = [
    path('about/', about_us, name='about_us'),
    path('chat/', chat, name='chat'),
    path('', home, name='home'),  # This corresponds to the home.html file
]

# messaging_app/urls.py
from django.urls import path
from .views import send_message

urlpatterns = [
    path('send_message/', send_message, name='send_message'),
]
