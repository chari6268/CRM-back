"""
URL configuration for IntelliCX CRM project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from crm.core.views import root_view

urlpatterns = [
    path('', root_view, name='root'),  # Serve React frontend at root
    path('admin/', admin.site.urls),
    path('api/', include('crm.core.urls')),
    path('api/customers/', include('crm.customers.urls')),
    path('api/sales/', include('crm.sales.urls')),
    path('api/marketing/', include('crm.marketing.urls')),
    path('api/analytics/', include('crm.analytics.urls')),
    path('api/support/', include('crm.support.urls')),
    path('api/surveys/', include('crm.surveys.urls')),
    path('api/employees/', include('crm.employees.urls')),
    path('api/knowledge/', include('crm.knowledge.urls')),
    path('api/workflows/', include('crm.workflows.urls')),
    path('api/ai/', include('crm.ai.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
