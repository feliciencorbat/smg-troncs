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

import constants
from stats.functions.anova_function import anova_function
from stats.functions.chi2_function import chi2_function
from stats.functions.cramer_function import cramer_function
from stats.functions.distribution_function import distribution_function
from stats.functions.export_function import export_function
from stats.functions.nb_species_evolution_function import nb_species_evolution_function


@login_required
def home(request):
    try:
        home_errors = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Erreurs")
        home_errors = home_errors.replace({np.nan: None})
        home_errors = home_errors.to_numpy()
        stats = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")
        nb_obs = stats.shape[0]
        home_species = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Espèces")
        nb_species = home_species.shape[0]
        default_species_writing = constants.Constants.default_species_writing
        gbif_synonyms_errors = constants.Constants.gbif_synonyms_errors
        return render(request, 'stats/home.html', {"nb_obs": nb_obs, "nb_species": nb_species, "errors": home_errors,
                                                   "default_species_writing": default_species_writing,
                                                   "gbif_synonyms_errors": gbif_synonyms_errors})
    except:
        return render(request, 'stats/website_error.html', {"error_info": "Il n'y a pas de fichier liste_modifiee.xlsx."})


@login_required
def observations(request):
    try:
        observations_list = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")
        observations_list = observations_list.replace({np.nan: None})
        observations_list = observations_list.to_numpy()
        return render(request, 'stats/observations.html', {"observations_list": observations_list})
    except:
        return render(request, 'stats/website_error.html', {"error_info": "Il n'y a pas de fichier liste_modifiee.xlsx."})


@login_required
def last_observations(request):
    try:
        observations_list = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")
        last_date = max(observations_list["Date"])
        observations_list = observations_list[observations_list['Date'] == last_date]
        observations_list = observations_list[["Tronc", "Espèce"]].groupby("Tronc")["Espèce"].apply(
            lambda x: list(np.unique(x))).to_frame()
        observations_list = pd.DataFrame({'Tronc': observations_list.index, 'Espèces': observations_list["Espèce"]})
        observations_list.index.name = None
        observations_list["Tronc_int"] = observations_list["Tronc"]
        observations_list["Tronc_int"] = observations_list["Tronc_int"].str.replace("G", "", regex=False)
        observations_list["Tronc_int"] = observations_list["Tronc_int"].str.replace("D", "", regex=False)
        observations_list["Tronc_int"] = observations_list["Tronc_int"].str.replace("_2", "", regex=False)
        observations_list["Tronc_int"] = pd.to_numeric(observations_list["Tronc_int"], errors='coerce')
        observations_list = observations_list.sort_values('Tronc_int')
        observations_list = observations_list[["Espèces", "Tronc"]]
        observations_list = observations_list.to_numpy()
        return render(request, 'stats/last_observations.html', {"date": last_date, "observations_list": observations_list})
    except:
        return render(request, 'stats/website_error.html', {"error_info": "Il n'y a pas de fichier liste_modifiee.xlsx."})


@login_required
def species(request):
    try:
        species_list = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Espèces")
        species_list = species_list.replace({np.nan: None})
        species_list = species_list.to_numpy()
        return render(request, 'stats/species.html', {"species_list": species_list})
    except:
        return render(request, 'stats/website_error.html', {"error_info": "Il n'y a pas de fichier liste_modifiee.xlsx."})


@login_required
def trunks(request):
    try:
        trunks_list = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Troncs")
        trunks_list = trunks_list.replace({np.nan: None})
        trunks_list = trunks_list.to_numpy()
        return render(request, 'stats/trunks.html', {"trunks_list": trunks_list})
    except:
        return render(request, 'stats/website_error.html', {"error_info": "Il n'y a pas de fichier liste_modifiee.xlsx."})


@login_required
def trunk_species(request):
    try:
        trunk_species_list = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Espèces par tronc")
        trunk_species_list = trunk_species_list.to_numpy()
        return render(request, 'stats/trunk_species.html', {"trunk_species_list": trunk_species_list})
    except:
        return render(request, 'stats/website_error.html', {"error_info": "Il n'y a pas de fichier liste_modifiee.xlsx."})


@login_required
def errors(request):
    try:
        errors_list = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Erreurs")
        errors_list = errors_list.replace({np.nan: None})
        errors_list = errors_list.to_numpy()
        return render(request, 'stats/errors.html', {"errors_list": errors_list})
    except:
        return render(request, 'stats/website_error.html', {"error_info": "Il n'y a pas de fichier liste_modifiee.xlsx."})


@login_required
def export(request):
    if request.method == 'POST':
        original_file = request.FILES['original_file']
        default_storage.save("files/import/liste_originale_" + str(datetime.date(datetime.now())) + ".xls",
                             ContentFile(original_file.read()))
        try:
            export_function(original_file)
            return redirect('home')
        except:
            return render(request, 'stats/website_error.html',
                          {"error_info": "Il y a eu un problème lors de la génération du fichier."})
    return render(request, 'stats/export.html')


@login_required
def distribution(request):
    try:
        data = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")
    except:
        return render(request, 'stats/website_error.html', {"error_info": "Il n'y a pas de fichier liste_modifiee.xlsx."})

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
    try:
        data = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")
    except:
        return render(request, 'stats/website_error.html', {"error_info": "Il n'y a pas de fichier liste_modifiee.xlsx."})

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
    try:
        data = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")
    except:
        return render(request, 'stats/website_error.html', {"error_info": "Il n'y a pas de fichier liste_modifiee.xlsx."})

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
    try:
        data = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")
    except:
        return render(request, 'stats/website_error.html', {"error_info": "Il n'y a pas de fichier liste_modifiee.xlsx."})

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
    try:
        data = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")
    except:
        return render(request, 'stats/website_error.html', {"error_info": "Il n'y a pas de fichier liste_modifiee.xlsx."})

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
def file(request, folder, filename, extension):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = base_dir + '/files/' + folder + "/" + filename + "." + extension
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=" + filename + "." + extension
    return response


@login_required
def archives_original_files(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files_list = os.listdir(base_dir + "/files/import")
    files_list = [i.split('.') for i in files_list]
    return render(request, 'stats/archives_original_files.html', {"files_list": files_list})
