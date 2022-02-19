from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('admins', views.AdminViewSet, basename='admins')
router.register('managers', views.ManagerViewSet, basename='managers')
router.register('candidates', views.CondidateViewSet, basename='candidates')

urlpatterns = [
    path('users/', include(router.urls)),
    path('users/login', views.Login.as_view()),
    path('users/logout', views.Logout.as_view()),
    path('users/change-password', views.ChangePasswordView.as_view()),
    path('users/get-me', views.GetMeView.as_view()),
    path('users/reset-password/', include('django_rest_passwordreset.urls', namespace='reset_password'))
]
