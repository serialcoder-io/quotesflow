"""from django.contrib import admin
from accounts.models import (
    CustomUser, Organization, 
    # OrganizationInvitation, OrgRole ,
    OrganizationUser, OrgPermissions, 
    SubscriptionPlan, SubscriptionPlanFeature,
    Feature
    )


# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name']
    readonly_fields = ['id']


class OrganizationAdmin(admin.ModelAdmin):
    # Champs à afficher dans le formulaire d'ajout/modification
    fields = (
        'name', 'first_name', 'last_name', 'logo',
        'legal_id_name', 'legal_id', 'subscription_plan',
        'subscription_start', 'subscription_duration',
        'country', 'address'
    )

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(CustomUser, CustomUserAdmin)"""
