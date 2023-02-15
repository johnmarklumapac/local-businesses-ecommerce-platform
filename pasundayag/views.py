from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.db.models import Q
from datetime import date
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from . forms import PersonnelFunctionIPCRForm, PersonnelSubfunctionIPCRForm, FunctionFormSet, SubfunctionFormSet, PersonnelIPCRForm
from .models import Personnel, IPCR, Rank, Area, Function, Subfunction, PersonnelFunctionIPCR, PersonnelSubfunctionIPCR

area_list = Area.objects.all()
context = {
    'area_list' : area_list,
    'area_list_limited' : area_list[:3]
}
@login_required
def index(request):
    ipcrs = IPCR.objects.prefetch_related("ipcr_image").filter(is_active=True)
    return render(request, "pasundayag/index.html", {"ipcrs": ipcrs})

def ipcr_all(request):
    personnel_list = Personnel.objects.filter(~Q(is_superuser=True) & ~Q(is_staff=True))
    ipcrs = IPCR.objects.prefetch_related("ipcr_image").filter(is_active=True)
    current_year = date.today().year
    years = range(current_year, current_year-10, -1)
    context['personnel_list'] = personnel_list
    context['ipcrs'] = ipcrs
    context['years'] = years
    return render(request, "pasundayag/ipcr_all.html", context)


def rank_list(request, rank_slug=None):
    rank = get_object_or_404(Rank, slug=rank_slug)
    ipcrs = IPCR.objects.filter(rank__in=Rank.objects.get(slug=rank_slug).get_descendants(include_self=True))
    
    return render(request, "pasundayag/ipcr_per_rank.html", {"rank": rank, "ipcrs": ipcrs})


def ipcr_add(request):
    area_list = Area.objects.all()
    function_list = Function.objects.all()
    sfunction_list = Subfunction.objects.all()
    form1 = PersonnelFunctionIPCRForm
    form2 = PersonnelSubfunctionIPCRForm

    context['area_list'] =  area_list
    context['function_list'] =  function_list
    context['sfunction_list'] =  sfunction_list
    context['form1'] = form1
    context['form2'] = form2
    return render(request, "pasundayag/ipcr_add.html", context)

@login_required
def ipcr_detail(request, personnel_id, year, period):
    personnel = Personnel.objects.get(pk=personnel_id)
    context['personnel'] = personnel
    context['year'] = year
    context['period'] = period
    area_list = Area.objects.all()
    function_list = Function.objects.all()
    sfunction_list = Subfunction.objects.all()
    pf_ipcr = PersonnelFunctionIPCR.objects.filter(Q(personnel_id=personnel_id) & Q(year=year) & Q(period=period))
    pf_ipcr_count = PersonnelFunctionIPCR.objects.filter(Q(personnel_id=personnel_id) & Q(year=year) & Q(period=period)).count()
    psf_ipcr = PersonnelSubfunctionIPCR.objects.filter(Q(personnel_id=personnel_id) & Q(year=year) & Q(period=period))
    psf_ipcr_count = PersonnelSubfunctionIPCR.objects.filter(Q(personnel_id=personnel_id) & Q(year=year) & Q(period=period)).count()
    context['area_list'] =  area_list
    context['function_list'] =  function_list
    context['pf_ipcr'] =  pf_ipcr
    context['pf_ipcr_count'] =  pf_ipcr_count
    context['psf_ipcr'] =  psf_ipcr
    context['psf_ipcr_count'] =  psf_ipcr_count
    context['sfunction_list'] =  sfunction_list
    return render(request, "pasundayag/ipcr_detail.html", context)


@login_required
def rate_personnel(request, personnel_id, year, period):
    personnel = Personnel.objects.get(pk=personnel_id)
    context['personnel'] = personnel
    context['year'] = year
    context['period'] = period
    if request.user.is_superuser:
        area_list = Area.objects.all()
        function_list = Function.objects.all()
        sfunction_list = Subfunction.objects.all()
        form1 = PersonnelFunctionIPCRForm
        form2 = PersonnelSubfunctionIPCRForm

        context['area_list'] =  area_list
        context['function_list'] =  function_list
        context['sfunction_list'] =  sfunction_list

        if request.method == 'POST':
            function_formset = FunctionFormSet(request.POST, prefix='function')
            subfunction_formset = SubfunctionFormSet(request.POST, prefix='subfunction')
            form = PersonnelIPCRForm(request.POST)

            if form.is_valid() and function_formset.is_valid() and subfunction_formset.is_valid():
                # save the form data
                ipcr = form.save(commit=False)
                ipcr.save()

                # save the function formset data
                for function_form in function_formset:
                    function_ipcr = function_form.save(commit=False)
                    function_ipcr.personnel = ipcr.personnel
                    function_ipcr.year = ipcr.year
                    function_ipcr.period = ipcr.period
                    function_ipcr.function = function_form.cleaned_data['function']
                    function_ipcr.save()

                # save the subfunction formset data
                for subfunction_form in subfunction_formset:
                    subfunction_ipcr = subfunction_form.save(commit=False)
                    subfunction_ipcr.personnel = ipcr.personnel
                    subfunction_ipcr.year = ipcr.year
                    subfunction_ipcr.period = ipcr.period
                    subfunction_ipcr.subfunction = subfunction_form.cleaned_data['subfunction']
                    subfunction_ipcr.save()

                return redirect('/')

        else:
            function_formset = FunctionFormSet(prefix='function')
            subfunction_formset = SubfunctionFormSet(prefix='subfunction')
            form = PersonnelIPCRForm()
            context['function_formset'] = function_formset
            context['subfunction_formset'] = subfunction_formset
            context['form'] = form

        return render(request, 'pasundayag/rate_personnel.html', context)
    
    else: 
        return redirect('admin:login')

@login_required
def logoutuser(request):
    logout(request)
    return redirect('/')