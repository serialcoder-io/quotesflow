from django.urls import include, path
from accounts.views import create_organization, dashboard

urlpatterns = [
    path("organizations/create/", create_organization, name="create_organization"),
    path("organizations/dashboard/", dashboard, name="dashboard"),
]