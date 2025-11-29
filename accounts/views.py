import uuid
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from allauth.account.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import Customer, Organization, OrganizationUser
#from accounts.utils import get_current_organization_context
from .helpers.organization import get_current_organization_context
from .forms import CustomerModelForm, OrganizationModelForm
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
def dashboard(request, id: uuid):
    context = get_current_organization_context(request, id)
    return render(request, "accounts/organization/dashboard.html", context)


@login_required
def customers(request, id: uuid):
    context = get_current_organization_context(request, id)
    org = context["organization"]
    customers_for_org = org.customers.all()
    paginator = Paginator(customers_for_org, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    new_customer_form = CustomerModelForm()
    context.update({
        "page_obj": page_obj,
        "new_customer_form": new_customer_form
    })
    return render(request, "accounts/organization/customers.html", context)


def organization_settins(request, id: uuid):
    pass


@login_required
def home(request):
    user_orgs = (
        OrganizationUser.objects
        .filter(
            user=request.user,
            is_active_by_plan=True,
            is_active_by_owner=True
        )
        .select_related("organization")
    )
    return render(request, "accounts/organization/index.html", {"user_orgs": user_orgs})


@login_required
def organization_settings(request, id: uuid):
    context = get_current_organization_context(request, id)
    if request.method == "POST":
        form = OrganizationModelForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            print(request.POST)
        if form.errors:
            for err in form.errors:
                print(err)
    else:
        current_org = context["organization"]
        form = OrganizationModelForm(instance=current_org)

    context.update({
        "form": form
    })
    return render(request, "accounts/organization/settings.html", context)