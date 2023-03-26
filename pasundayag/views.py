from datetime import date

import numpy as np
import pandas as pd
from django.db.models import Avg, Count
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import (
    FunctionFormSet,
    IPCRForm,
    PersonnelFunctionIPCRForm,
    PersonnelIPCRForm,
    PersonnelSubfunctionIPCRForm,
    SubfunctionFormSet,
)
from .models import (
    IPCR,
    AnnualIPCR,
    Area,
    Function,
    Personnel,
    PersonnelFunctionIPCR,
    PersonnelSubfunctionIPCR,
    Rank,
    Subfunction,
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
        annual_counts_3.append({
            'year': year,
            'os': os,
            'vsf': vsf,
            'sf': sf,
            'usf': usf,
            'pr': pr,
        })

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
        annual_counts_5.append({
            'year': year,
            'os': os,
            'vsf': vsf,
            'sf': sf,
            'usf': usf,
            'pr': pr,
        })

    context = {
        'ipcrs': ipcr_list,
        'annual_counts_3': annual_counts_3,
        'annual_counts_5': annual_counts_5,
        'years': years,
        'current_year': current_year,
        'year_list_3': year_list_3,
        'year_list_5': year_list_5,
        'os_label': "Outstanding",
        'vsf_label': "Very Satisfactory",
        'sf_label': "Satisfactory",
        'usf_label': "Unsatisfactory",
        'pr_label': "Poor",
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
        annual_counts_3.append({
            'year': year,
            'os': os,
            'vsf': vsf,
            'sf': sf,
            'usf': usf,
            'pr': pr,
        })

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
        annual_counts_5.append({
            'year': year,
            'os': os,
            'vsf': vsf,
            'sf': sf,
            'usf': usf,
            'pr': pr,
        })

    context = {
        'ipcrs': ipcr_list,
        'annual_counts_3': annual_counts_3,
        'annual_counts_5': annual_counts_5,
        'years': years,
        'current_year': current_year,
        'year_list_3': year_list_3,
        'year_list_5': year_list_5,
        'os_label': "Outstanding",
        'vsf_label': "Very Satisfactory",
        'sf_label': "Satisfactory",
        'usf_label': "Unsatisfactory",
        'pr_label': "Poor",
    }
    context['year'] = year + 4
    return render(request, "pasundayag/index_02.html", context)

def ipcr_all(request):
    personnel_list = Personnel.objects.filter(~Q(is_superuser=True) & ~Q(is_staff=True))
    ipcrs = IPCR.objects.prefetch_related("ipcr_image").filter(is_active=True)
    paginator = Paginator(ipcrs, 10)
    page = request.GET.get("page")
    try:
        ipcrs = paginator.page(page)
    except PageNotAnInteger:
        ipcrs = paginator.page(1)
    except EmptyPage:
        ipcrs = paginator.page(paginator.num_pages)
    pf_ipcr_list = PersonnelFunctionIPCR.objects.all()
    psf_ipcr = PersonnelSubfunctionIPCR.objects.all()
    current_year = date.today().year
    years = range(current_year, current_year - 10, -1)
    context["personnel_list"] = personnel_list
    context["ipcrs"] = ipcrs
    context["pf_ipcr_list"] = pf_ipcr_list
    context["psf_ipcr"] = psf_ipcr
    context["years"] = years
    return render(request, "pasundayag/ipcr_all.html", context)


def rank_list(request, slug=None):
    personnel_list = Personnel.objects.filter(~Q(is_superuser=True) & ~Q(is_staff=True))
    rank = get_object_or_404(Rank, slug=slug)
    ipcr_list = IPCR.objects.filter(personnel__rank=rank)
    paginator = Paginator(ipcr_list, 10)
    page = request.GET.get("page")
    try:
        ipcr_list = paginator.page(page)
    except PageNotAnInteger:
        ipcr_list = paginator.page(1)
    except EmptyPage:
        ipcr_list = paginator.page(paginator.num_pages)
    current_year = date.today().year
    years = range(current_year, current_year - 10, -1)
    context["personnel_list"] = personnel_list
    context["rank"] = rank
    context["ipcr_list"] = ipcr_list
    context["years"] = years

    return render(request, "pasundayag/ipcr_per_rank.html", context)


def ipcr_add(request):
    area_list = Area.objects.all()
    function_list = Function.objects.all()
    sfunction_list = Subfunction.objects.all()
    form1 = PersonnelFunctionIPCRForm
    form2 = PersonnelSubfunctionIPCRForm

    context["area_list"] = area_list
    context["function_list"] = function_list
    context["sfunction_list"] = sfunction_list
    context["form1"] = form1
    context["form2"] = form2
    return render(request, "pasundayag/ipcr_add.html", context)


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
            context["years"] = years
            context["ipcr"] = ipcr
            context["prev_ipcr"] = prev_ipcr
            context["personnel"] = personnel
            context["year"] = year
            context["period"] = period
            context["diff"] = diff

            return render(request, "pasundayag/ipcr_detail_rating.html", context)

        else:
            context["years"] = years
            context["ipcr"] = ipcr
            context["personnel"] = personnel
            context["year"] = year
            context["period"] = period
            return render(request, "pasundayag/ipcr_detail_rating.html", context)
    else:
        context["ipcr"] = ipcr
        context["personnel"] = personnel
        context["year"] = year
        context["period"] = period

        return render(request, "pasundayag/ipcr_detail_rating.html", context)


@login_required
def ipcr_detail_analytics(request, personnel_id):
    personnel = Personnel.objects.get(id=personnel_id)
    context["personnel"] = personnel
    try:
        annual_ipcrs_3 = AnnualIPCR.objects.filter(personnel=personnel).order_by('year')[:3]
        for annualipcr in annual_ipcrs_3:
            annualipcr.calculate_annual_numerical_rating()  
    except AnnualIPCR.DoesNotExist:
        annual_ipcrs = None
    if annual_ipcrs_3:
        context['annual_ipcrs_3'] = annual_ipcrs_3
        return render(request, "pasundayag/ipcr_detail_analytics.html", context)
    else:
        return render(request, "pasundayag/ipcr_detail_analytics.html", context)


@login_required
def ipcr_detail_02(request, personnel_id, year, period):
    personnel = Personnel.objects.get(pk=personnel_id)
    context["personnel"] = personnel
    context["year"] = year
    context["period"] = period
    area_list = Area.objects.all()
    function_list = Function.objects.filter(period=period)
    sfunction_list = Subfunction.objects.filter(period=period)
    pf_ipcr_list = PersonnelFunctionIPCR.objects.filter(Q(personnel_id=personnel_id) & Q(year=year) & Q(period=period))
    pf_ipcr_count = pf_ipcr_list.count()

    psf_ipcr = PersonnelSubfunctionIPCR.objects.filter(Q(personnel_id=personnel_id) & Q(year=year) & Q(period=period))
    psf_ipcr_count = psf_ipcr.count()

    context["area_list"] = area_list
    context["function_list"] = function_list
    context["pf_ipcr_list"] = pf_ipcr_list
    context["pf_ipcr_count"] = pf_ipcr_count
    context["psf_ipcr"] = psf_ipcr
    context["psf_ipcr_count"] = psf_ipcr_count
    context["sfunction_list"] = sfunction_list

    return render(request, "pasundayag/ipcr_detail_02.html", context)


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
            context["form"] = form
            return render(request, "pasundayag/rate_personnel.html", context)

        else:
            return redirect("admin:login")


@login_required
def academic_title(request):
    rank_list = Rank.objects.all()
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
