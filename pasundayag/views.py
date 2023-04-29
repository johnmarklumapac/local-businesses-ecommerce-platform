from datetime import date

import numpy as np
import pandas as pd
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.decorators import user_passes_test

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
@user_passes_test(lambda u: u.is_superuser)
def index(request):
    ipcr_list = IPCR.objects.prefetch_related("ipcr_image").filter(is_active=True)
    current_month = date.today().month
    current_year = date.today().year
    years = range(current_year, current_year - 10, -1)

    annual_counts = []
    ipcrs = AnnualIPCR.objects.filter(year=current_year)
    for annualipcr in ipcrs:
        annualipcr.calculate_annual_numerical_rating()
    os = ipcrs.filter(annual_adjectival_rating="Outstanding").count()
    vsf = ipcrs.filter(annual_adjectival_rating="Very Satisfactory").count()
    sf = ipcrs.filter(annual_adjectival_rating="Satisfactory").count()
    usf = ipcrs.filter(annual_adjectival_rating="Unsatisfactory").count()
    pr = ipcrs.filter(annual_adjectival_rating="Poor").count()
    annual_counts.append(
        {
            "year": current_year,
            "os": os,
            "vsf": vsf,
            "sf": sf,
            "usf": usf,
            "pr": pr,
        }
    )

    context = {
        "ipcrs": ipcr_list,
        "annual_counts": annual_counts,
        "years": years,
        "current_year": current_year,
        "os_label": "Outstanding",
        "vsf_label": "Very Satisfactory",
        "sf_label": "Satisfactory",
        "usf_label": "Unsatisfactory",
        "pr_label": "Poor",
    }
    return render(request, "pasundayag/index.html", context)

@user_passes_test(lambda u: u.is_superuser)
def index_02(request, year):
    ipcr_list = IPCR.objects.prefetch_related("ipcr_image").filter(is_active=True)
    current_month = date.today().month
    current_year = date.today().year
    years = range(current_year, current_year - 10, -1)

    annual_counts = []
    ipcrs = AnnualIPCR.objects.filter(year=year)
    for annualipcr in ipcrs:
        annualipcr.calculate_annual_numerical_rating()
    os = ipcrs.filter(annual_adjectival_rating="Outstanding").count()
    vsf = ipcrs.filter(annual_adjectival_rating="Very Satisfactory").count()
    sf = ipcrs.filter(annual_adjectival_rating="Satisfactory").count()
    usf = ipcrs.filter(annual_adjectival_rating="Unsatisfactory").count()
    pr = ipcrs.filter(annual_adjectival_rating="Poor").count()
    annual_counts.append(
        {
            "year": current_year,
            "os": os,
            "vsf": vsf,
            "sf": sf,
            "usf": usf,
            "pr": pr,
        }
    )

    context = {
        "ipcrs": ipcr_list,
        "annual_counts": annual_counts,
        "years": years,
        "current_year": current_year,
        "os_label": "Outstanding",
        "vsf_label": "Very Satisfactory",
        "sf_label": "Satisfactory",
        "usf_label": "Unsatisfactory",
        "pr_label": "Poor",
    }
    context["year"] = year
    context["current_year"] = year
    return render(request, "pasundayag/index_02.html", context)

@user_passes_test(lambda u: u.is_superuser)
def index_03(request, year, rating):
    annual_ipcr_list = AnnualIPCR.objects.filter(annual_adjectival_rating=rating, year=year).order_by(
        "-annual_numerical_rating"
    )
    annual_ipcr_count = AnnualIPCR.objects.filter(annual_adjectival_rating=rating, year=year).count()
    current_year = date.today().year
    years = range(current_year, current_year - 10, -1)
    context["rating"] = rating
    context["annual_ipcr_list"] = annual_ipcr_list
    context["annual_ipcr_count"] = annual_ipcr_count
    context["years"] = years

    return render(request, "pasundayag/index_03.html", context)

@user_passes_test(lambda u: u.is_superuser)
def ipcr_all(request):
    personnel_list = Personnel.objects.filter(
        ~Q(is_superuser=True),
        ~Q(is_staff=True),
        id__in=IPCR.objects.values_list('personnel_id', flat=True).distinct()
    )
    all_personnel = Personnel.objects.filter(~Q(is_superuser=True) & ~Q(is_staff=True))
    personnel_count = personnel_list.count()
    ipcrs = IPCR.objects.prefetch_related("ipcr_image").filter(is_active=True)
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
        "personnel_list": personnel_list,
        "all_personnel": all_personnel,
        "personnel_count": personnel_count,
        "ipcrs": ipcrs,
        "years": years,
    }
    return render(request, "pasundayag/ipcr_all.html", context)

@login_required
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
    pf_ipcr_list = PersonnelFunctionIPCR.objects.all()
    psf_ipcr = PersonnelSubfunctionIPCR.objects.all()
    current_year = date.today().year
    years = range(current_year, current_year - 10, -1)
    context["ipcrs"] = ipcrs
    context["personnel"] = personnel
    context["ipcrs"] = ipcrs
    context["pf_ipcr_list"] = pf_ipcr_list
    context["psf_ipcr"] = psf_ipcr
    context["years"] = years
    return render(request, "pasundayag/ipcr_per_personnel.html", context)

