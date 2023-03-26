from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import PersonnelFunctionIPCR, PersonnelSubfunctionIPCR

@receiver(post_save, sender=PersonnelFunctionIPCR)
def create_subfunction_ratings(sender, instance, created, **kwargs):
    if created:
        # Get all related subfunctions
        subfunctions = instance.function.subfunction_set.all()
        # Create PersonnelSubfunctionIPCR objects for each subfunction
        for subfunction in subfunctions:
            subfunction_rating = PersonnelSubfunctionIPCR.objects.create(
                personnel=instance.personnel,
                year=instance.year,
                period=instance.period,
                subfunction=subfunction,
                accomplishments=instance.accomplishments,
                rating_Q=instance.rating_Q,
                rating_E=instance.rating_E,
                rating_T=instance.rating_T,
                remarks=instance.remarks
            )
