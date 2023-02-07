from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (
    IPCR,
    IPCRImage,
    IPCRSpecification,
    IPCRSpecificationValue,
    IPCRType,
    Rank,
)

admin.site.register(Rank, MPTTModelAdmin)


class IPCRSpecificationInline(admin.TabularInline):
    model = IPCRSpecification


@admin.register(IPCRType)
class IPCRTypeAdmin(admin.ModelAdmin):
    inlines = [
        IPCRSpecificationInline,
    ]


class IPCRImageInline(admin.TabularInline):
    model = IPCRImage


class IPCRSpecificationValueInline(admin.TabularInline):
    model = IPCRSpecificationValue


@admin.register(IPCR)
class IPCRAdmin(admin.ModelAdmin):
    inlines = [
        IPCRSpecificationValueInline,
        IPCRImageInline,
    ]
