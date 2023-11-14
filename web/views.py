from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project,Tag
from .forms import ProjectForm, Reviewform
from django.contrib.auth.decorators import login_required
from.utils import searchproject
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
# Create your views here.


def projects(request):
    projects,search_query = searchproject(request)

    page = request.GET.get('page')
    results = 6
    paginator= Paginator(projects, results)

    try:
        projects= paginator.page(page)
    except PageNotAnInteger:
        page=1
        projects= paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects= paginator.page(page)
    
    context={"projects":projects,"search_query":search_query, "paginator":paginator}
    return render(request, "products.html",context)


def project(request, pk):
    projectObj= Project.objects.get(id=pk)
    form=Reviewform()

    if request.method=="POST":
        form = Reviewform(request.POST)
        review=form.save(commit=False)
        review.project = projectObj
        review.owner=request.user.profile
        review.save()

        projectObj.votes
        
        messages.success(request, "Your message was successfully submitted")
        return redirect('project',pk=projectObj.id)
    
    return render(request, "singleproject.html",{"project":projectObj,"form":form})

@login_required(login_url="login")
def createproject(request):
    profile=request.user.profile
    form=ProjectForm()

    if request.method=="POST":
        form=ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("account")
            
        
    context={"form":form}
    return render(request, "forms.html",context)


@login_required(login_url="login")
def updateProject(request,pk):
    profile = request.user.profile
    project=profile.project_set.get(id=pk)
    form=ProjectForm(instance=project)

    if request.method=="POST":
        newtags = request.POST.get('newtags').replace(',', " ").split()

        form=ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project= form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect("account")
        
    context={"form":form}
    return render(request, "forms.html",context)


@login_required(login_url="login")
def deleteProject(request,pk):
    profile = request.user.profile
    project=profile.project_set.get(id=pk)
    if request.method =="POST":
        project.delete()
        return redirect("account")
    
    context={"object":project}
    return render(request,"Delete.html",context)