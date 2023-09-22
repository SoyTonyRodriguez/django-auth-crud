from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks_completed/", views.tasks_Completed, name="tasks_completed"),
    path("logout/", views.signout, name="logout"),
    path("signin/", views.signin, name="signin"),
    path("create/task/", views.create_Task, name="create_task"),
    path("tasks/<int:task_id>", views.task_Detail, name="task_detail"),
    path("tasks/<int:task_id>/complete", views.task_Complete, name="task_complete"),
    path("tasks/<int:task_id>/delete", views.task_Delete, name="task_delete"),
]
