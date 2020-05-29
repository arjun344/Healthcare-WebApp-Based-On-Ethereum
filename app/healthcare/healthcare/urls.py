"""swt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('AddPatient',views.AddPatient,name='AddPatient'),
    path('AddDoctor',views.AddDoctor,name='AddDoctor'),
    path('AddInsurer',views.AddInsurer,name='AddInsurer'),
    path('LoginUser',views.LoginUser,name='LoginUser'),
    path('LoginDoctor',views.LoginDoctor,name='LoginDoctor'),
    path('LoginInsurer',views.LoginInsurer,name='LoginInsurer'),
    path('patient',views.patient,name='patient'),
    path('doctor',views.doctor,name='doctor'),
    path('AddinsToUsr',views.AddinsToUsr,name='AddinsToUsr'),
    path('AdddocToUsr',views.AdddocToUsr,name='AdddocToUsr'),
    path('AddMedicalRecord',views.AddMedicalRecord,name='AddMedicalRecord'),
    path('UpdateMedicalRecord',views.UpdateMedicalRecord,name='UpdateMedicalRecord'),
    path('UpdateRepStats',views.UpdateRepStats,name='UpdateRepStats'),
    path('DeleteMedicalRecord',views.DeleteMedicalRecord,name='DeleteMedicalRecord'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
