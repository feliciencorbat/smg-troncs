import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from stats.functions.cramer_function import cramer_function
from stats.functions.distribution_function import distribution_function
from stats.functions.export_function import export_function


@login_required
def home(request):
    return render(request, 'stats/home.html')


@login_required
def export(request):
    if request.method == 'POST':
        file = request.FILES['original_file']
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
