from datetime import datetime
import mimetypes
import os

import numpy as np
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from stats.functions.anova_function import anova_function
from stats.functions.chi2_function import chi2_function
from stats.functions.cramer_function import cramer_function
from stats.functions.distribution_function import distribution_function
from stats.functions.export_function import export_function
from stats.functions.nb_species_evolution_function import nb_species_evolution_function


@login_required
def home(request):
    errors = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Erreurs")
    errors = errors.replace({np.nan: None})
    errors = errors.to_numpy()
    stats = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")
    nb_obs = stats.shape[0]
    species = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Espèces")
    nb_species = species.shape[0]
    return render(request, 'stats/home.html', {"nb_obs": nb_obs, "nb_species": nb_species, "errors": errors})


@login_required
def species(request):
    species_list = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Espèces")
    species_list = species_list.replace({np.nan: None})
    species_list = species_list.to_numpy()
    return render(request, 'stats/species.html', {"species_list": species_list})


@login_required
def export(request):
    if request.method == 'POST':
        file = request.FILES['original_file']
        default_storage.save("files/import/liste_originale" + str(datetime.date(datetime.now())) + ".xls",
                             ContentFile(file.read()))
        export_function(file)
        return redirect('home')
    return render(request, 'stats/export.html')


@login_required
def distribution(request):
    data = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")
    if request.method == 'POST':
        post_request = request.POST
        location = post_request.get("location")
        variable = post_request.get("variable")
        title = post_request.get("title")
        limit = post_request.get("limit")
        cf = post_request.get("cf")
        if cf is None:
            cf = False
        else:
            cf = True

        distribution_function(data, variable, title, int(limit), cf, location)
        return render(request, 'stats/distribution_view.html')
    else:
        locations = data["Lieu"].dropna().unique()
        variables = data.columns.values
        return render(request, 'stats/distribution.html', {"locations": locations, "variables": variables})


@login_required
def cramer(request):
    data = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")
    if request.method == 'POST':
        post_request = request.POST
        location = post_request.get("location")
        cf = post_request.get("cf")
        if cf is None:
            cf = False
        else:
            cf = True

        cramer_function(data, cf, location)
        return render(request, 'stats/cramer_view.html')
    else:
        locations = data["Lieu"].dropna().unique()
        return render(request, 'stats/cramer.html', {"locations": locations})


@login_required
def chi2(request):
    data = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")
    if request.method == 'POST':
        post_request = request.POST
        location = post_request.get("location")
        variable1 = post_request.get("variable1")
        variable2 = post_request.get("variable2")
        title = post_request.get("title")
        species_agg = post_request.get("species_agg")
        if species_agg is None:
            species_agg = False
        else:
            species_agg = True

        cf = post_request.get("cf")
        if cf is None:
            cf = False
        else:
            cf = True

        chi2_function(data, variable1, variable2, title, species_agg, cf, location)
        return render(request, 'stats/chi2_view.html')
    else:
        locations = data["Lieu"].dropna().unique()
        variables = data.columns.values
        return render(request, 'stats/chi2.html', {"locations": locations, "variables": variables})


@login_required
def anova(request):
    data = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")
    if request.method == 'POST':
        post_request = request.POST
        location = post_request.get("location")
        variable1 = post_request.get("variable1")
        variable2 = post_request.get("variable2")
        title = post_request.get("title")

        cf = post_request.get("cf")
        if cf is None:
            cf = False
        else:
            cf = True

        anova_function(data, variable1, variable2, title, cf, location)
        return render(request, 'stats/anova_view.html')
    else:
        locations = data["Lieu"].dropna().unique()
        variables = data.columns.values
        return render(request, 'stats/anova.html', {"locations": locations, "variables": variables})


@login_required
def nb_species_evolution(request):
    data = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")
    if request.method == 'POST':
        post_request = request.POST
        location = post_request.get("location")

        cf = post_request.get("cf")
        if cf is None:
            cf = False
        else:
            cf = True

        nb_species_evolution_function(data, cf, location)
        return render(request, 'stats/nb_species_evolution_view.html')
    else:
        locations = data["Lieu"].dropna().unique()
        return render(request, 'stats/nb_species_evolution.html', {"locations": locations})


@login_required
def download_liste_modifiee(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = base_dir + '/files/export/liste_modifiee.xlsx'
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=liste_modifiee.xlsx"
    return response
