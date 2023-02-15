from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from . forms import PersonnelFunctionIPCRForm, PersonnelSubfunctionIPCRForm
from .models import (
    Rank,
    Area,
    Function,
    Subfunction,
    PersonnelFunctionIPCR,
    PersonnelSubfunctionIPCR
)

admin.site.register(Rank, MPTTModelAdmin)

class AreaAdmin(admin.ModelAdmin):
    list_display = ('rank', 'description', 'percent',)
    list_filter = ('rank',)
    ordering = ('-description',)


admin.site.register(Area, AreaAdmin)

class FunctionAdmin(admin.ModelAdmin):
    list_display = ('area', 'mfo_pap',)
    list_filter = ('area',)
    ordering = ('-area',)

admin.site.register(Function, FunctionAdmin)

class SubfunctionAdmin(admin.ModelAdmin):
    list_display = ('function', 'mfo_pap', 'indicators',)
    list_filter = ('function',)
    ordering = ('-function', 'mfo_pap',)   


admin.site.register(Subfunction, SubfunctionAdmin)

class PFIPCRAdmin(admin.ModelAdmin):
    list_display = ('personnel', 'function', 'year', 'period')
    list_filter = ('personnel','year', 'period',)
    form = PersonnelFunctionIPCRForm

admin.site.register(PersonnelFunctionIPCR, PFIPCRAdmin)

class PSFIPCRAdmin(admin.ModelAdmin):
    list_display = ('personnel', 'subfunction', 'year', 'period')
    list_filter = ('personnel','year', 'period',)
    form = PersonnelSubfunctionIPCRForm
    
admin.site.register(PersonnelSubfunctionIPCR, PSFIPCRAdmin)
