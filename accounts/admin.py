from django.contrib import admin
from accounts.models import CustomUser
from .models import Organization
from organizations.models import Organization as OrgDefault

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

# Désenregistrer l'admin par défaut

admin.site.unregister(OrgDefault)

# Enregistrer le custom admin
admin.site.register(Organization, OrganizationAdmin)


admin.site.register(CustomUser, CustomUserAdmin)
