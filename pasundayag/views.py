from datetime import date

import numpy as np
import pandas as pd
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, Q
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.functions import Coalesce
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from .forms import (
    IPCRForm,

)
from .models import (
    IPCR,
    AnnualIPCR,
    Area,
    Personnel,
    Rank,
)

area_list = Area.objects.all()
context = {"area_list": area_list, "area_list_limited": area_list[:3]}


@login_required
def index(request):
    ipcr_list = IPCR.objects.prefetch_related("ipcr_image").filter(is_active=True)
    current_month = date.today().month
    current_year = date.today().year
    year_list_5 = range(current_year, current_year - 5, -1)
    year_list_3 = range(current_year, current_year - 3, -1)
    years = range(current_year, current_year - 10, -1)

    annual_counts_3 = []
    for year in year_list_3:
        ipcrs = AnnualIPCR.objects.filter(year=year)
        for annualipcr in ipcrs:
            annualipcr.calculate_annual_numerical_rating()
        os = ipcrs.filter(annual_adjectival_rating="Outstanding").count()
        vsf = ipcrs.filter(annual_adjectival_rating="Very Satisfactory").count()
        sf = ipcrs.filter(annual_adjectival_rating="Satisfactory").count()
        usf = ipcrs.filter(annual_adjectival_rating="Unsatisfactory").count()
        pr = ipcrs.filter(annual_adjectival_rating="Poor").count()
        annual_counts_3.append(
            {
                "year": year,
                "os": os,
                "vsf": vsf,
                "sf": sf,
                "usf": usf,
                "pr": pr,
            }
        )

    annual_counts_5 = []
    for year in year_list_5:
        ipcrs = AnnualIPCR.objects.filter(year=year)
        for annualipcr in ipcrs:
            annualipcr.calculate_annual_numerical_rating()
        os = ipcrs.filter(annual_adjectival_rating="Outstanding").count()
        vsf = ipcrs.filter(annual_adjectival_rating="Very Satisfactory").count()
        sf = ipcrs.filter(annual_adjectival_rating="Satisfactory").count()
        usf = ipcrs.filter(annual_adjectival_rating="Unsatisfactory").count()
        pr = ipcrs.filter(annual_adjectival_rating="Poor").count()
        annual_counts_5.append(
            {
                "year": year,
                "os": os,
                "vsf": vsf,
                "sf": sf,
                "usf": usf,
                "pr": pr,
            }
        )

    context = {
        "ipcrs": ipcr_list,
        "annual_counts_3": annual_counts_3,
        "annual_counts_5": annual_counts_5,
        "years": years,
        "current_year": current_year,
        "year_list_3": year_list_3,
        "year_list_5": year_list_5,
        "os_label": "Outstanding",
        "vsf_label": "Very Satisfactory",
        "sf_label": "Satisfactory",
        "usf_label": "Unsatisfactory",
        "pr_label": "Poor",
    }
    return render(request, "pasundayag/index.html", context)


def index_02(request, year):
    ipcr_list = IPCR.objects.prefetch_related("ipcr_image").filter(is_active=True)
    current_month = date.today().month
    current_year = date.today().year
    year_list_5 = range(year, year - 5, -1)
    year_list_3 = range(year, year - 3, -1)
    years = range(current_year, current_year - 10, -1)

    annual_counts_3 = []
    for year in year_list_3:
        ipcrs = AnnualIPCR.objects.filter(year=year)
        for annualipcr in ipcrs:
            annualipcr.calculate_annual_numerical_rating()
        os = ipcrs.filter(annual_adjectival_rating="Outstanding").count()
        vsf = ipcrs.filter(annual_adjectival_rating="Very Satisfactory").count()
        sf = ipcrs.filter(annual_adjectival_rating="Satisfactory").count()
        usf = ipcrs.filter(annual_adjectival_rating="Unsatisfactory").count()
        pr = ipcrs.filter(annual_adjectival_rating="Poor").count()
        annual_counts_3.append(
            {
                "year": year,
                "os": os,
                "vsf": vsf,
                "sf": sf,
                "usf": usf,
                "pr": pr,
            }
        )

    annual_counts_5 = []
    for year in year_list_5:
        ipcrs = AnnualIPCR.objects.filter(year=year)
        for annualipcr in ipcrs:
            annualipcr.calculate_annual_numerical_rating()
        os = ipcrs.filter(annual_adjectival_rating="Outstanding").count()
        vsf = ipcrs.filter(annual_adjectival_rating="Very Satisfactory").count()
        sf = ipcrs.filter(annual_adjectival_rating="Satisfactory").count()
        usf = ipcrs.filter(annual_adjectival_rating="Unsatisfactory").count()
        pr = ipcrs.filter(annual_adjectival_rating="Poor").count()
        annual_counts_5.append(
            {
                "year": year,
                "os": os,
                "vsf": vsf,
                "sf": sf,
                "usf": usf,
                "pr": pr,
            }
        )

    context = {
        "ipcrs": ipcr_list,
        "annual_counts_3": annual_counts_3,
        "annual_counts_5": annual_counts_5,
        "years": years,
        "current_year": current_year,
        "year_list_3": year_list_3,
        "year_list_5": year_list_5,
        "os_label": "Outstanding",
        "vsf_label": "Very Satisfactory",
        "sf_label": "Satisfactory",
        "usf_label": "Unsatisfactory",
        "pr_label": "Poor",
    }
    context["year"] = year + 4
    context['current_year'] = year + 4
    return render(request, "pasundayag/index_02.html", context)


