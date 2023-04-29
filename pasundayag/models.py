from decimal import Decimal
from django.db.models import Sum
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import ModelChoiceField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from account.models import Personnel
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    PERIODS = [
        ("Select", "Please select period..."),
        ("Jan-Jun", "January to June"),
        ("Jul-Dec", "July to December"),
    ]
    personnel = models.ForeignKey(
        Personnel,
        on_delete=models.PROTECT,
        limit_choices_to=~Q(is_superuser=True) & ~Q(is_staff=True),
    )
    year = models.PositiveSmallIntegerField()
    period = models.CharField(max_length=8, choices=PERIODS, default="Select")
    rank = models.CharField(max_length=255)
    ipcr_type = models.ForeignKey(IPCRType, on_delete=models.PROTECT, verbose_name=_("IPCR Type"))
    is_active = models.BooleanField(
        verbose_name=_("IPCR visibility"),
        help_text=_("Change IPCR visibility"),
        default=True,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False, blank=True, null=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True, blank=True, null=True)

    stra_e1 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    stra_e2 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    stra_e3 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    stra_a1 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    stra_a2 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    stra_a3 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    stra_total = models.DecimalField(blank=True, max_digits=5, decimal_places=2, default=0.0000)
    stra_adjectival_rating = models.CharField(
        verbose_name=_("Strategic Functions Adjectival Rating"), blank=True, max_length=255, default="Poor"
    )
    core_q1 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_q2 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_q3 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_q4 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e1 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e2 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e3 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e4 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e5 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e6 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e7 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e8 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e9 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e10 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e11 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e12 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e13 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e14 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_e15 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_t1 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a1 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a2 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a3 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a4 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a5 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a6 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_acad_total = models.DecimalField(blank=True, max_digits=5, decimal_places=2, default=0.0000)
    core_acad_adjectival_rating = models.CharField(
        verbose_name=_("Core Functions - Academic Adjectival Rating"), blank=True, max_length=255, default="Poor"
    )
    core_a7 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a8 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a9 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a10 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a11 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a12 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_prod_total = models.DecimalField(blank=True, max_digits=5, decimal_places=2, default=0.0000)
    core_prod_adjectival_rating = models.CharField(
        verbose_name=_("Core Functions - Improving Research Productivity Adjectival Rating"),
        blank=True,
        max_length=255,
        default="Poor",
    )
    core_a13 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a14 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a15 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a16 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a17 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a18 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_a19 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    core_tech_total = models.DecimalField(blank=True, max_digits=5, decimal_places=2, default=0.0000)
    core_tech_adjectival_rating = models.CharField(
        verbose_name=_("Core Functions - Technical Advisory/Extension Adjectival RAting"),
        blank=True,
        max_length=255,
        default="Poor",
    )
    supp_e1 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    supp_e2 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    supp_e3 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    supp_e4 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    supp_e5 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    supp_t1 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    supp_a1 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    supp_a2 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    supp_a3 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    supp_a4 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    supp_a5 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    supp_a6 = models.DecimalField(max_digits=5, decimal_places=2, default=0.0000)
    supp_total = models.DecimalField(blank=True, max_digits=5, decimal_places=2, default=0.0000)
    supp_adjectival_rating = models.CharField(
        verbose_name=_("Support Function Adjectival Rating"), blank=True, max_length=255, default="Poor"
    )
    final_numerical_rating = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, default=0.0000)
    final_adjectival_rating = models.CharField(
        verbose_name=_("Final Adjectival Rating"), blank=True, max_length=255, default="Poor"
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("IPCR")
        verbose_name_plural = _("IPCRs")

    def get_absolute_url(self):
        return reverse("pasundayag:ipcr_detail", args=[self.slug])


    def calculate_stra_total(self):
        stra_total = self.stra_a1 + self.stra_a2 + self.stra_a3
        stra_total = stra_total / 3
        stra_percent = ((((stra_total) / (3 * 5)) * 100) / 100) * 30
        stra_percent = (stra_total / 3) * Decimal(0.30)
        self.stra_percent = round(stra_percent, 2)
        self.stra_total = round(stra_total, 2)
        self.save()

    def calculate_core_acad_total(self):
        core_acad_total = (
            self.core_a1 * Decimal(0.05)
            + self.core_a2 * Decimal(0.15)
            + self.core_a3 * Decimal(0.15)
            + self.core_a4 * Decimal(0.15)
            + self.core_a5 * Decimal(0.35)
            + self.core_a6 * Decimal(0.15)
        )
        self.core_acad_total = round(core_acad_total, 2)
        self.save()

    def calculate_core_prod_total(self):
        core_prod_total = (
            self.core_a7 * Decimal(0.01)
            + self.core_a8 * Decimal(0.5)
            + self.core_a9 * Decimal(0.01)
            + self.core_a10 * Decimal(0.02)
            + self.core_a11 * Decimal(0.5)
            + self.core_a12 * Decimal(0.01)
        )
        self.core_prod_total = round(core_prod_total, 2)
        self.save()

    def calculate_core_tech_total(self):
        core_tech_total = (
            self.core_a13 * Decimal(0.2)
            + self.core_a14 * Decimal(0.2)
            + self.core_a15 * Decimal(0.2)
            + self.core_a16 * Decimal(0.2)
            + self.core_a17 * Decimal(0.2)
            + self.core_a18 * Decimal(0.05)
            + self.core_a19 * Decimal(0.05)
        )
        self.core_tech_total = round(core_tech_total, 2)
        self.save()

    def calculate_supp_total(self):
        supp_total = (self.supp_a1 + self.supp_a2 + self.supp_a3 + self.supp_a4 + self.supp_a5 + self.supp_a6) / 6
        supp_percent = ((((supp_total) / (6 * 5)) * 100) / 100) * 10
        supp_percent = (supp_total / 6) * Decimal(0.30)
        self.supp_percent = round(supp_percent, 2)
        self.supp_total = round(supp_total, 2)
        self.save()

    def calculate_final_numerical_rating(self):
        final_numerical_rating = (
            self.stra_total + self.core_acad_total + self.core_prod_total + self.core_tech_total + self.supp_total
        )
        final_numerical_percent = ((((final_numerical_rating) / (5 * 5)) * 100) / 100) * 100
        final_numerical_rating = final_numerical_rating / 5
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
            self.stra_adjectival_rating = "Poor"
        super().save(*args, **kwargs)

    def core_acad_save(self, *args, **kwargs):
        if self.core_acad_total >= 5:
            self.core_acad_adjectival_rating = "Outstanding"
        elif self.core_acad_total >= 4:
            self.core_acad_adjectival_rating = "Very Satisfactory"
        elif self.core_acad_total >= 3:
            self.core_acad_adjectival_rating = "Satisfactory"
        elif self.core_acad_total >= 2:
            self.core_acad_adjectival_rating = "Unsatisfactory"
        else:
            self.core_acad_adjectival_rating = "Poor"
        super().save(*args, **kwargs)

    def core_prod_save(self, *args, **kwargs):
        if self.core_prod_total >= 5:
            self.core_prod_adjectival_rating = "Outstanding"
        elif self.core_prod_total >= 4:
            self.core_prod_adjectival_rating = "Very Satisfactory"
        elif self.core_prod_total >= 3:
            self.core_prod_adjectival_rating = "Satisfactory"
        elif self.core_prod_total >= 2:
            self.core_prod_adjectival_rating = "Unsatisfactory"
        else:
            self.core_prod_adjectival_rating = "Poor"
        super().save(*args, **kwargs)

    def core_tech_save(self, *args, **kwargs):
        if self.core_tech_total >= 5:
            self.core_tech_adjectival_rating = "Outstanding"
        elif self.core_tech_total >= 4:
            self.core_tech_adjectival_rating = "Very Satisfactory"
        elif self.core_tech_total >= 3:
            self.core_tech_adjectival_rating = "Satisfactory"
        elif self.core_tech_total >= 2:
            self.core_tech_adjectival_rating = "Unsatisfactory"
        else:
            self.core_tech_adjectival_rating = "Poor"
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
            self.core_adjectival_rating = "Poor"
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
            self.final_adjectival_rating = "Poor"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.personnel.name + "-" + str(self.year) + "-" + self.period + "(" + str(self.final_numerical_rating) + ") "
   
class AnnualIPCR(models.Model):
    personnel = models.ForeignKey(
        Personnel,
        on_delete=models.PROTECT,
        limit_choices_to=~Q(is_superuser=True) & ~Q(is_staff=True),
    )
    year = models.PositiveSmallIntegerField()
    jan_jun_final_rating = models.ForeignKey(
        IPCR,
        blank=True,
        null = True,
        on_delete=models.PROTECT,
        limit_choices_to=Q(period='Jan-Jun'),
        related_name = "jan_jun_rating"
    )
    jul_dec_final_rating = models.ForeignKey(
        IPCR,
        blank=True,
        null = True,
        on_delete=models.PROTECT,
        limit_choices_to=Q(period='Jul-Dec'),
        related_name = "jul_dec_rating"

    )
    rank = models.CharField(max_length=255)
    annual_numerical_rating = models.DecimalField(blank=True, max_digits=5, decimal_places=2, default=0.0000)
    annual_adjectival_rating = models.CharField(
        verbose_name=_("Annual Adjectival Rating"), blank=True, max_length=255, default="Poor"
    )

    class Meta:
        verbose_name = _("Annual IPCR")
        verbose_name_plural = _("Annual IPCRs")

    def __str__(self):
        return self.personnel.name + " (" + str(self.year) + ")"

    def calculate_annual_numerical_rating(self):
        if self.jan_jun_final_rating and self.jul_dec_final_rating:
            total_rating = (self.jan_jun_final_rating.final_numerical_rating + self.jul_dec_final_rating.final_numerical_rating) / 2
            self.annual_numerical_rating = round(total_rating, 2)
            self.save()
        elif self.jan_jun_final_rating:
            total_rating = (self.jan_jun_final_rating.final_numerical_rating) / 1
            self.annual_numerical_rating = round(total_rating, 2)
            self.save()
        elif self.jul_dec_final_rating:
            total_rating = (self.jul_dec_final_rating.final_numerical_rating) / 1
            self.annual_numerical_rating = round(total_rating, 2)
            self.save()

    def save(self, *args, **kwargs):
        if self.annual_numerical_rating >= 5:
            self.annual_adjectival_rating = "Outstanding"
        elif self.annual_numerical_rating >= 4:
            self.annual_adjectival_rating = "Very Satisfactory"
        elif self.annual_numerical_rating >= 3:
            self.annual_adjectival_rating = "Satisfactory"
        elif self.annual_numerical_rating >= 2:
            self.annual_adjectival_rating = "Unsatisfactory"
        else:
            self.annual_adjectival_rating = "Poor"
        super().save(*args, **kwargs)
        
@receiver(post_save, sender=IPCR)
def create_or_update_annual_ipcr(sender, instance, created, **kwargs):
    
    if created:  # If a new IPCR instance is created
        # Create an instance of AnnualIPCR for Jan-Jun period
        try:
            annual_ipcr = AnnualIPCR.objects.get(personnel=instance.personnel, year=instance.year)
        except AnnualIPCR.DoesNotExist:
            # If an instance does not exist, create a new one
            annual_ipcr = AnnualIPCR.objects.create(
                personnel=instance.personnel,
                year=instance.year,
                jan_jun_final_rating=instance,
                rank=instance.rank
            )
            annual_ipcr.save()
        else:
            # If an instance exists, update its fields with the values from the new IPCR instance
            annual_ipcr.jan_jun_final_rating = instance
            annual_ipcr.rank=instance.rank
            annual_ipcr.save()
    else:  # If an existing IPCR instance is updated
        # Check if the IPCR instance is for Jul-Dec period and if it has a final numerical rating
        if instance.period == 'Jul-Dec' and instance.final_numerical_rating:
            # Update the corresponding AnnualIPCR instance with the Jul-Dec final rating
            try:
                annual_ipcr = AnnualIPCR.objects.get(personnel=instance.personnel, year=instance.year)
                annual_ipcr.jul_dec_final_rating = instance
                annual_ipcr.save()
            except AnnualIPCR.DoesNotExist:
                annual_ipcr=None

@receiver(post_save, sender=IPCR)
def save_annual_ipcr(sender, instance, **kwargs):
    print(instance)
    try: 
        annual_ipcr = AnnualIPCR.objects.get(personnel=instance.personnel, year=instance.year)
            
    except Exception as e:
        AnnualIPCR.objects.create(
            personnel=instance.personnel,
            year=instance.year,
            jan_jun_final_rating=instance,
            rank=instance.rank)
        instance.personnel.save()

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


class Area(models.Model):
    rank = models.ManyToManyField(Rank)
    description = models.CharField(max_length=255)
    percent = models.DecimalField(decimal_places=2, max_digits=50)

    def __str__(self):
        rank_names = [rank.name for rank in self.rank.all()[:3]]
        if self.rank.count() > 3:
            rank_names.append("...")
        rank_list = ", ".join(rank_names)
        return str(self.description) + " - " + f"{rank_list} - {self.description}"

    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")
        ordering = ["description"]


class Function(models.Model):
    PERIODS = [
        ("Select", "Please select period..."),
        ("Jan-Jun", "January to June"),
        ("Jul-Dec", "July to December"),
    ]
    period = models.CharField(max_length=8, choices=PERIODS, default="Select")
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    mfo_pap = models.TextField(verbose_name=_("MFO/PAP"), null=True, blank=True)
    indicators = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.mfo_pap) + " - " + str(self.area)

    class Meta:
        verbose_name = _("Function")
        verbose_name_plural = _("Functions")
        ordering = ["mfo_pap"]


class Subfunction(models.Model):
    PERIODS = [
        ("Select", "Please select period..."),
        ("Jan-Jun", "January to June"),
        ("Jul-Dec", "July to December"),
    ]
    period = models.CharField(max_length=8, choices=PERIODS, default="Select")
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
        ("Select", "Please select period..."),
        ("Jan-Jun", "January to June"),
        ("Jul-Dec", "July to December"),
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
        return str(self.personnel) + " " + str(self.function.area) + " " + str(self.function)

    class Meta:
        verbose_name = _("Personnel Function Rating")
        verbose_name_plural = _("Personnel Function Ratings")

    def rating_average(self):
        ratings = [self.rating_Q, self.rating_E, self.rating_T]
        valid_ratings = [r for r in ratings if r is not None]
        if valid_ratings:
            return sum(valid_ratings) / len(valid_ratings)
        else:
            return None


class PersonnelSubfunctionIPCR(models.Model):
    PERIODS = [
        ("Select", "Please select period..."),
        ("Jan-Jun", "January to June"),
        ("Jul-Dec", "July to December"),
    ]
    personnel = models.ForeignKey(
        Personnel, on_delete=models.CASCADE, limit_choices_to=~Q(is_superuser=True) & ~Q(is_staff=True)
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
