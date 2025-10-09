from django.urls import include, path
from accounts.views import create_organization, customer_management, dashboard

urlpatterns = [
    path("organizations/create/", create_organization, name="create_organization"),
    path("organizations/<str:org_slug>/dashboard/", dashboard, name="dashboard"),
    path("organizations/<str:org_slug>/customer_management/", customer_management, name="customer_management"),
]