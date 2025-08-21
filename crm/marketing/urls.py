from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'campaigns', views.MarketingCampaignViewSet)
router.register(r'email-campaigns', views.EmailCampaignViewSet)
router.register(r'email-templates', views.EmailTemplateViewSet)
router.register(r'subscribers', views.EmailSubscriberViewSet)
router.register(r'email-sends', views.EmailSendViewSet)
router.register(r'social-campaigns', views.SocialMediaCampaignViewSet)
router.register(r'automations', views.MarketingAutomationViewSet)
router.register(r'metrics', views.MarketingMetricsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
