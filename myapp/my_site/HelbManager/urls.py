from django.urls import path
from .views import ProjectDetailView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView, TaskDetailView, TaskDeleteView, SubTaskDeleteView, TaskUpdateView, SubTaskUpdateView
from . import views

urlpatterns = [
    path('', views.home, name='HelbManager-home'),
    #path('user/<str:username>', UserProjectListView.as_view(), name='user-project'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    #path('project/<int:pk>/', views.project_detail_view, name='project-detail'),

    path('project/new/', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:projectId>/task/new/', views.newTask, name='task-create'),
    path('task/<int:taskId>/subtask/new/', views.newSubTask, name='subtask-create'),

    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),

    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),

    path('subtask/<int:pk>/update/', SubTaskUpdateView.as_view(), name='subtask-update'),
    path('subtask/<int:pk>/delete/', SubTaskDeleteView.as_view(), name='subtask-delete'),

    path('project/<int:projectId>/historypage/', views.historypage, name='HelbManager-historypage'),
    path('project/<int:projectId>/project-progress/', views.projectProgress, name='HelbManager-project-progress'),

    path('project/notification/<int:notificationId>', views.notificationRead, name='HelbManager-notification-read'),

    path('about/', views.about, name='HelbManager-about'),
    path('taskFlow/<int:projectId>/', views.dragAndDrop, name='HelbManager-taskFlow'),
    path('update-task-status/<int:taskId>/status/<int:taskStatusId>', views.taskFlow, name='taskFlow-update'),
    path('update-subtask-status/<int:subtaskId>/status/<int:subtaskStatusId>', views.subtaskFlow, name='subtaskFlow-update'), 
]