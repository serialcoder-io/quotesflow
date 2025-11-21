from django import forms
from django_countries import countries
from .models import Customer, Organization
from django.utils.translation import gettext_lazy as _

input_classes: str = "w-full focus:outline-1 focus:outline-primary/40 p-2 border border-neutral-200 rounded-md pl-9 validator text-sm text-base-content"

class OrganizationModelForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            'name', 'is_org', 
            'first_name', 'last_name', 
            'logo', 'legal_id_name', 'legal_id', 
            'industry_choice', 'industry_custom',
            'subscription_start', 'subscription_end',
            'trial_start', 'trial_end', 
            'country', 'address', 'initials'
        ]
        widgets = {
            "is_org": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "name": forms.TextInput(attrs={"class": input_classes, "placeholder": _("Organization name")}),
            "initials": forms.TextInput(attrs={"class": input_classes, "placeholder": _("Organization initials")}),
            "first_name": forms.TextInput(attrs={"class": input_classes, "placeholder": _("First name")}),
            "last_name": forms.TextInput(attrs={"class": input_classes, "placeholder": _("Last name")}),
            "logo": forms.FileInput(attrs={"class": input_classes + " file-input", "placeholder": _("Logo")}),
            "legal_id_name": forms.TextInput(attrs={"class": input_classes, "placeholder": _("Type of legal ID. (e.g: SIRET)")}),
            "legal_id": forms.TextInput(attrs={"class": input_classes, "placeholder": _("Legal ID number")}),
            "industry_choice": forms.Select(attrs={"class": input_classes}),
            "industry_custom": forms.TextInput(attrs={"class": input_classes, "placeholder": _("Business sector")}),
            "subscription_start": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "subscription_end": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "subscription_duration": forms.NumberInput(attrs={"class": "form-control"}),
            "trial_start": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "trial_end": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "country": forms.Select(attrs={"class": input_classes}),
            "address": forms.Textarea(attrs={"class": input_classes + " resize-none", "rows": 2, "placeholder": _("Address")}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        choice = cleaned_data.get("industry_choice")
        custom = cleaned_data.get("industry_custom")
        if not choice and not custom:
            raise forms.ValidationError(_("Please select or enter an industry."))
        return cleaned_data


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'is_company', 'name',
            'first_name', 'last_name', 
            'email', 'contact', 'address'
        ]

        widgets = {
            "is_company": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "name": forms.TextInput(attrs={"class": input_classes, "placeholder": _("Organization name")}),
            "first_name": forms.TextInput(attrs={"class": input_classes, "placeholder": _("First name")}),
            "last_name": forms.TextInput(attrs={"class": input_classes, "placeholder": _("Last name")}),
            "email": forms.TextInput(attrs={"class": input_classes, "placeholder": _("Email")}),
            "contact": forms.TextInput(attrs={"class": input_classes, "placeholder": _("e.g: +230********")}),
            "address": forms.Textarea(attrs={"class": input_classes + " resize-none", "rows": 2, "placeholder": _("Address")}),
        }