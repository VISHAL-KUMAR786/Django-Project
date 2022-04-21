from math import ceil
from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Contact, Order, OrderUpdate
import json
# Create your views here.


def index(request):
    products = Product.objects.all()
    n = len(products)
    nSlides = n//4 + ceil((n/4) - (n//4))

    category = Product.objects.values('category', 'product_id')
    cats = {items['category'] for items in category}
    allProd = []
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = round(n//4 + ceil((n/4) - (n//4)))
        allProd.append([prod, range(1, nSlides), nSlides])
    params = {'allProd': allProd}
    return render(request, 'shop/index.html', params)


def searchMatch(query, item):

    if query in item.product_name or query in item.desc or query in item.category:
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search', '')
    products = Product.objects.all()
    n = len(products)
    nSlides = n//4 + ceil((n/4) - (n//4))

    category = Product.objects.values('category', 'product_id')
    cats = {items['category'] for items in category}
    allProd = []
    for cat in cats:
        producttemp = Product.objects.filter(category=cat)
        prod = [item for item in producttemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = round(n//4 + ceil((n/4) - (n//4)))
        if len(prod) != 0:
            allProd.append([prod, range(1, nSlides), nSlides])
    params = {'allProd': allProd, 'msg': ""}
    if len(allProd) == 0 or len(query) < 2:
        params = {"msg": "Please Enter some releavent Query"}
    print(params)
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        a = Contact(name=name, email=email, phone=phone, desc=desc)
        a.save()
        h5 = f'Thank {name} for Contacting us 😍🥰😭'
        p = 'you response will be responded soon ⌚⌛'
        button = 'Go to Home'
        params = {'h5': h5, 'p': p, 'button': button, 'name': name}
        return render(request, 'shop/thank.html', params)

    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == 'POST':
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)

            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    # Exception as Object of type date is not JSON serializable
                    response = json.dumps({"status":"success","updates":updates,"item_json":order[0].item_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"No Item"}')

        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')


def product(request, id):
    product = Product.objects.filter(product_id=id)  # return a quesryset
    params = {'product': product[0]}
    return render(request, 'shop/product.html', params)


def checkout(request):
    if request.method == 'POST':
        item_json = request.POST.get('item_json', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address1 = request.POST.get(
            'address1', '') + ' 2️⃣  ' + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip = request.POST.get('zip', '')
        phone = request.POST.get('phone', '')

        order = Order(item_json=item_json, name=name, email=email,
                      address1=address1, city=city, state=state, zip=zip, phone=phone, amount=amount)
        order.save()

        update_desc = "The order has been placed ."
        update = OrderUpdate(order_id=order.order_id, update_desc=update_desc)
        update.save()

        h5 = f'Thank {name} for Placing order . Your Tracker or Refrence id is {order.order_id} 🥰'
        p = 'you response will be responded soon ⌚⌛'
        button = 'Go to Home'
        h5_1 = f'Use Tracker Id ({order.order_id}) for Tracking Location of Your Product'
        thank = True
        params = {'h5': h5, 'p': p, 'button': button,
                  'name': name, 'h5_1': h5_1, 'thank': thank}
        return render(request, 'shop/thank.html', params)

    return render(request, 'shop/checkout.html')


def thank(request):
    h5 = 'Thank someone for Contacting us 😍🥰😭'
    p = 'you response will be responded soon ⌚⌛'
    button = 'Go to Home'
    return render(request, 'shop/thank.html', {'h5': h5, 'p': p, 'button': button})
