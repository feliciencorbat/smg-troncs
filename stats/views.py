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
def trunk_species(request, date):
    try:
        observations_list = pd.read_excel("files/export/liste_modifiee.xlsx", sheet_name="Statistiques")

        if date == "last":
            last_date = max(observations_list["Date"])
            observations_list = observations_list[observations_list['Date'] == last_date]
            title = "Dernières observations du "
        else:
            last_date = ""
            title = "Espèces par tronc"

        observations_list = observations_list[["Tronc", "Espèce", "Espèce du tronc"]].groupby(["Tronc", "Espèce du tronc"])["Espèce"].apply(
            lambda x: list(np.unique(x)))
        observations_list = pd.DataFrame({'Tronc': observations_list.index.get_level_values(0),
                                          'Espèce du tronc': observations_list.index.get_level_values(1),
                                          'Espèces': observations_list})
        observations_list["Tronc_int"] = observations_list["Tronc"]
        observations_list["Tronc_int"] = observations_list["Tronc_int"].str.replace("G", "", regex=False)
        observations_list["Tronc_int"] = observations_list["Tronc_int"].str.replace("D", "", regex=False)
        observations_list["Tronc_int"] = observations_list["Tronc_int"].str.replace("_2", "", regex=False)
        observations_list["Tronc_int"] = pd.to_numeric(observations_list["Tronc_int"], errors='coerce')
        observations_list = observations_list.sort_values('Tronc_int')
        observations_list = observations_list.to_numpy()
        return render(request, 'stats/trunk_species.html', {"title": title, "date": last_date, "observations_list": observations_list})
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

        distribution_function(data, variable, title, int(limit), cf, location, str(request.user.id))
        return render(request, 'stats/distribution_view.html', {"folder": "distribution_" + str(request.user.id)})
    else:
        locations = data["Lieu"].dropna().unique()
        variables = get_qualitative_variables()
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

        cramer_function(data, cf, location, str(request.user.id))
        return render(request, 'stats/cramer_view.html', {"folder": "cramer_" + str(request.user.id)})
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

        minimum = int(post_request.get("minimum"))

        p_value, chi2, deg_freedom, contingency, expected, differences, dependence_contribution = chi2_function(data, variable1, variable2, title, species_agg, cf, location, minimum, str(request.user.id))

        contingency.reset_index(inplace=True)
        contingency = pd.DataFrame(np.vstack([contingency.columns, contingency]))
        contingency = contingency.to_numpy()

        expected.reset_index(inplace=True)
        expected = pd.DataFrame(np.vstack([expected.columns, expected]))
        expected = expected.to_numpy()

        differences.reset_index(inplace=True)
        differences = pd.DataFrame(np.vstack([differences.columns, differences]))
        differences = differences.to_numpy()

        dependence_contribution.reset_index(inplace=True)
        dependence_contribution = pd.DataFrame(np.vstack([dependence_contribution.columns, dependence_contribution]))
        dependence_contribution = dependence_contribution.to_numpy()

        return render(request, 'stats/chi2_view.html', {"p_value": p_value, "chi2": chi2, "deg_freedom": deg_freedom, "contingency": contingency, "expected": expected, "differences": differences, "dependence_contribution": dependence_contribution, "folder": "chi2_" + str(request.user.id)})
    else:
        locations = data["Lieu"].dropna().unique()
        variables = get_qualitative_variables()
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

        minimum = int(post_request.get("minimum"))

        shapiro, levene, anova, kruskal = anova_function(data, variable1, variable2, title, cf, location, minimum, str(request.user.id))

        shapiro = pd.DataFrame(np.vstack([shapiro.columns, shapiro]))
        shapiro = shapiro.to_numpy()

        levene = pd.DataFrame(np.vstack([levene.columns, levene]))
        levene = levene.to_numpy()

        anova = pd.DataFrame(np.vstack([anova.columns, anova]))
        anova = anova.to_numpy()

        kruskal = pd.DataFrame(np.vstack([kruskal.columns, kruskal]))
        kruskal = kruskal.to_numpy()

        return render(request, 'stats/anova_view.html', {"shapiro": shapiro, "levene": levene, "anova": anova, "kruskal": kruskal, "folder": "anova_" + str(request.user.id)})
    else:
        locations = data["Lieu"].dropna().unique()
        qualitative_variables = get_qualitative_variables()
        quantitative_variables = get_quantitative_variables()
        return render(request, 'stats/anova.html', {"locations": locations, "qualitative_variables": qualitative_variables, "quantitative_variables": quantitative_variables})


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

        nb_species_evolution_function(data, cf, location, str(request.user.id))
        return render(request, 'stats/nb_species_evolution_view.html', {"folder": "nb_species_evolution_" + str(request.user.id)})
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

def get_qualitative_variables():
    return ['Saison', 'Mois', 'Espèce', 'Espèce actuelle', 'Phylum', 'Ordre', 'Liste rouge', 'Menace', 'Tronc', 'Espèce du tronc', "Lieu", "Groupe troncs"]

def get_quantitative_variables():
     return ['Longueur', 'Diamètre moyen', 'Age du tronc']
