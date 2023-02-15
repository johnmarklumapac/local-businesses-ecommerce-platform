from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from decimal import Decimal
from django.forms.models import ModelChoiceField


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

    ipcr_type = models.ForeignKey(IPCRType, on_delete=models.PROTECT, verbose_name=_("IPCR Type"))
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

    ipcr_type = models.ForeignKey(IPCRType, on_delete=models.PROTECT, verbose_name=_("IPCR Type"))
    rank = models.ForeignKey(Rank, on_delete=models.PROTECT)
    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("Required"),
        max_length=255,
    )
    description = models.TextField(verbose_name=_("description"), help_text=_("Not Required"), blank=True)
    slug = models.SlugField(max_length=255)
    is_active = models.BooleanField(
        verbose_name=_("IPCR visibility"),
        help_text=_("Change IPCR visibility"),
        default=True,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    stra_e1 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    stra_e2 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    stra_e3 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    stra_a1 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    stra_a2 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    stra_a3 = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    stra_total = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    stra_adjectival_rating = models.CharField(
        verbose_name=_("Strategic Function Adjectival Rating"), max_length=255, default="Poor"
    )
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
    core_total = models.DecimalField(max_digits=3, decimal_places=2, default=0.0000)
    core_adjectival_rating = models.CharField(
        verbose_name=_("Core Function Adjectival Rating"), max_length=255, default="Poor"
    )
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
    supp_adjectival_rating = models.CharField(
        verbose_name=_("Support Function Adjectival Rating"), max_length=255, default="Poor"
    )
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

    def calculate_stra_total(self):
        stra_total = (self.stra_a1 + self.stra_a2 + self.stra_a3)
        stra_total_avg = stra_total / 3
        stra_percent = ((((stra_total) / (3 * 5)) * 100) / 100) * 30
        stra_total = (stra_total / 3) * Decimal(0.30)
        self.stra_total_avg = round(stra_total_avg, 2)
        self.stra_percent = round(stra_percent, 2)
        self.stra_total = round(stra_total, 2)
        self.save()

    def calculate_core_total(self):
        core_total = (
            self.core_a1
            + self.core_a2
            + self.core_a3
            + self.core_a4
            + self.core_a5
            + self.core_a6
            + self.core_a7
            + self.core_a8
            + self.core_a9
            + self.core_a10
            + self.core_a11
            + self.core_a12
            + self.core_a13
            + self.core_a14
            + self.core_a15
            + self.core_a16
            + self.core_a17
            + self.core_a18
            + self.core_a19
        )
        core_acad_total_avg = (
            self.core_a1
            + self.core_a2
            + self.core_a3
            + self.core_a4
            + self.core_a5
            + self.core_a6
        ) / 6
        core_prod_total_avg = (
            self.core_a7
            + self.core_a8
            + self.core_a9
            + self.core_a10
            + self.core_a11
            + self.core_a12
        ) / 6
        core_tech_total_avg = (
            self.core_a13
            + self.core_a14
            + self.core_a15
            + self.core_a16
            + self.core_a17
            + self.core_a18
            + self.core_a19
        ) / 7

        core_percent = ((((core_total) / (19 * 5)) * 100) / 100) * 60
        core_total = (core_total / 19 ) * Decimal(0.30)
        self.core_acad_total_avg = round(core_acad_total_avg, 2)
        self.core_prod_total_avg= round(core_prod_total_avg, 2)
        self.core_tech_total_avg= round(core_tech_total_avg, 2)
        self.core_percent = round(core_percent, 2)
        self.core_total = round(core_total, 2)
        self.save()

    def calculate_supp_total(self):
        supp_total = (self.supp_a1 + self.supp_a2 + self.supp_a3 + self.supp_a4 + self.supp_a5 + self.supp_a6)
        supp_total_avg = supp_total / 6
        supp_percent = ((((supp_total) / (6 * 5)) * 100) / 100) * 10
        supp_total = (supp_total / 6 ) * Decimal(0.30)
        self.supp_total_avg = round(supp_total_avg, 2)
        self.supp_percent = round(supp_percent, 2)
        self.supp_total = round(supp_total, 2)
        self.save()

    def calculate_final_numerical_rating(self):
        final_numerical_rating = (
            self.stra_total_avg
            + self.core_acad_total_avg
            + self.core_prod_total_avg
            + self.core_tech_total_avg
            + self.supp_total_avg
        )
        final_numerical_percent = ((((final_numerical_rating) / (5 * 5)) * 100) / 100 ) * 100
        final_numerical_rating = (final_numerical_rating / 5)
        self.final_numerical_percent = round(final_numerical_percent, 2)
        self.final_numerical_rating = round(final_numerical_rating, 2)
        self.save()

    def stra_save(self, *args, **kwargs):
        if self.stra_total >= 5:
            self.stra_adjectival_rating = "Outstanding"
        elif self.stra_total >= 4:
            self.stra_adjectival_rating = "Very Satisfactory"
        elif self.stra_total >= 3:
            self.stra_adjectival_rating = "Satisfactory"
        elif self.stra_total >= 2:
            self.stra_adjectival_rating = "Unsatisfactory"
        else:
            self.stra_adjectival_rating = "Very Unsatisfactory"
        super().save(*args, **kwargs)

    def core_save(self, *args, **kwargs):
        if self.core_total >= 5:
            self.core_adjectival_rating = "Outstanding"
        elif self.core_total >= 4:
            self.core_adjectival_rating = "Very Satisfactory"
        elif self.core_total >= 3:
            self.core_adjectival_rating = "Satisfactory"
        elif self.core_total >= 2:
            self.core_adjectival_rating = "Unsatisfactory"
        else:
            self.core_adjectival_rating = "Very Unsatisfactory"
        super().save(*args, **kwargs)

    def supp_save(self, *args, **kwargs):
        if self.supp_total >= 5:
            self.supp_adjectival_rating = "Outstanding"
        elif self.supp_total >= 4:
            self.supp_adjectival_rating = "Very Satisfactory"
        elif self.supp_total >= 3:
            self.supp_adjectival_rating = "Satisfactory"
        elif self.supp_total >= 2:
            self.supp_adjectival_rating = "Unsatisfactory"
        else:
            self.core_adjectival_rating = "Very Unsatisfactory"
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.final_numerical_rating >= 5:
            self.final_adjectival_rating = "Outstanding"
        elif self.final_numerical_rating >= 4:
            self.final_adjectival_rating = "Very Satisfactory"
        elif self.final_numerical_rating >= 3:
            self.final_adjectival_rating = "Satisfactory"
        elif self.final_numerical_rating >= 2:
            self.final_adjectival_rating = "Unsatisfactory"
        else:
            self.final_adjectival_rating = "Very Unsatisfactory"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class IPCRSpecificationValue(models.Model):
    """
    The IPCR Specification Value table holds each of the
    ipcrs individual specification or bespoke features.
    """

    ipcr = models.ForeignKey(IPCR, on_delete=models.CASCADE)
    specification = models.ForeignKey(IPCRSpecification, on_delete=models.PROTECT)
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


from account.models import Personnel
from django.db.models import Q

class Area(models.Model):
    rank = models.ForeignKey(Rank, on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    percent = models.DecimalField(decimal_places=2, max_digits=50)

    def __str__(self):
        return str(self.rank) + ' - ' + str(self.description)

    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")
        ordering = ['description']

class Function(models.Model):
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    mfo_pap = models.TextField(verbose_name=_("MFO/PAP"), null=True, blank=True)
    indicators = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.area) + ' - ' + str(self.mfo_pap)

    class Meta:
        verbose_name = _("Function")
        verbose_name_plural = _("Functions")
        ordering = ['mfo_pap']

class Subfunction(models.Model):
    function = models.ForeignKey(Function, on_delete=models.PROTECT)
    mfo_pap = models.TextField(verbose_name=_("MFO/PAP"), null=True, blank=True)
    indicators = models.TextField(null=True, blank=True)
    percent = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)

    def __str__(self):
        return self.mfo_pap

    class Meta:
        verbose_name = _("Subfunction")
        verbose_name_plural = _("Subfunctions")

