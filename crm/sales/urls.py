from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'leads', views.LeadViewSet)
router.register(r'opportunities', views.OpportunityViewSet)
router.register(r'deals', views.DealViewSet)
router.register(r'sales-activities', views.SalesActivityViewSet)
router.register(r'pipelines', views.SalesPipelineViewSet)
router.register(r'forecasts', views.SalesForecastViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
