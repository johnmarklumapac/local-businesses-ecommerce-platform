from django.shortcuts import get_object_or_404, render

from .models import IPCR, Rank


def ipcr_all(request):
    ipcrs = IPCR.objects.prefetch_related("ipcr_image").filter(is_active=True)
    return render(request, "pasundayag/index.html", {"ipcrs": ipcrs})


def rank_list(request, rank_slug=None):
    rank = get_object_or_404(Rank, slug=rank_slug)
    ipcrs = IPCR.objects.filter(rank__in=Rank.objects.get(name=rank_slug).get_descendants(include_self=True))
    return render(request, "pasundayag/rank.html", {"rank": rank, "ipcrs": ipcrs})


def ipcr_detail(request, slug):
    ipcr = get_object_or_404(IPCR, slug=slug, is_active=True)
    ipcr.calculate_stra_total()
    ipcr.calculate_core_total()
    ipcr.calculate_supp_total()
    ipcr.calculate_final_numerical_rating()
    ipcr.stra_save()
    ipcr.core_save()
    ipcr.supp_save()
    return render(request, "pasundayag/single.html", {"ipcr": ipcr})
