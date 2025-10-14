from django.http import Http404
from django.shortcuts import get_object_or_404, render
from allauth.account.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import Customer, Organization, OrganizationUser
from accounts.utils import get_current_organization_context
from .forms import OrganizationModelForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


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


@login_required
def dashboard(request, org_slug):
    context = get_current_organization_context(request, org_slug)
    return render(request, "accounts/organization/dashboard.html", context)


@login_required
def customer_management(request, org_slug):
    context = get_current_organization_context(request, org_slug)
    org = context["organization"]
    customers_for_org = org.customers.all()
    paginator = Paginator(customers_for_org, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    context.update({
        "page_obj": page_obj
    })
    return render(request, "accounts/organization/customer_management.html", context)