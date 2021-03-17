from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders
from math import ceil


# Create your views here.
def index(request):
    allProds = []
    catprods = Product.objects.values('categrory', 'id')
    cats = {item['categrory'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(categrory=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'index.html', params)

def about(request):
    return render(request,'about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request,'contact.html')


def tracker (request):
    return render(request,'tracker.html')
def search (request):
    return render(request,'search.html')
def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)

    return render(request,'prodView.html', {'product':product[0]})
def checkout (request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        thank = True
        id = order.order_id
        return render(request, 'checkout.html', {'thank': thank, 'id': id})
    return render(request, 'checkout.html')