def index_03(request, year, rating):
    annual_ipcr_list = AnnualIPCR.objects.filter(
        annual_adjectival_rating=rating,
        year=year
    ).order_by("-annual_numerical_rating")
    annual_ipcr_count = annual_ipcr_list.count()
    current_year = date.today().year
    years = range(current_year, current_year - 10, -1)
    
    context = {
        'rating': rating,
        'annual_ipcr_list': annual_ipcr_list, # Convert QuerySet to list of dictionaries
        'annual_ipcr_count': annual_ipcr_count,
        'years': years, # Convert range object to list
        'year': year,
    }

    return render(request, "pasundayag/index_03.html", context)

def ipcr_all(request):
    ipcrs = IPCR.objects.prefetch_related("ipcr_image").filter(is_active=True)
    all_personnel = Personnel.objects.filter(~Q(is_superuser=True) & ~Q(is_staff=True))
    personnel_list = Personnel.objects.filter(~Q(is_superuser=True) & ~Q(is_staff=True))
    paginator = Paginator(personnel_list, 10)
    page = request.GET.get("page")
    try:
        personnel_list = paginator.page(page)
    except PageNotAnInteger:
        personnel_list = paginator.page(1)
    except EmptyPage:
        personnel_list = paginator.page(paginator.num_pages)

    current_year = date.today().year
    years = range(current_year, current_year - 10, -1)
    context = {
        "all_personnel": all_personnel,
        "personnel_list": personnel_list,
        "ipcrs": ipcrs,
        "years": years,
    }
    return render(request, "pasundayag/ipcr_all.html", context)


def ipcr_per_personnel(request, personnel_id):
    personnel = Personnel.objects.get(pk=personnel_id)
    ipcrs = IPCR.objects.filter(Q(personnel_id=personnel_id)).order_by("-year")
    paginator = Paginator(ipcrs, 10)
    page = request.GET.get("page")
    try:
        ipcrs = paginator.page(page)
    except PageNotAnInteger:
        ipcrs = paginator.page(1)
    except EmptyPage:
        ipcrs = paginator.page(paginator.num_pages)
    current_year = date.today().year
    years = range(current_year, current_year - 10, -1)
    context = {
        'personnel': personnel,
        'ipcrs': ipcrs,
        'years': years,
    }
    return render(request, "pasundayag/ipcr_per_personnel.html", context)


def rank_list(request, slug=None):
    rank = get_object_or_404(Rank, slug=slug)
    ipcr_list = IPCR.objects.filter(personnel__rank=rank)
    all_personnel = Personnel.objects.filter(~Q(is_superuser=True) & ~Q(is_staff=True) & Q(rank=rank))
    personnel_list = Personnel.objects.filter(~Q(is_superuser=True) & ~Q(is_staff=True) & Q(rank=rank))
    paginator = Paginator(personnel_list, 10)
    page = request.GET.get("page")
    try:
        personnel_list = paginator.page(page)
    except PageNotAnInteger:
        personnel_list = paginator.page(1)
    except EmptyPage:
        personnel_list = paginator.page(paginator.num_pages)

    current_year = date.today().year
    years = range(current_year, current_year - 10, -1)
    context = {
        "all_personnel": all_personnel,
        'personnel_list': personnel_list,
        'rank': rank,
        'ipcr_list': ipcr_list,
        'years': years
    }

    return render(request, "pasundayag/ipcr_per_rank.html", context)

