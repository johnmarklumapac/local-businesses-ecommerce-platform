from django.shortcuts import get_object_or_404, render


def pasundayag(request):
    return render(request, "pasundayag/index_pasundayag.html")