"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
import authentication.views
from django.urls import path
import stats.views
from django.contrib import admin

urlpatterns = [
    path('login', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('', stats.views.home, name='home'),
    path('observations/', stats.views.observations, name='observations'),
    path('species/', stats.views.species, name='species'),
    path('trunks/', stats.views.trunks, name='trunks'),
    path('trunk_species/<slug:date>', stats.views.trunk_species, name='trunk_species'),
    path('errors/', stats.views.errors, name='errors'),
    path('export/', stats.views.export, name='export'),
    path('distribution/', stats.views.distribution, name='distribution'),
    path('cramer/', stats.views.cramer, name='cramer'),
    path('chi2/', stats.views.chi2, name='chi2'),
    path('anova/', stats.views.anova, name='anova'),
    path('nb_species_evolution/', stats.views.nb_species_evolution, name='nb_species_evolution'),
    path('file/<slug:folder>/<slug:filename>.<slug:extension>', stats.views.file, name="file"),
    path('archives_original_files/', stats.views.archives_original_files, name='archives_original_files'),
]
