from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('contact/', views.contact_view, name='contact'),
    path('inscription/', views.SignUpView.as_view(), name='signup'),
]
