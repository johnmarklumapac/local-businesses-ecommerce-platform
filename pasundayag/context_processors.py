from .models import Rank


def categories(request):
    return {"categories": Rank.objects.filter(level=0)}
