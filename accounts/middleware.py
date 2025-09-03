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
        # Ignorer les utilisateurs non authentifiés
        if request.user.is_authenticated:
            # URLs à ignorer pour éviter les boucles
            exempt_urls = [
                reverse('create_organization'),
                reverse('account_logout'),
                reverse('account_login'),
                '/admin/'  # éventuellement d'autres URLs à ignorer
            ]
            
            if (not Organization.objects.filter(owner=request.user).exists() and
                not OrganizationUser.objects.filter(user=request.user).exists() and
                request.path not in exempt_urls):
                return redirect('create_organization')

        response = self.get_response(request)
        return response
