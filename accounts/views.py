from django.shortcuts import render
from allauth.account.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import Organization, OrganizationUser


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
    return render(request, 'accounts/create_organization.html')