from django.http import Http404
from django.shortcuts import get_object_or_404, render
from allauth.account.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import Organization, OrganizationUser
from .forms import OrganizationModelForm
from django.contrib.auth.decorators import login_required

def index_view(request):
    return render(request, 'index.html')


@login_required
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


def dashboard(request, org_slug):
    org = get_object_or_404(
        Organization.objects.only("id", "name", "initials", "logo"),
        slug=org_slug
    )

    user_orgs = OrganizationUser.objects.filter(user=request.user).values('organization__id', 'organization__name', 'organization__slug')

    # check if user belongs to the organization
    is_user_in_org = OrganizationUser.objects.filter(
        user=request.user, organization=org
    ).exists()

    if not is_user_in_org:
        # Hide the existence of the organization if the user is not part of it
        raise Http404("Organization not found.")

    return render(
        request,
        "accounts/organization/dashboard.html",
        {"organization": org, "user_organizations": user_orgs, "current_slug": org_slug}
    )