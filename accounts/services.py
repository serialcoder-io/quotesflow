from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import (
    Organization,
    OrganizationUser,
    SubscriptionPlan,
    PlanChoices,
)
from django.conf import settings

TRIAL_DAYS = getattr(settings, "DEFAULT_TRIAL_DAYS", 15)

def create_organization_for_user(user, name, **extra_fields):
    """
    Crée une organisation en appliquant la règle :
      - si user.has_already_been_org_owner == False -> assigner PREMIUM + trial
      - sinon -> assigner FREE par défaut
    Retourne l'instance Organization créée.
    """
    with transaction.atomic():
        # choisir le plan de base
        if not getattr(user, "has_already_been_org_owner", False):
            try:
                plan = SubscriptionPlan.objects.get(name=PlanChoices.PREMIUM)
            except ObjectDoesNotExist:
                # fallback si pas de Premium en DB
                plan = SubscriptionPlan.objects.filter().first()
            trial_start = timezone.now().date()
            trial_end = trial_start + timedelta(days=TRIAL_DAYS)

            org = Organization.objects.create(
                name=name,
                owner=user,
                subscription_plan=plan,
                trial_start=trial_start,
                trial_end=trial_end,
                **extra_fields
            )

            # marquer que l'utilisateur a déjà été owner (bloque futurs trials)
            user.has_already_been_org_owner = True
            user.save(update_fields=["has_already_been_org_owner"])

        else:
            try:
                free_plan = SubscriptionPlan.objects.get(name=PlanChoices.FREE)
            except ObjectDoesNotExist:
                free_plan = SubscriptionPlan.objects.filter().first()

            org = Organization.objects.create(
                name=name,
                owner=user,
                subscription_plan=free_plan,
                **extra_fields
            )

        # créer le lien OrganizationUser pour l'owner (activé)
        OrganizationUser.objects.create(
            user=user,
            organization=org,
            role=None,  # mettre le role "owner" si tu as un role Owner précréé
            # si tu as les champs is_active_by_plan / is_active_by_owner, les set ici:
            # is_active_by_plan=True, is_active_by_owner=True
        )

        return org
