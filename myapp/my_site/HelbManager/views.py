import datetime
from enum import Enum
import logging
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from HelbManager.forms import TaskRegistrationForm, SubTaskRegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from HelbManager.models import Project, Task, SubTask, ProjectHistory, ProjectNotification, ProjectResource

#    logging.basicConfig(level=logging.NOTSET) 
#    logging.debug(pk)

def home(request):
    notifications=ProjectNotification.objects.filter(notify_id=request.user, read=False)
    if int(request.user.role) == 1:
        context = {
            'projects': Project.objects.filter(author=request.user),
            'tasks' : Task.objects.filter(project_id__in=(list(Project.objects.filter(author=request.user)))),
            'notifications' : notifications
        }
        return render(request, 'HelbManager/home.html', context)

    if int(request.user.role) == 2:
        context = {
            'projects': Project.objects.filter(id__in=(Task.objects.filter(assign=request.user).values_list("project_id"))),
            'tasks' : Task.objects.filter(assign=request.user),
            'notifications' : notifications
        }
        return render(request, 'HelbManager/home.html', context)
        
    return redirect('register')

def projectProgress(request, projectId):
    if int(request.user.role) == 1:
        tasks = Task.objects.filter(project_id = projectId)
        taskToDoCount = 0
        taskToInprogressCount = 0
        taskToDoneCount= 0
        taskToInrevisionCount = 0

        if tasks.filter(status=1).count() > 0:
            taskToDoCount = (tasks.filter(status=1).count() / tasks.count()) * 100

        if tasks.filter(status=2).count() > 0:
            taskToInprogressCount = (tasks.filter(status=2).count() / tasks.count()) * 100
        
        if tasks.filter(status=3).count() > 0:
            taskToDoneCount = (tasks.filter(status=3).count() / tasks.count()) * 100
        
        if tasks.filter(status=4).count() > 0:
            taskToInrevisionCount = (tasks.filter(status=4).count() / tasks.count()) * 100
        
        if int(request.user.role) == 1:
            context = {
                'project' : Project.objects.filter(id = projectId),
                'taskToDoCount' : int(taskToDoCount),
                'taskToInprogressCount' : int(taskToInprogressCount),
                'taskToDoneCount' : int(taskToDoneCount),
                'taskToInrevisionCount' : int(taskToInrevisionCount),
                'taskCount': tasks.count()
            }
            return render(request, 'HelbManager/projecprogress.html', context)
    return redirect('projecprogress')
    
def historypage(request, projectId):
    if int(request.user.role) == 1:
        context = {
            'projectHistoryElements' : ProjectHistory.objects.filter(projectId = projectId).order_by("entityId", "when"),
            }
        return render(request, 'HelbManager/historypage.html', context)
    return redirect('historypage')

def notificationRead(request, notificationId):
    notification = ProjectNotification.objects.get(id = notificationId)
    notification.read = True
    notification.save()
    return redirect(home)

class ProjectDetailView(DetailView):
    model = Project
    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['tasks'] = Task.objects.filter(project_id=self.kwargs.get('pk'))
        
        if self.request.user.role == 2: 
            context['tasks'] = Task.objects.filter(project_id=self.kwargs.get('pk'), assign=self.request.user)

        return context
    
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['title', 'content', 'resources']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def newTask(request, projectId):
    if request.method == 'POST':
        form = TaskRegistrationForm(request.POST, projectId=projectId)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'HelbManager/task_form.html', context)
        else:
            return render(request, 'HelbManager/task_form.html', context)
    else:
        form = TaskRegistrationForm()
        context = {
            'form': form,
        }
        return render(request,'HelbManager/task_form.html', context)

def newSubTask(request, taskId):
    if request.method == 'POST':
        form = SubTaskRegistrationForm(request.POST, taskId=taskId)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'HelbManager/subtask_form.html', context)
        else:
            return render(request, 'HelbManager/subtask_form.html', context)
    else:
        form = TaskRegistrationForm()
        context = {
            'form': form,
        }
        return render(request,'HelbManager/subtask_form.html', context)

class TaskDetailView(DetailView):
    model = Task
    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context['subtasks'] = SubTask.objects.filter(task_id=self.kwargs.get('pk'))
        return context

        
class ProjectUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'content', 'status', 'start_date', 'end_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    def test_func(self):
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False

