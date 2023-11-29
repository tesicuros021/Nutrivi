"""
URL configuration for Proba6 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from app import views

urlpatterns = [
    path('', views.nutrivita),
    path('admin/', admin.site.urls),
    path('unos/', views.unos),
    path('nutrivita/', views.nutrivita),
    path('ponuda/', views.ponuda),
    path('detalji/<int:patient_id>/', views.detalji, name='detalji'),
    path('sastanak/<int:patient_id>/<int:patient_meeting_id>/', views.sastanak, name='sastanak'),
    path('brisanje/<int:x>', views.brisanje),
    path('novisastanak/<int:patient_id>/', views.novisastanak, name='novisastanak'),
]
