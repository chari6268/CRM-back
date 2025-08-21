from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'interactions', views.InteractionViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'dashboard', views.DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
