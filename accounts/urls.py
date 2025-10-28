from django.urls import include, path
from accounts.views import create_organization, customer_management, dashboard, home, organization_settings

urlpatterns = [
    path("", home, name="home"),
    path("create/", create_organization, name="create_organization"),
    path("<uuid:id>/settings/", organization_settings, name="organization_settings"),
    path("<uuid:id>/dashboard/", dashboard, name="dashboard"),
    path("<uuid:id>/customer_management/", customer_management, name="customer_management"),
]