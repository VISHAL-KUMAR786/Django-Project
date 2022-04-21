from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.contrib import messages
from .models import Post ,BlogComment
from django.core.paginator import Paginator

# Create your views here.


def home(request):
    posts = Post.objects.all()
    book_paginator = Paginator(posts,4)
    page_num = request.GET['page']
    page = book_paginator.get_page(page_num)

    posts = page 

    content = {'posts': posts, 'count':book_paginator.count}
    return render(request, 'Blog/index.html', content)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.view += 1
    post.save()

    comments = BlogComment.objects.filter(post=post,parent=None)
    
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}

    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    content = {'post': post,'comments':comments,'replyDict':replyDict}
    return render(request, 'Blog/blogpost.html', content)


def postComment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        # comment = request.POST.get('comment')

        if comment == '':
            messages.add_message(request,messages.WARNING,"Do'nt leave the comment empty")
            return redirect(f'/blog')

        user = request.user
        postSno = request.POST['postId']
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST['parent']

        if parentSno == "":
            blogcomment = BlogComment(comment=comment,user=user,post=post)
            blogcomment.save()

            messages.add_message(request,messages.SUCCESS,"your comment have been posted")
            return redirect(f'/blog/{post.slug}')
        
        else:
            parent = BlogComment.objects.get(sno = parentSno)
            blogcomment = BlogComment(comment=comment,user=user,post=post,parent=parent)
            blogcomment.save()  

            messages.add_message(request,messages.SUCCESS,"your comment have been posted")
            return redirect(f'/blog/{post.slug}')
        

    return render(request, 'blogHome')
