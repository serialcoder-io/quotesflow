import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin, 
    Group, Permission
)
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django_quill.fields import QuillField
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# --------------------------
# Custom User
# --------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    email = models.EmailField(verbose_name=_('email address'), unique=True)
    first_name = models.CharField(verbose_name=_('first name'), max_length=30, blank=True)
    last_name = models.CharField(verbose_name=_('last name'), max_length=30, blank=True)
    phone_number = models.CharField(verbose_name=_('phone number'), max_length=20, blank=True)
    avatar = models.ImageField(verbose_name=_('profile photo'), upload_to="avatars/", blank=True, null=True)
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    is_staff = models.BooleanField(verbose_name=_('staff status'), default=False)
    date_joined = models.DateTimeField(verbose_name=_('date joined'), auto_now_add=True)
    has_already_been_org_owner = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True, verbose_name=_('user groups'))
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True, verbose_name=_('user permissions'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'custom_user'


# --------------------------
# Organization Permissions, Roles and plan
# --------------------------
class OrgPermissions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    code = models.CharField(verbose_name=_('code'), max_length=20, unique=True)
    label = models.CharField(verbose_name=_('label'), max_length=60)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('organization permission')
        verbose_name_plural = _('organization permissions')
        db_table = 'org_permissions'


class OrgRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    name = models.CharField(verbose_name=_('role name'), max_length=20, unique=True)
    permissions = models.ManyToManyField(OrgPermissions, blank=True, verbose_name=_('permissions'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('organization role')
        verbose_name_plural = _('organization roles')
        db_table = 'org_roles'


# --------------------------
# Plan and features
# --------------------------
class ValueTypeChoices(models.TextChoices):
    BOOLEAN = 'bool', 'Bool'
    INTEGER = 'int', 'Int'

class Feature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    code = models.CharField(verbose_name=_('code'), max_length=50, unique=True)
    value_type = models.CharField(verbose_name=_('value type'), max_length=8, choices=ValueTypeChoices, default=ValueTypeChoices.BOOLEAN, help_text=_('the type of the value: form exp for feature send invoice to client by email, the type of the the vallue will be true or false'))
    description = QuillField(verbose_name=_('description'))

    class Meta:
        db_table = 'features'
        verbose_name = "Feature"
        verbose_name_plural = "Features"

    def __str__(self):
        return self.code


class PlanChoices(models.TextChoices):
    FREE = 'free', _('Free')
    STARTER = 'starter', _('Starter')
    PREMIUM = 'premium', _('Premium')
    ENTREPRISE = 'entreprise', _('Entreprise')

class SubscriptionPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    name = models.CharField(verbose_name=_('plan name'), max_length=12, choices=PlanChoices, default=PlanChoices.FREE)
    monthly_price = models.PositiveBigIntegerField()
    features = models.ManyToManyField(Feature, through='accounts.SubscriptionPlanFeature')

    class Meta:
        db_table = 'subscription_plans'
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plans"
    
    def __str__(self):
        return self.name


class SubscriptionPlanFeature(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name=_('feature'))
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, verbose_name=_('subscription plan'))
    value = models.CharField(verbose_name=_('the value of the feature for the plan'), max_length=60, blank=True)

    class Meta:
        db_table = 'subscription_plan_features'
        verbose_name = "Subscription plan Feature"
        verbose_name_plural = "Subscription plan Features"

    def __str__(self):
        return f"{self.subscription_plan.name} - {self.feature.code}"


# --------------------------
# Organization
# --------------------------
class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    name = models.CharField(verbose_name=_('organization name'), max_length=100, blank=True, null=True)
    slug = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    is_org = models.BooleanField(default=True, verbose_name=_('is organization'))
    owner = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='owned_organizations')
    first_name = models.CharField(verbose_name=_('First name'), max_length=60, blank=True, null=True)
    last_name = models.CharField(verbose_name=_('Last name'), max_length=60, blank=True, null=True)
    logo = models.ImageField(verbose_name=_('logo'), upload_to="org_logos/", blank=True, null=True)
    legal_id_name = models.CharField(verbose_name=_('Type of legal ID'), max_length=50, blank=True, null=True)  # ex: SIRET
    legal_id = models.CharField(verbose_name=_('legal ID number'), max_length=50, blank=True, null=True)
    subscription_plan = models.ForeignKey(
        SubscriptionPlan, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        verbose_name=_('Subscription plan')
    )
    subscription_start = models.DateField(_('subscription start date'), blank=True, null=True)
    subscription_duration = models.PositiveIntegerField(verbose_name=_('duration in month'), default=1)
    subscription_end = models.DateField(_('subscription end date'), blank=True, null=True)
    trial_start = models.DateField(_('trial start date'), blank=True, null=True)
    trial_end = models.DateField(_('trial end date'), blank=True, null=True)
    country = CountryField(verbose_name=_('country'), blank=True, null=True)
    address = models.CharField(verbose_name=_('address'), max_length=200)
    email = models.EmailField(verbose_name=_("Organization email"), blank=True, null=True)
    contact = PhoneNumberField(verbose_name=_("Phone number"), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('creation date'), auto_now_add=True)
    users = models.ManyToManyField(CustomUser, through='accounts.OrganizationUser')

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], condition=models.Q(is_org=True), name='unique_org_name')
        ]
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')
        db_table = 'organizations'
    
    def clean(self):
        if self.is_org and not self.name:
            raise ValidationError({'name': _('Organization name is required.')})
        if not self.is_org and (not self.first_name or not self.last_name):
            raise ValidationError(_('First name and last name are required for individuals.'))

    def save(self, *args, **kwargs):
        if self.pk:
            # Update : récupérer l'ancien nom
            try:
                old_name = Organization.objects.only("name").get(pk=self.pk).name
            except Organization.DoesNotExist:
                old_name = None
            # Si le nom a changé, mettre à jour le slug
            if old_name and old_name != self.name:
                self.slug = slugify(self.name)
        else:
            # Création : générer le slug
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


