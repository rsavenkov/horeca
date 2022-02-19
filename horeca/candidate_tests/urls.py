from django.urls import path
from rest_framework import routers


from . import views

router = routers.DefaultRouter()


urlpatterns = [
    path('testing-session', views.TestingSessionView.as_view({'get': 'get'})),
    path('testing-session/next', views.TestingSessionView.as_view({'post': 'next_step'})),
    path('testing-session/back', views.TestingSessionView.as_view({'post': 'previous_step'})),
    path('testing-session/fill-personal-data', views.TestingSessionView.as_view({'put': 'fill_personal_data'})),
    path('testing-session/answer-question', views.TestingSessionView.as_view({'post': 'answer_question'})),
]
