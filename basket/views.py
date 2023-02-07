from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from pasundayag.models import IPCR

from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    return render(request, "basket/summary.html", {"basket": basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        ipcr_id = int(request.POST.get("ipcrid"))
        ipcr_qty = int(request.POST.get("ipcrqty"))
        ipcr = get_object_or_404(IPCR, id=ipcr_id)
        basket.add(ipcr=ipcr, qty=ipcr_qty)

        basketqty = basket.__len__()
        response = JsonResponse({"qty": basketqty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        ipcr_id = int(request.POST.get("ipcrid"))
        basket.delete(ipcr=ipcr_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({"qty": basketqty, "subtotal": baskettotal})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        ipcr_id = int(request.POST.get("ipcrid"))
        ipcr_qty = int(request.POST.get("ipcrqty"))
        basket.update(ipcr=ipcr_id, qty=ipcr_qty)

        basketqty = basket.__len__()
        basketsubtotal = basket.get_subtotal_price()
        response = JsonResponse({"qty": basketqty, "subtotal": basketsubtotal})
        return response
