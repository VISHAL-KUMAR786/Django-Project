from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Contact ,CA
from django.contrib import messages
from Blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import xlwt
import datetime


# HTML pages

def home(request):
    popular3Posts = Post.objects.all().order_by("-view")[:4]
    content = {'posts':popular3Posts}

    return render(request, 'home/index.html',content)


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    if request.method == 'POST':
        # name = request.POST.get('name','')
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']

        # more auth is required
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(desc) < 4:
            messages.add_message(request, messages.ERROR,
                                 'Please enter a valid value in contact form')
            return redirect('home')
        else:
            messages.add_message(
                request, messages.SUCCESS, f'Thank {name} for Contact Us . Your Response has Been Recorded 🥰')
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
    else:
        messages.add_message(request, messages.INFO,
                             'Please fill Contact form')

    return render(request, 'home/contact.html')
    return HttpResponse('404 Error page not found')


def search(request):
    query = request.GET['query']
    if len(query) > 70:
        post = Post.objects.none()
    else:
        post1 = Post.objects.filter(title__icontains=query)
        post2 = Post.objects.filter(author__icontains=query)
        post3 = Post.objects.filter(slug__icontains=query)
        post4 = Post.objects.filter(content__icontains=query)
        post = post1.union(post2, post3, post4)
    if post.count() == 0:
        messages.add_message(
            request, messages.ERROR, f'No search result are found . Please refine your query 😭')
    content = {'posts': post, 'Query': query}
    return render(request, 'home/search.html', content)


# Authentication API's


def handlesignup(request):
    if request.method == 'POST':
        # getting the value from form
        userName = request.POST['userName']
        fname = request.POST['fname']
        lname = request.POST['lname']
        emailSign = request.POST['emailSign']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # checking the value are not empty

        # username must be under 10 char
        if len(userName) > 10:
            messages.add_message(
                request, messages.ERROR, 'Username must be under 10 character')
            return render(request, 'home/signUp.html')

        # username must contain only character and number
        if not userName.isalnum():
            messages.add_message(
                request, messages.ERROR, 'Username contain only character & numbers')
            return render(request, 'home/signUp.html')

        # password must be same
        if password1 != password2:
            messages.add_message(
                request, messages.ERROR, "Password don't match")
            return render(request, 'home/signUp.html')

        # saving into user model from django.contrib.auth.models import User
        user = User.objects.create_user(userName, emailSign, password1)
        user.first_name = fname
        user.last_name = lname
        user.save()
        messages.add_message(
            request, messages.SUCCESS, "You account has been created in codingSolution")
        return redirect('home')
    else:
        messages.add_message(request, messages.INFO,
                             'Please fill sign up form')
        return render(request, 'home/signUp.html')

    return HttpResponse('404 Error page not found')


def handlelogin(request):
    if request.method == 'POST':
        userName = request.POST['userName']
        password = request.POST['password']

        user = authenticate(request, username=userName, password=password)

        if user is not None:
            login(request, user)
            messages.add_message(
                request, messages.SUCCESS, 'Login Successfully')
            return redirect('home')
        else:
            messages.add_message(
                request, messages.ERROR, 'Invalid credentials! Please try again')
            return redirect('home')
    else:
        messages.add_message(request, messages.INFO, 'Please fill login form')
        return render(request, 'home/login.html')

    return HttpResponse('404 Error page not found')


def handlelogout(request):
    logout(request)
    messages.add_message(
        request, messages.SUCCESS, 'Logout Successfully')
    return redirect('home')

# by user.objects.create() -> password is unhashable



# Excel data

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Posts Data')  # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['panNo', 'name', 'phone', 'completed','timeStamp','unit','email','Password']

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = CA.objects.all().values_list(
        'panNo', 'name', 'phone', 'completed','timeStamp','unit','email','Password')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

def CAccountant(request):
    if request.method == 'POST':
        panNo = request.POST['panNo']
        name = request.POST['name']
        phone = request.POST['phone']
        compl = request.POST.get('completed',False)
        timeStamp = request.POST['dobUk']
        unit = request.POST['unit']
        email = request.POST['email']
        Password = request.POST['Password']

        if compl == 'on':
            completed = True 
        else :
            completed = False

        timeStamp = datetime.datetime.strptime(timeStamp, "%Y-%m-%d").strftime("%d/%m/%Y")
        ca = CA(panNo=panNo,name=name,phone=phone,completed=completed,timeStamp=timeStamp,unit=unit,email=email,Password=Password)
        ca.save()
        messages.add_message(request,messages.SUCCESS,'thank for submiting the form')


    return render(request,'home/ca.html')

def CAView(request):
    clients = CA.objects.all()
    params = {'clients':clients}
    return render(request,'home/caView.html',params)

def CASearch(request):
    query = request.GET['query']
    

    find1 = CA.objects.filter(panNo__icontains=query)
    find2 = CA.objects.filter(name__icontains=query)
    find3 = CA.objects.filter(phone__icontains=query)
    # find5 = CA.objects.filter(dobUk__icontains=query)
    find6 = CA.objects.filter(unit__icontains=query)
    find7 = CA.objects.filter(email__icontains=query)
    find8 = CA.objects.filter(Password__icontains=query)
    find9 = CA.objects.filter(panNo__icontains=query)
    find10 = CA.objects.filter(panNo__icontains=query)

    if query == 'True' or query == 'False':
        find4 = CA.objects.filter(completed=query)
        find1 = find1.union(find1, find2, find3,find4,find6,find7,find8,find9,find10)
    else:
        pass 
        find1 = find1.union(find1, find2, find3,find6,find7,find8,find9,find10)

    if find1.count() == 0:
        messages.add_message(
            request, messages.ERROR, f'No search result are found . Please refine your query 😭')

    print(find1)
    content = {'clients': find1}
    return render(request,'home/caView.html',content)