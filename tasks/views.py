from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

# UserCreationForm: Formulario para registro de usuarios
# AuthenticationForm: Formulario para comprobar si el usuario existe(login)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Modelo para registro de usuarios
from django.contrib.auth.models import User

# login: Iniciar sesion de un usuario
# logout: Quitar seseion de un usuario
# authenticate: Autenticar un usario
from django.contrib.auth import login, logout, authenticate

# Error dado por el navegador cuando el usuario ya existe
from django.db import IntegrityError

from .forms import Task_Form
from .models import Task

from django.utils import timezone

# Restringir el acceso a las vistas que necesitan usuario logeado, y redirigir al login (Esto se hace en settings)
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request: HttpResponse):
    return render(request, "home.html")


def signup(request: HttpResponse):
    # si llega por el metodo GET significa que esta intentando ver la interfaz
    if request.method == "GET":
        # This is with our own form created manually
        return render(request, "signup.html")
        # This is with the form provided by django
        # return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # Register user
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()

                # Standar way to handle user authentication
                login(request, user)

                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {
                        # "form": UserCreationForm,
                        "error": "User already exists"
                    },
                )

        return render(
            request,
            "signup.html",
            {
                # "form": UserCreationForm,
                "error": "Password do not match"
            },
        )


@login_required
def tasks(request: HttpResponse):
    # Filtrando las tareas por las del usuario actual, y mostrando solo las que no han sido completadas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "tasks.html", {"tasks": tasks, "title": "Task Pending"})


@login_required
def signout(request: HttpResponse):
    logout(request)
    return redirect("home")


def signin(request: HttpResponse):
    if request.method == "GET":
        # This is with our own form created manual
        return render(request, "signin.html")

        # This is with the form provided by django
        # return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    # "form": AuthenticationForm,
                    "error": "Username or password is incorrect",
                },
            )
        else:
            login(request, user)
            return redirect("tasks")


@login_required
def create_Task(request: HttpResponse):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": Task_Form})
    else:
        try:
            # Pasando a Task_Form los datos, y esto los convierte en un form. Toma los datos enviados
            # por el usuario y los valida con los campos del formulario.
            form = Task_Form(request.POST)

            # Crea un objeto 'new_Task', pero commit=False evita guardarlo en la base de datos
            # inmediatamente. Esto permite realizar modificaciones adicionales a la tarea antes de guardarla.
            new_Task = form.save(commit=False)

            # Asignando al usuario actual como propietario de la tarea
            new_Task.user = request.user

            # Guardando la nueva tarea en la base de datos
            new_Task.save()

            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "create_task.html",
                {"form": Task_Form, "error": "Please provide valid data"},
            )


@login_required
def task_Detail(request: HttpResponse, task_id):
    # pk means primary key
    # user=request.user to show only our tasks
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "GET":
        # El formulario se completa inicialmente con los detalles de la tarea en cuestion
        form = Task_Form(instance=task)

        return render(request, "task_detail.html", {"task": task, "form": form})
    else:
        try:
            # Actualizando los datos
            form = Task_Form(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "task_detail.html",
                {"task": task, "form": form, "error": "Error updating task"},
            )


@login_required
def task_Complete(request: HttpResponse, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks")


@login_required
def task_Delete(request: HttpResponse, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")


@login_required
def tasks_Completed(request: HttpResponse):
    # Filtrando las tareas por las del usuario actual, y mostrando solo las que han sido completadas
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False
    ).order_by("-datecompleted")
    return render(request, "tasks.html", {"tasks": tasks, "title": "Task Completed"})
