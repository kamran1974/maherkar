from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from django.shortcuts import render


urlpatterns = [    

    
    path('admin/', admin.site.urls),
    path('', include('account_module.urls')),
    path('ads/', include('advertisement_module.urls')),
    path('job-company/', include('jobAndCompanyActivity_module.urls')),
    path('', include('home_module.urls')),
    path('panel/', include('userPanel_module.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
