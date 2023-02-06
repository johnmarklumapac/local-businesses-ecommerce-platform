from django.shortcuts import get_object_or_404, render

from .models import Product, Rank


def product_all(request):
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)
    return render(request, "pasundayag/index.html", {"products": products})


def rank_list(request, rank_slug=None):
    rank = get_object_or_404(Rank, slug=rank_slug)
    products = Product.objects.filter(rank__in=Rank.objects.get(name=rank_slug).get_descendants(include_self=True))
    return render(request, "pasundayag/rank.html", {"rank": rank, "products": products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "pasundayag/single.html", {"product": product})
