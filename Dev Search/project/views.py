from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Project, Review, Tag
from .forms import ProjectForm, ReviewForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import searchProject, paginateProject

# REST API DJANGO RESPONSE MIMIC


def index(request):
    projectsList, search_query = searchProject(request)
    paginator, custom_range, projectsList = paginateProject(request,projectsList,12)
    
    content = {'projectsList': projectsList,'search_query':search_query,'paginator':paginator,'custom_range':custom_range}
    return render(request, 'project/index.html', content)


def about(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    form = ReviewForm()

    if request.method == 'POST':
        try:
            form = ReviewForm(request.POST)
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()

            projectObj.getVoteCount

            messages.success(request,'your comment have been posted')
            return redirect('project:About',pk=projectObj.id)
        except Exception as e:
            messages.error(request,'some error occur')
            pass 

    content = {'project': projectObj, 'tags': tags,'form':form}
    return render(request, 'project/about.html', content)


@login_required(login_url='user:login')
def createProject(request):
    profile = request.user.profile
    forms = ProjectForm()

    if request.method == 'POST':
        newTag = request.POST.get('newTag').strip().replace(',',' ').replace('\n',' ').split()
        forms = ProjectForm(request.POST, request.FILES)
        if forms.is_valid:
            project = forms.save(commit=False)
            for tag in newTag:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.all()
            project.owner = profile
            project.save()
            return redirect('user:account')

    content = {'forms': forms}
    return render(request, 'project/project_form.html', content)


@login_required(login_url='user:login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    forms = ProjectForm(instance=project)

    if request.method == 'POST':
        newTag = request.POST.get('newTag').strip().replace(',',' ').replace('\n',' ').split()
        forms = ProjectForm(request.POST, request.FILES, instance=project)
        if forms.is_valid:
            project =  forms.save()
            for tag in newTag:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.all()
            return redirect('user:account')

    content = {'forms': forms,'project':project}
    return render(request, 'project/project_form.html', content)


@login_required(login_url='user:login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('user:account')

    content = {'project': project}
    return render(request, 'project/delete.html', content)

