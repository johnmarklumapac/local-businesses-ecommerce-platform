from django.shortcuts import get_object_or_404, render


def pasundayag_home(request):
    return render(request, "pasundayag/pasundayag_home.html")
