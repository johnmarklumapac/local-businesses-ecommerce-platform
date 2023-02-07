from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from account.models import Customer


class Rank(MPTTModel):
    """
    Rank Table implimented with MPTT.
    """

    name = models.CharField(
        verbose_name=_("Rank Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(verbose_name=_("Rank safe URL"), max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Rank")
        verbose_name_plural = _("Ranks")

    def get_absolute_url(self):
        return reverse("pasundayag:rank_list", args=[self.slug])

    def __str__(self):
        return self.name


class IPCRType(models.Model):
    """
    IPCRType Table will provide a list of the different types
    of ipcrs that are for sale.
    """

    name = models.CharField(verbose_name=_("IPCR Name"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Employement Status")
        verbose_name_plural = _("Employement Status")

    def __str__(self):
        return self.name


class IPCRSpecification(models.Model):
    """
    The IPCR Specification Table contains ipcr
    specifiction or features for the Employment Status.
    """

    ipcr_type = models.ForeignKey(IPCRType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("IPCR Specification")
        verbose_name_plural = _("IPCR Specifications")

    def __str__(self):
        return self.name


class IPCR(models.Model):
    """
    The IPCR table contining all ipcr items.
    """

    ipcr_type = models.ForeignKey(IPCRType, on_delete=models.RESTRICT)
    rank = models.ForeignKey(Rank, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("Required"),
        max_length=255,
    )
    description = models.TextField(verbose_name=_("description"), help_text=_("Not Required"), blank=True)
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name=_("Regular price"),
        help_text=_("Maximum 99999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 99999.99."),
            },
        },
        max_digits=7,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount price"),
        help_text=_("Maximum 99999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 99999.99."),
            },
        },
        max_digits=5,
        decimal_places=2,
    )
    is_active = models.BooleanField(
        verbose_name=_("IPCR visibility"),
        help_text=_("Change ipcr visibility"),
        default=True,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True)

    stra_e1 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    stra_e2 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    stra_e3 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    stra_a1 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    stra_a2 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    stra_a3 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    stra_total = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_q1 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_q2 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_q3 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_q4 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e1 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e2 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e3 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e4 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e5 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e6 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e7 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e8 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e9 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e10 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e11 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e12 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e13 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e14 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_e15 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_t1 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a1 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a2 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a3 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a4 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a5 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a6 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a7 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a8 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a9 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a10 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a11 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a12 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a13 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a14 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a15 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a16 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a17 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a18 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_a19 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_total1 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    core_total2 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    supp_e1 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    supp_e2 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    supp_e3 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    supp_e4 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    supp_e5 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    supp_t1 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    supp_a1 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    supp_a2 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    supp_a3 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    supp_a4 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    supp_a5 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    supp_a6 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    supp_total = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    final_numerical_rating = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    final_adjectival_rating = models.CharField(
        verbose_name=_("Final Adjectival Rating"), max_length=255, default="Poor"
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("IPCR")
        verbose_name_plural = _("IPCRs")

    def get_absolute_url(self):
        return reverse("pasundayag:ipcr_detail", args=[self.slug])

    def __str__(self):
        return self.title


class IPCRSpecificationValue(models.Model):
    """
    The IPCR Specification Value table holds each of the
    ipcrs individual specification or bespoke features.
    """

    ipcr = models.ForeignKey(IPCR, on_delete=models.CASCADE)
    specification = models.ForeignKey(IPCRSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("IPCR specification value (maximum of 255 words"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("IPCR Specification Value")
        verbose_name_plural = _("IPCR Specification Values")

    def __str__(self):
        return self.value


class IPCRImage(models.Model):
    """
    The IPCR Image table.
    """

    ipcr = models.ForeignKey(IPCR, on_delete=models.CASCADE, related_name="ipcr_image")
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a ipcr image"),
        upload_to="images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("IPCR Image")
        verbose_name_plural = _("IPCR Images")