class TaskUpdateView(UpdateView):
    model = Task
    fields = ['name', 'content', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    def test_func(self):
        task = self.get_object()
        if self.request.user == task.assign:
            return True
        return False

class SubTaskUpdateView(UpdateView):
    model = SubTask
    fields = ['name', 'content', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    def test_func(self):
        subtask = self.get_object()
        if self.request.user == subtask.assign:
            return True
        return False

class ProjectDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Project
    success_url = '/'

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False

class TaskDeleteView(DeleteView):
    model = Task
    success_url = '/'
    
    def test_func(self):
        task = self.get_object()
        if self.request.user == task.assign:
            return True
        return False

class SubTaskDeleteView(DeleteView):
    model = SubTask
    success_url = '/'
    
    def test_func(self):
        subtask = self.get_object()
        if self.request.user == subtask.assign:
            return True
        return False

def about(request):
    return render(request, 'HelbManager/about.html', {'title' : 'About'})

def dragAndDrop(request, projectId):
    if int(request.user.role) == 1:
        context = {
            'projects': Project.objects.filter(author=request.user),
            'tasks' : Task.objects.filter(project_id = projectId),
            'subtasks' : SubTask.objects.filter(task_id__in=(list(Task.objects.filter(project_id = projectId))))

        }
        return render(request, 'HelbManager/taskFlow.html', context)

    if int(request.user.role) == 2:
        context = {
            'projects': Project.objects.filter(author=request.user),
            'tasks' : Task.objects.filter(assign=request.user, project_id = projectId),
            'subtasks' : SubTask.objects.filter(task_id__in=(list(Task.objects.filter(assign=request.user, project_id = projectId))), assign=request.user),
         }
        return render(request, 'HelbManager/taskFlow.html', context)
        
    return redirect('register')

def taskFlow(request, taskId, taskStatusId):
  task = Task.objects.get(id=taskId)
  
  projectHistory = CreateHistory(task.project_id,  task.id, 'TASK',task.name,task.status, taskStatusId,request.user)

  for resource in ProjectResource.objects.filter(project_id = task.project_id) :
    if resource.resource != request.user:
        projectNotification = ProjectNotification(
            projectId=task.project_id, 
            projectName = task.project.title,
            description = task.name + " status changed to " +  StatusDescription(taskStatusId),
            notify = resource.resource,
            when=datetime.date.today(),
            author=request.user)
        projectNotification.save()

  task.status = taskStatusId
  projectHistory.save()
  task.save()
  return render(request, 'HelbManager/taskFlow.html')

def subtaskFlow(request, subtaskId, subtaskStatusId):
  subtask = SubTask.objects.get(id=subtaskId)
  
  projectHistory = CreateHistory(subtask.task.project_id,  subtask.id, 'SUBTASK',subtask.name,subtask.status, subtaskStatusId,request.user)

  for resource in ProjectResource.objects.filter(project_id = subtask.task.project_id) :
    if resource.resource != request.user:
        projectNotification = ProjectNotification(
            projectId=subtask.task.project_id, 
             projectName = subtask.task.project.title,
            description = subtask.name + " status changed to " + StatusDescription(subtaskStatusId),
            notify = resource.resource,
            when=datetime.date.today(),
            author=request.user)
        projectNotification.save()

  subtask.status = subtaskStatusId

  projectHistory.save()
  subtask.save()
  return render(request, 'HelbManager/taskFlow.html')

def StatusDescription(statusId):
    if statusId == 1:
        return 'To do'
    if statusId == 2:
        return 'In progress'
    if statusId == 3:
        return 'Done'
    if statusId == 4:
        return 'In revision'

def CreateHistory(projectId, entityId, entityType, entityName, fromValue,  toValue, user):
    return ProjectHistory(
        projectId=projectId, 
        entityId=entityId, 
        entityType=entityType,
        entityName = entityName,
        fromValue=fromValue, 
        toValue=toValue,
        when=datetime.date.today(),
        author=user)

def RegisterCollaboratorToProject(request, projectId):
    if request.method == 'POST':
        form = TaskRegistrationForm(request.POST, projectId=projectId)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'HelbManager/task_form.html', context)
        else:
            return render(request, 'HelbManager/task_form.html', context)

    

