from .models import Rank


def ranks(request):
    return {"ranks": Rank.objects.filter(level=0)}
