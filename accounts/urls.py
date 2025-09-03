from django.urls import include, path
from accounts.views import CustomLoginView, create_organization

urlpatterns = [
    path("organizations/create/", create_organization, name="create_organization"),
]