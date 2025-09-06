# accounts/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import Organization, OrganizationUser

class ForceOrganizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            exempt_urls = [
                reverse('create_organization'),
                reverse('account_logout'),
                reverse('account_login'),
                reverse('admin:index'),  # admin home
            ]

            # Vérifie si l'URL est exemptée
            is_exempt = (
                any(request.path.startswith(url) for url in exempt_urls) or
                request.path.startswith('/admin/')
            )

            if (not Organization.objects.filter(owner=request.user).exists() and
                not OrganizationUser.objects.filter(user=request.user).exists() and
                not is_exempt):
                return redirect('create_organization')

        return self.get_response(request)

