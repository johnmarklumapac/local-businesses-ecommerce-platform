import datetime
import os

from django import forms
from django.db.models import Q
from django.forms import modelformset_factory

from .models import (
    IPCR,
    Function,
    Personnel,
    PersonnelFunctionIPCR,
    PersonnelSubfunctionIPCR,
    Subfunction,
)

FunctionFormSet = modelformset_factory(
    PersonnelFunctionIPCR, fields=("accomplishments", "rating_Q", "rating_E", "rating_T", "remarks")
)

SubfunctionFormSet = modelformset_factory(
    PersonnelSubfunctionIPCR, fields=("accomplishments", "rating_Q", "rating_E", "rating_T", "remarks")
)


class YearSelect(forms.Select):
    def __init__(self, attrs=None):
        year_range = range(1990, datetime.date.today().year + 1)
        choices = [("", "Please select year...")] + [(year, year) for year in year_range]
        super().__init__(attrs, choices)


class PersonnelIPCRForm(forms.ModelForm):
    year = forms.IntegerField(widget=YearSelect, initial="")

    class Meta:
        model = PersonnelFunctionIPCR
        fields = (
            "personnel",
            "year",
            "period",
            "function",
            "subfunction",
            "accomplishments",
            "rating_Q",
            "rating_E",
            "rating_T",
            "remarks",
        )

    subfunction = forms.ModelChoiceField(queryset=Subfunction.objects.all())

    def __init__(self, *args, **kwargs):
        super(PersonnelIPCRForm, self).__init__(*args, **kwargs)
        self.fields["personnel"].choices = [(None, "Please select personnel to rate...")] + list(
            self.fields["personnel"].choices
        )[1:]
        self.fields["year"].widget.attrs["class"] = "form-control"
        self.fields["period"].widget.attrs["class"] = "form-control"
        self.fields["accomplishments"].widget.attrs["class"] = "form-control"
        self.fields["remarks"].widget.attrs["class"] = "form-control"


class PersonnelFunctionIPCRForm(forms.ModelForm):
    year = forms.IntegerField(widget=YearSelect, initial="")
    personnel = forms.ModelChoiceField(
        queryset=Personnel.objects.filter(~Q(is_superuser=True) & ~Q(is_staff=True)),
        initial=None,
        empty_label="Please select a personnel to rate...",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    function = forms.ModelChoiceField(
        queryset=Function.objects.all(),
        initial=None,
        empty_label="Please select a function...",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    rating_Q = forms.IntegerFieldwidget = forms.Select(attrs={"class": "form-control"})
    rating_E = forms.IntegerFieldwidget = forms.Select(attrs={"class": "form-control"})
    rating_T = forms.IntegerFieldwidget = forms.Select(attrs={"class": "form-control"})

    class Meta:
        model = PersonnelFunctionIPCR
        fields = ("personnel", "year", "period", "accomplishments", "rating_Q", "rating_E", "rating_T", "remarks")

    def __init__(self, *args, **kwargs):
        super(PersonnelFunctionIPCRForm, self).__init__(*args, **kwargs)
        self.fields["personnel"].choices = [(None, "Please select personnel to rate...")] + list(
            self.fields["personnel"].choices
        )[1:]
        self.fields["year"].widget.attrs["class"] = "form-control"
        self.fields["period"].widget.attrs["class"] = "form-control"
        self.fields["accomplishments"].widget.attrs["class"] = "form-control"
        self.fields["remarks"].widget.attrs["class"] = "form-control"


class PersonnelSubfunctionIPCRForm(forms.ModelForm):
    year = forms.IntegerField(widget=YearSelect, initial="")
    personnel = forms.ModelChoiceField(
        queryset=Personnel.objects.filter(~Q(is_superuser=True) & ~Q(is_staff=True)),
        initial=None,
        empty_label="Please select a personnel to rate...",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    subfunction = forms.ModelChoiceField(
        queryset=Subfunction.objects.all(),
        initial=None,
        empty_label="Please select a function...",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = PersonnelSubfunctionIPCR
        fields = ("personnel", "year", "period", "accomplishments", "rating_Q", "rating_E", "rating_T", "remarks")

    def __init__(self, *args, **kwargs):
        super(PersonnelSubfunctionIPCRForm, self).__init__(*args, **kwargs)
        self.fields["personnel"].choices = [(None, "Please select personnel to rate...")] + list(
            self.fields["personnel"].choices
        )[1:]
        self.fields["year"].widget.attrs["class"] = "form-control"
        self.fields["period"].widget.attrs["class"] = "form-control"
        self.fields["accomplishments"].widget.attrs["class"] = "form-control"
        self.fields["remarks"].widget.attrs["class"] = "form-control"


class IPCRForm(forms.ModelForm):
    class Meta:
        model = IPCR
        fields = "__all__"

        def __init__(self, *args, **kwargs):
            super(IPCRForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update({"class": "form-control"})
