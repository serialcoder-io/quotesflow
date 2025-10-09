from django.contrib import admin
from accounts.models import (
    CustomUser, Organization, OrganizationInvitation, OrgRole,
    OrganizationUser, OrgPermissions, SubscriptionPlan, SubscriptionPlanFeature,
    Feature
)

# --------------------------
# CustomUser
# --------------------------
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name']
    readonly_fields = ['id']


# --------------------------
# Organization
# --------------------------
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'legal_id_name', 'legal_id']


# --------------------------
# OrgRole
# --------------------------
class OrgRoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['permissions']


# --------------------------
# OrgPermissions
# --------------------------
class OrgPermissionsAdmin(admin.ModelAdmin):
    list_display = ['code', 'label']


# --------------------------
# OrganizationUser
# --------------------------
class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role']
    filter_horizontal = ['permissions']


# --------------------------
# OrganizationInvitation
# --------------------------
class OrganizationInvitationAdmin(admin.ModelAdmin):
    list_display = ['email', 'organization', 'accepted', 'created_at', 'expires_at']
    readonly_fields = ['token', 'created_at']


# --------------------------
# Feature
# --------------------------
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['code', 'value_type']


# --------------------------
# SubscriptionPlanFeature Inline
# --------------------------
class SubscriptionPlanFeatureInline(admin.TabularInline):
    model = SubscriptionPlanFeature
    extra = 1


# --------------------------
# SubscriptionPlan
# --------------------------
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'monthly_price']
    inlines = [SubscriptionPlanFeatureInline]


# --------------------------
# SubscriptionPlanFeature
# --------------------------
class SubscriptionPlanFeatureAdmin(admin.ModelAdmin):
    list_display = ['subscription_plan', 'feature', 'value']


# --------------------------
# Register all
# --------------------------
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrgRole, OrgRoleAdmin)
admin.site.register(OrgPermissions, OrgPermissionsAdmin)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
admin.site.register(OrganizationInvitation, OrganizationInvitationAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(SubscriptionPlanFeature, SubscriptionPlanFeatureAdmin)
