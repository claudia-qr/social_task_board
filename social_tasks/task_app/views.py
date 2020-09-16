from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "log.html")

def tasks(request):
    if 'name' not in request.session:
        return redirect('/')
    else:
        context = {
            'all_tasks': Task.objects.all(),
        }
    return render(request, "tasks.html", context)

def register(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        print(errors)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request,values)
            return redirect('/')
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name=request.POST['first_name'], 
            last_name=request.POST['last_name'], 
            email=request.POST['email'], 
            password=pw_hash
            )
        print(new_user.password)
        request.session['name'] = new_user.first_name
        request.session['user_id'] = new_user.id
        return redirect('/tasks')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        logged_user = User.objects.filter(email=request.POST['email'])
        if len(logged_user) > 0:
            logged_user = logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['name'] = logged_user.first_name
                request.session['user_id'] = logged_user.id
                return redirect('/tasks')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def new(request):
    return render(request, 'new.html')

def create_task(request):
    errors = Task.objects.validator(request.POST)
    if len(errors):
        for (key, values) in errors.items():
            messages.error(request,values)
        return redirect('/tasks/new')
    else:
        new_task = Task.objects.create(
            title=request.POST['title'],
            points=request.POST['points'],
            description=request.POST['description'],
            creator=User.objects.get(id=request.session['user_id'])
        )
        print (new_task)
        return redirect('/tasks')
    return redirect('/')

def delete_task(request, id):
    Task.objects.get(id=id).delete()
    return redirect('/tasks')

def edit_task(request, id):
    one_task = Task.objects.get(id=id)
    context = {
        'edit_task': one_task
    }
    return render(request, 'edit_task.html', context)

def update_task(request, id):
    errors = Task.objects.validator(request.POST)
    if len(errors):
        for (key, values) in errors.items():
            messages.error(request,values)
        return redirect('/tasks/edit/')
    to_update = Task.objects.get(id=id)
    to_update.title = request.POST['title']
    to_update.points = request.POST['points']
    to_update.description = request.POST['description']
    to_update.save()
    return redirect('/tasks')

def profile(request, id):
    context = {
        'one_user': User.objects.get(id=id)
    }
    return render(request, 'profile.html', context)

def account(request, id):
    context = {
        'one_user': User.objects.get(id=id)
    }
    return render(request, 'account.html', context)

def update_account(request, id):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for (key, values) in errors.items():
            messages.error(request,values)
        return redirect('/account')
    profile_update = User.objects.get(id=id)
    profile_update.first_name = request.POST['first_name']
    profile_update.last_name = request.POST['last_name']
    profile_update.email = request.POST['email']
    profile_update.password = request.POST['password']
    return redirect('/account')

def add_like(request, id):
    liked_task = Task.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_task.likes.add(user_liking)
    return redirect('/tasks')

def complete_task(request, id):
    liked_task = Task.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_task.completed_by.add(user_liking)
    return redirect('/tasks')

def add_comment(request, id):
    creator = User.objects.get(id=request.session['user_id'])
    task = Task.objects.get(id=id)
    #create the comment
    Comment.objects.create(
        content = request.POST['content'], 
        creator = creator, 
        task = task)
    return redirect('/tasks')


def edit_comm(request, id):
    one_comm = Comment.objects.get(id=id)
    if request.method == 'POST':
        one_comm.content = request.POST['content']
        one_comm.save()
        return redirect(f'/tasks/{str(one_comm.creator.id)}')
    context = {
        'comm': Comment.objects.get(id=id)
    }
    return render(request, 'edit_comm.html', context)

def delete_comm(request, id):
    Comment.objects.get(id=id).delete()
    return redirect('/tasks')

