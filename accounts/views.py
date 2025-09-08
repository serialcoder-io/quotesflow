from django.shortcuts import render
from allauth.account.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import Organization, OrganizationUser
from .forms import OrganizationModelForm


def index_view(request):
    return render(request, 'index.html')

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        # Si l’utilisateur n’a pas d’organisation
        if not Organization.objects.filter(owner=user).exists() and not OrganizationUser.objects.filter(user=user).exists():
            return '/accounts/organizations/create/'  # ton formulaire de création d'organisation
        # Sinon, redirige vers la home (ou LOGIN_REDIRECT_URL)
        return super().get_success_url()


def create_organization(request):
    if request.method == "POST":
        form = OrganizationModelForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            print(request.POST)
        if form.errors:
            for err in form.errors:
                print(err)
    else:
        form = OrganizationModelForm()

    return render(request, "accounts/create_organization.html", {"form": form})