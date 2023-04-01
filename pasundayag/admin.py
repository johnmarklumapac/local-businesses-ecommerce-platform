from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django.forms import DecimalField
from .forms import PersonnelFunctionIPCRForm, PersonnelSubfunctionIPCRForm
from .models import IPCR, IPCRType, Rank, AnnualIPCR

admin.site.register(IPCRType)


class IPCRAdmin(admin.ModelAdmin):
    list_display = (
        "personnel",
        "rank",
        "year",
        "period",
    )
    save_as = True
    prepopulated_field = {"rank": ("personnel__rank",)}


admin.site.register(IPCR, IPCRAdmin)
admin.site.register(Rank, MPTTModelAdmin)

class AnnualIPCRAdmin(admin.ModelAdmin):
    list_display = (
        "personnel",
        "rank",
        "year",
        "annual_numerical_rating",
        "annual_adjectival_rating",
        
    )
    save_as = True

admin.site.register(AnnualIPCR, AnnualIPCRAdmin)
