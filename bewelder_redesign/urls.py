"""bewelder_redesign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import mainapp.views as mainapp  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('orgs/', include('orgs.urls', namespace='orgs')),
    path('resumes/', include('resumes.urls', namespace='resumes')),
    path('vacancies/', include('vacancies.urls', namespace='vacancies')),
    path('search/', include('search.urls', namespace='search')),
    path('api/messaging/', include('dialogs.api.urls', namespace='dialogs_api')),
    path('dialogs/', include('dialogs.urls', namespace='dialogs')),
    path('', include('mainapp.urls', namespace='mainapp'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
