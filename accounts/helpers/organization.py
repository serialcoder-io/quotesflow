from django.http import Http404
from django.shortcuts import get_object_or_404

from accounts.models import Organization, OrganizationUser



def get_current_organization_context(request, id: int):
    """
    get_current_organization_context retrieves the current organization his slug, and organizations that current user is part.
    """
    org = get_object_or_404(
        Organization.objects.only("id", "name", "initials", "logo", "slug"),
        id=id
    )

    user_orgs = OrganizationUser.objects.filter(
        user=request.user, 
        is_active_by_plan=True, 
        is_active_by_owner=True
    ).values(
        'organization__id', 
        'organization__name', 
        'organization__slug'
    )

    # check if user belongs to the organization
    is_user_in_org = OrganizationUser.objects.filter(
        user=request.user, organization=org
    ).exists()

    if not is_user_in_org:
        # Hide the existence of the organization if the user is not part of it
        raise Http404("Organization not found.")
    
    return {
        "organization": org, 
        "user_organizations": user_orgs,
        "current_slug": org.slug
        }