@user_passes_test(lambda u: u.is_superuser)
def ipcr_per_rank(request, slug=None):
    rank = get_object_or_404(Rank, slug=slug)
    ipcr_list = IPCR.objects.filter(personnel__rank=rank)
    personnel_list = Personnel.objects.filter(
        ~Q(is_superuser=True),
        ~Q(is_staff=True),
        id__in=IPCR.objects.values_list('personnel_id', flat=True).distinct(),
        rank=rank
    )
    all_personnel = Personnel.objects.filter(~Q(is_superuser=True) & ~Q(is_staff=True) & Q(rank=rank))
    personnel_count = personnel_list.count()
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
        "personnel_list": personnel_list,
        "all_personnel": all_personnel,
        "personnel_count": personnel_count,
        "rank": rank,
        "ipcr_list": ipcr_list,
        "years": years,
    }

    return render(request, "pasundayag/ipcr_per_rank.html", context)

@user_passes_test(lambda u: u.is_superuser)
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
        annual_ipcrs_3 = AnnualIPCR.objects.filter(personnel=personnel).order_by("-year")[:3]
        annual_ipcrs_5 = AnnualIPCR.objects.filter(personnel=personnel).order_by("-year")[:5]
        for annualipcr in annual_ipcrs_3:
            annualipcr.calculate_annual_numerical_rating()
        for annualipcr in annual_ipcrs_5:
            annualipcr.calculate_annual_numerical_rating()
    except AnnualIPCR.DoesNotExist:
        annual_ipcrs_3 = None
        annual_ipcrs_5 = None
    context["annual_ipcrs_3"] = annual_ipcrs_3
    context["annual_ipcrs_5"] = annual_ipcrs_5
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


@user_passes_test(lambda u: u.is_superuser)
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
                    return redirect(
                        "/ipcr-detail-rating/" + str(personnel.id) + "-" + str(year) + "-" + str(period) + "/"
                    )

            else:
                form = IPCRForm()

            context["error"] = form.errors
            context["form"] = form
            return render(request, "pasundayag/rate_personnel.html", context)

        else:
            return redirect("admin:login")


from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


@user_passes_test(lambda u: u.is_superuser)
def update_personnel_ipcr(request, pk, personnel_name, year, period):
    ipcr = get_object_or_404(IPCR, pk=pk)
    form = IPCRForm(request.POST or None, instance=ipcr)

    if form.is_valid():
        form.save()
        personnel_id = ipcr.personnel.id
        year = ipcr.year
        period = ipcr.period
        return redirect("/ipcr-detail-rating/" + str(personnel_id) + "-" + str(year) + "-" + str(period) + "/")

    context = {"form": form, "ipcr": ipcr, "personnel_id": personnel_name, "year": year, "period": period}
    return render(request, "pasundayag/ipcr_detail_update.html", context)


@user_passes_test(lambda u: u.is_superuser)
def academic_title(request):
    rank_list = Rank.objects.all().order_by("pk")
    for rank in rank_list:
        personnel_count = Personnel.objects.filter(rank__id=rank.id).count()
        rank.personnel_count = personnel_count
    context["rank_list"] = rank_list

    return render(request, "pasundayag/academic_title.html", context)


@user_passes_test(lambda u: u.is_superuser)
def personnel_per_title(request, slug):
    rank = Rank.objects.get(slug=slug)
    personnel_list = Personnel.objects.filter(rank__id=rank.id)
    for personnel in personnel_list:
        annual_ipcr = AnnualIPCR.objects.filter(personnel__id=personnel.id).first()
        personnel.annual_ipcr = annual_ipcr
    personnel_count = Personnel.objects.filter(rank__id=rank.id).count()
    context["rank"] = rank
    context["personnel_list"] = personnel_list
    context["personnel_count"] = personnel_count

    return render(request, "pasundayag/personnel_per_academic_title.html", context)


@login_required
def logoutuser(request):
    logout(request)
    return redirect("/")

@user_passes_test(lambda u: u.is_superuser)
def annualipcr_chart(request):
    requested_year = request.GET.get("year", None)
    if requested_year is not None:
        data = AnnualIPCR.objects.filter(year__range=[int(requested_year) - 2, int(requested_year)])
    else:
        data = AnnualIPCR.objects.all()

    df = pd.DataFrame(list(data.values()))
    df = (
        df.groupby(
            [
                "year",
                "annual_adjectival_rating",
            ]
        )
        .size()
        .reset_index(name="count")
    )
    df = df.pivot_table(index="year", columns="annual_adjectival_rating", values="count", fill_value=0).reset_index()

    # Filter the data based on the requested year
    if requested_year is not None:
        df = df.loc[df["year"].isin([str(y) for y in range(int(requested_year) - 2, int(requested_year) + 1)])]

    # Add the "year" column to the JSON data
    data = df.to_dict("records")
    for item in data:
        item["year"] = str(item["year"])

    return JsonResponse(data, safe=False)
