from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'contacts', views.ContactViewSet)
router.register(r'segments', views.CustomerSegmentViewSet)
router.register(r'tags', views.CustomerTagViewSet)
router.register(r'activities', views.CustomerActivityViewSet)
router.register(r'preferences', views.CustomerPreferenceViewSet)
router.register(r'documents', views.CustomerDocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
