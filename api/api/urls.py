from django.urls import path

from api import views


urlpatterns = [
    path('events/', views.EventList.as_view()),
    path('events/<int:pk>/', views.EventDetail.as_view()),
]