@login_required
def ipcr_detail_rating(request, personnel_id, year, period):
    current_year = date.today().year
    personnel = Personnel.objects.get(pk=personnel_id)
    years = range(current_year, current_year - 10, -1)
    try:
        ipcr = IPCR.objects.get(personnel_id=personnel_id, year=year, period=period)

    except IPCR.DoesNotExist:
        ipcr = None

    if ipcr:
        if period == "Jan-Jun":
            prev_period = "Jul-Dec"
            prev_year = str(int(year) - 1)
        else:
            prev_period = "Jan-Jun"
            prev_year = year

        try:
            prev_ipcr = (
                IPCR.objects.filter(personnel_id=personnel_id, year=prev_year, period=prev_period)
                .order_by("-period")
                .first()
            )
        except IPCR.DoesNotExist:
            prev_ipcr = None

        ipcr.calculate_stra_total()
        ipcr.calculate_core_acad_total()
        ipcr.calculate_core_prod_total()
        ipcr.calculate_core_tech_total()
        ipcr.calculate_supp_total()
        ipcr.calculate_final_numerical_rating()
        ipcr.stra_save()
        ipcr.core_acad_save()
        ipcr.core_prod_save()
        ipcr.core_tech_save()
        ipcr.supp_save()

        if prev_ipcr:
            prev_ipcr.calculate_stra_total()
            prev_ipcr.calculate_core_acad_total()
            prev_ipcr.calculate_core_prod_total()
            prev_ipcr.calculate_core_tech_total()
            prev_ipcr.calculate_supp_total()
            prev_ipcr.calculate_final_numerical_rating()
            prev_ipcr.stra_save()
            prev_ipcr.core_acad_save()
            prev_ipcr.core_prod_save()
            prev_ipcr.core_tech_save()
            prev_ipcr.supp_save()
            diff = ipcr.final_numerical_percent - prev_ipcr.final_numerical_percent
            context = {
                'years': years,
                'ipcr': ipcr,
                'prev_ipcr': prev_ipcr,
                'personnel': personnel,
                'year': year,
                'period': period,
                'diff': diff
            }

            return render(request, "pasundayag/ipcr_detail_rating.html", context)

        else:
            context = {
                'years': years,
                'ipcr': ipcr,
                'personnel': personnel,
                'year': year,
                'period': period,
            }
            return render(request, "pasundayag/ipcr_detail_rating.html", context)
    else:
        context = {
            'ipcr': ipcr,
            'personnel': personnel,
            'year': year,
            'period': period,
        }

        return render(request, "pasundayag/ipcr_detail_rating.html", context)

@login_required
def ipcr_detail_analytics(request, personnel_id):
    personnel = Personnel.objects.get(id=personnel_id)
    context["personnel"] = personnel
    try:
        annual_ipcrs_3 = AnnualIPCR.objects.filter(personnel=personnel).order_by("year")[:3]
        for annualipcr in annual_ipcrs_3:
            annualipcr.calculate_annual_numerical_rating()
    except AnnualIPCR.DoesNotExist:
        annual_ipcrs = None
    if annual_ipcrs_3:
        context["annual_ipcrs_3"] = annual_ipcrs_3
        return render(request, "pasundayag/ipcr_detail_analytics.html", context)
    else:
        return render(request, "pasundayag/ipcr_detail_analytics.html", context)

@login_required
def rate_personnel(request, personnel_id, year, period):
    personnel = Personnel.objects.get(pk=personnel_id)
    context["personnel"] = personnel
    context["year"] = year
    context["period"] = period
    try:
        ipcr = IPCR.objects.filter(personnel_id=personnel_id, year=year, period=period)
    except IPCR.DoesNotExist:
        ipcr = None

    if ipcr:
        context["ipcr"] = ipcr
        context["message"] = (
            "IPCR already exists for " + personnel.name + " for " + str(period) + " of the year " + str(year)
        )

        return render(request, "pasundayag/rate_personnel.html", context)
    else:
        if request.user.is_superuser:
            if request.method == "POST":
                form = IPCRForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("/")
            else:
                form = IPCRForm()
            
            context['error'] = form.errors
            context["form"] = form
            return render(request, "pasundayag/rate_personnel.html", context)

        else:
            return redirect("admin:login")

class UpdateInfoView(UpdateView):
    model = IPCR
    form_class = IPCRForm
    template_name = 'pasundayag/ipcr_detail_update.html'
    success_url = reverse_lazy('pasundayag:dashboard')

@login_required
def academic_title(request):
    rank_list = Rank.objects.filter(level=0)
    for rank in rank_list:
        personnel_count = Personnel.objects.filter(rank__id=rank.id).count()
        rank.personnel_count = personnel_count
    context["rank_list"] = rank_list
    return render(request, "pasundayag/academic_title.html", context)


@login_required
def personnel_per_title(request, slug):
    rank = Rank.objects.get(slug=slug)
    personnel_list = Personnel.objects.filter(rank__id=rank.id)
    personnel_count = Personnel.objects.filter(rank__id=rank.id).count()
    context["rank"] = rank
    context["personnel_list"] = personnel_list
    context["personnel_count"] = personnel_count

    return render(request, "pasundayag/personnel_per_academic_title.html", context)


@login_required
def logoutuser(request):
    logout(request)
    return redirect("/")
