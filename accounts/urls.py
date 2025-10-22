from django.urls import include, path
from accounts.views import create_organization, customer_management, dashboard, home

urlpatterns = [
    path("organizations/create/", create_organization, name="create_organization"),
    path("organizations/<uuid:id>/dashboard/", dashboard, name="dashboard"),
    path("organizations/<uuid:id>/customer_management/", customer_management, name="customer_management"),
    path("organizations/", home, name="home"),
]