from django import forms
from django_countries import countries
from .models import Organization
from django.utils.translation import gettext_lazy as _

input_classes: str = "w-full focus:outline-1 focus:outline-primary/40 p-2 border border-neutral-200 rounded-md pl-9 validator text-sm text-base-content"

class OrganizationModelForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            'name', 'is_org', 
            'first_name', 'last_name', 
            'logo', 'legal_id_name', 
            'legal_id', 
            'subscription_start', 'subscription_end',
            'trial_start', 'trial_end', 
            'country', 'address'
        ]
        widgets = {
            "is_org": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "name": forms.TextInput(attrs={"class": input_classes, "placeholder": _("Organization name")}),
            "first_name": forms.TextInput(attrs={"class": input_classes, "placeholder": _("First name")}),
            "last_name": forms.TextInput(attrs={"class": input_classes, "placeholder": _("Last name")}),
            "logo": forms.ClearableFileInput(attrs={"class": input_classes+ " file-input", "placeholder": _("Logo")}),
            "legal_id_name": forms.TextInput(attrs={"class": input_classes, "placeholder": _("Type of legal ID. (e.g: SIRET)")}),
            "legal_id": forms.TextInput(attrs={"class": input_classes, "placeholder": _("Legal ID number")}),
            "subscription_start": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "subscription_end": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "subscription_duration": forms.NumberInput(attrs={"class": "form-control"}),
            "trial_start": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "trial_end": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "country": forms.Select(attrs={"class": input_classes}),
            "address": forms.Textarea(attrs={"class": input_classes + " resize-none", "rows": 2, "placeholder": _("Address")}),
        }
