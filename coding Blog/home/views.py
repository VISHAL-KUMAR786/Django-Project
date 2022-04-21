from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from Blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

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