# --------------------------
# OrganizationUser
# --------------------------
class OrganizationUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_organizations",
        verbose_name=_('user')
    )
    is_active_by_plan = models.BooleanField(default=True, verbose_name=_("active according to subscription plan"))
    is_active_by_owner = models.BooleanField(default=True, verbose_name=_("active according to owner decision"))
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="organization_users",
        verbose_name=_('organization')
    )
    role = models.ForeignKey(
        OrgRole,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('organization user role')
    )
    permissions = models.ManyToManyField(
        OrgPermissions,
        blank=True,
        verbose_name=_('organization user permissions')
    )

    def __str__(self):
        return f"{self.user.email} - {self.organization.name}"

    class Meta:
        verbose_name = _('organization user')
        verbose_name_plural = _('organization users')
        db_table = 'organization_users'


class OrganizationInvitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        'Organization', 
        on_delete=models.CASCADE, 
        related_name='invitations'
    )
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_invitations'
    )
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)  # optionnel

    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    def __str__(self):
        return f"{self.email} invited to {self.organization.name}"
    


class Customer(models.Model):
    organization = models.ForeignKey(
        'Organization', 
        on_delete=models.CASCADE, 
        related_name="customers",
        verbose_name=_("Organisation")
    )
    is_company = models.BooleanField(default=False, verbose_name=_("Is a company"))
    name = models.CharField(max_length=200, verbose_name=_("Customer name"), blank=True, null=True)
    first_name = models.CharField(verbose_name=_('First name'), max_length=60, blank=True, null=True)
    last_name = models.CharField(verbose_name=_('Last name'), max_length=60, blank=True, null=True)
    email = models.EmailField(verbose_name=_("Email"))
    contact = PhoneNumberField(verbose_name=_("Phone number"), blank=True, null=True)
    address = models.CharField(max_length=250, verbose_name=_("Adresse"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))

    class Meta:
        db_table = "customer"
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.name or f"{self.first_name} {self.last_name}"