class PersonnelFunctionIPCR(models.Model):
    PERIODS = [
        ('Select', 'Please select period...'),
        ('Jan-Jun', 'January to June'),
        ('Jul-Dec', 'July to December'),
    ]
    personnel = models.ForeignKey(
        Personnel,
        on_delete=models.CASCADE,
        limit_choices_to=~Q(is_superuser=True) & ~Q(is_staff=True),
    )
    year = models.PositiveSmallIntegerField()
    period = models.CharField(max_length=8, choices=PERIODS, default="Select")
    function = models.ForeignKey(Function, on_delete=models.PROTECT)
    accomplishments = models.TextField(null=True, blank=True)
    rating_Q = models.FloatField(default=0.0, null=True, blank=True)
    rating_E = models.FloatField(default=0.0, null=True, blank=True)
    rating_T = models.FloatField(default=0.0, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.personnel) + ' ' + str(self.function.area) + ' ' + str(self.function)

    class Meta:
        verbose_name = _("Personnel Function Rating")
        verbose_name_plural = _("Personnel Function Ratings")

class PersonnelSubfunctionIPCR(models.Model):
    PERIODS = [
        ('Select', 'Please select period...'),
        ('Jan-Jun', 'January to June'),
        ('Jul-Dec', 'July to December'),
    ]
    personnel = models.ForeignKey(
        Personnel,
        on_delete=models.CASCADE,
        limit_choices_to=~Q(is_superuser=True) & ~Q(is_staff=True)
    )
    year = models.PositiveSmallIntegerField()
    period = models.CharField(max_length=8, choices=PERIODS, default="Select")
    subfunction = models.ForeignKey(Subfunction, on_delete=models.PROTECT)
    accomplishments = models.TextField(null=True, blank=True)
    rating_Q = models.FloatField(default=0.0, null=True, blank=True)
    rating_E = models.FloatField(default=0.0, null=True, blank=True)
    rating_T = models.FloatField(default=0.0, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.personnel)

    class Meta:
        verbose_name = _("Personnel Subfunction Rating")
        verbose_name_plural = _("Personnel Subfunction Ratings")

        