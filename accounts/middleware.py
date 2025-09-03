# accounts/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import Organization, OrganizationUser

class ForceOrganizationMiddleware:
    """
    Force un utilisateur connecté à créer ou rejoindre une organisation
    s'il n'est membre d'aucune organisation et n'en possède aucune.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            exempt_urls = [
                reverse('create_organization'),
                reverse('account_logout'),
                reverse('account_login'),
            ]

            # Vérifie si l'URL est exemptée
            is_exempt = (
                request.path in exempt_urls or
                request.path.startswith('/admin/')
            )

            if (not Organization.objects.filter(owner=request.user).exists() and
                not OrganizationUser.objects.filter(user=request.user).exists() and
                not is_exempt):
                return redirect('create_organization')

        return self.get_response(request)

