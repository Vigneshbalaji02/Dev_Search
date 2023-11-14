from django.shortcuts import render,redirect
from .models import Profile, skill, message
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import customusercreationform, Profileform, skillform, messagefrom
from .utils import searchprofiles
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
# Create your views here.

def profiles(request):
    profiles,search_query = searchprofiles(request)

    page = request.GET.get('page')
    results = 3
    paginator= Paginator(profiles, results)

    try:
        profiles= paginator.page(page)
    except PageNotAnInteger:
        page=1
        profiles= paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles= paginator.page(page)


    context={"profiles":profiles,"search_query":search_query,"paginator":paginator}
    return render(request, "profiles.html", context)


def userProfie(request,pk):
    profile=Profile.objects.get(id=pk)

    topskills  = profile.skill_set.exclude(description__exact ="")
    otherskills = profile.skill_set.filter(description="")

    context={"profile":profile,"topskills":topskills,"otherskills":otherskills}
    return render(request, "user-profile.html",context)

def loginuser(request):
   

    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method=='POST':
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error ( request, "Username does not exist !")

        user= authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("profiles")
        else:
            messages.error ( request, "Username or Password is incorrect")
    return render(request, "login_register.html")

def registeruser(request):
    page="register"
    form=customusercreationform()

    if request.method =="POST":
        form=customusercreationform(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()

            messages.success(request, "User account created!")

            login(request, user)
            return redirect("editaccount")
        else:
            messages.success(
                request, "An error has occurred during registration"
            )

    context={"page":page, "form":form}
    return render(request, "login_register.html", context)

def logoutuser(request):
    logout(request)
    messages.success ( request, "Username was logout !")
    return redirect("login")

@login_required(login_url="login")
def useraccount(request):
    profile=request.user.profile

    skill = profile.skill_set.all()
    projects = profile.project_set.all()

    context={"profile":profile, "skill":skill, "projects":projects}
    return render(request, "account.html",context)


@login_required(login_url="login")
def editaccount(request):
    profile=request.user.profile
    form=Profileform(instance=profile)

    if request.method == "POST":
        form=Profileform(request.POST,request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("account")

    context = {"form":form}
    return render(request, "profileform.html",context)

@login_required(login_url="login")
def createskill(request):
    profile=request.user.profile
    form=skillform()

    if request.method == "POST":
        form=skillform(request.POST)
        if form.is_valid():
            skill=form.save(commit=False)
            skill.owner= profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect("account")
        
    context={"form":form}
    return render(request,"skill_template.html",context)

@login_required(login_url="login")
def updateskill(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    form=skillform (instance=skill)

    if request.method == "POST":
        form=skillform(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully!")
            return redirect("account")
        
    context={"form":form}
    return render(request,"skill_template.html",context)

def deleteskills(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        return redirect("account")
    context={'object':skill}
    return render(request,'Delete.html',context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messagesrequested=profile.messages.all()
    unreadcount = messagesrequested.filter(is_read=False).count()
    context={'messagesrequested':messagesrequested,'unreadcount':unreadcount }
    return render (request, 'inbox.html', context)


@login_required(login_url="login")
def viewmessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read  == False:
        message.is_read = True
        message.save()

    context={'message':message}
    return render(request, "message.html",context)


@login_required(login_url="login")
def createmessage(request,pk):
    recipient= Profile.objects.get(id=pk)
    form = messagefrom()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method =='POST':
        form =messagefrom(request.POST)
        message = form.save(commit=False)
        message.sender = sender
        message.recipient = recipient

        if sender:
            message.name = sender.name
            message.email = sender.email
        message.save()

        messages.success(request, "Your message was successfull sent")
        return redirect('/')

    context={'recipient':recipient, 'form':form}
    return render(request, 'message_form.html', context)

