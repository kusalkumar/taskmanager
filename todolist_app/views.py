from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from todolist_app.models import TaskList
from todolist_app.forms import TaskForm


# Create your views here.

def index(request):
    context = {
            'index_text': 'welcome to index page'
            }
    return render(request, 'index.html', context)

@login_required
def todolist(request):
    print(request.method)
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        print(form.is_valid())
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manager = request.user
            instance.save()
        #messages.success(request, 'New task added')
        messages.add_message(
                request,
                messages.SUCCESS,
                'The task added successfully'
                )
        return redirect('todolist')

    else:
        all_tasks = TaskList.objects.filter(manager=request.user)
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)
        return render(request, 'todolist.html', {'all_tasks':all_tasks})


@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
            messages.add_message(
                    request,
                    messages.SUCCESS,
                    'The task added successfully'
                    )
        return redirect('todolist')
    else:
        task = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {'task':task})

@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if request.user == task.manager:
        task.done = True
        task.save()
        msg = task.task + " marked as completed"
        messages.add_message(
                request,
                messages.SUCCESS,
                msg,
                )
    else:
        msg = "You don't have a access to delete the task"
        messages.add_message(
                request,
                messages.error,
                msg
                )

    return redirect('todolist')

@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if request.user == task.manager:
        task.done = False
        task.save()
        msg = task.task + " marked as pending"
        messages.add_message(
                request,
                messages.SUCCESS,
                msg,
                )
    else:
        msg = "You don't have a access to perfomrm this action"
        messages.add_message(
                request,
                messages.error,
                msg
                )
    return redirect('todolist')


@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manager == request.user:
        task_name = task.task
        task.delete()
        msg = "Task : " + task_name + " deleted successfully"
        messages.add_message(
                request,
                messages.SUCCESS,
                msg
                )
    else:
        msg = "You don't have a access to perform the action"
        messages.add_message(
                request,
                messages.SUCCESS,
                msg
                )
    return redirect('todolist')

@login_required
def contact(request):
    context = {
            'contact_text': 'welcome to contact page'
            }
    print("----------")
    return render(request, 'contact.html', context)

@login_required
def about(request):
    context = {
            'about_text': 'welcome to about page'
            }
    return render(request, 'about.html', context)
