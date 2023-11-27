import datetime
import logging
from django import forms
from .models import Project, Task, SubTask,ProjectResource, ProjectNotification
from users.models import CustomUser
from django.shortcuts import get_object_or_404

STATUS = (
    (1, 'Not started'),
    (2, 'In progress'),
    (3, 'Done'),
    (4, 'In revision'),
)

class TaskRegistrationForm(forms.ModelForm):
    assign = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    name = forms.CharField(max_length=80)
    status = forms.ChoiceField(choices=STATUS)
    content = forms.Textarea()

    class Meta:
        model = Task
        fields = ['name', 'content', 'status']
        labels = {'name': 'Nom'}

    def save(self, commit=True):
        project = Project.objects.get(id=self._projectId)
        for resource in ProjectResource.objects.filter(project_id = self._projectId) :
            if resource.resource != project.author:
                projectNotification = ProjectNotification(
                    projectId=self._projectId, 
                    projectName = self.cleaned_data['name'],
                    description = self.cleaned_data['name'] + " Created",
                    notify = resource.resource,
                    when=datetime.date.today(),
                    author=project.author)
                projectNotification.save()
        
        task = super(TaskRegistrationForm, self).save(commit=False)
        task.name = self.cleaned_data['name']
        task.status = self.cleaned_data['status']
        task.content = self.cleaned_data['content']
        task.project = get_object_or_404(Project, id = self._projectId)
        task.assign = self.cleaned_data['assign']
        task.save()

        if commit:
            task.save()

        return task

    def __init__(self, *args, **kwargs):
        self._projectId = kwargs.pop('projectId', None)
        super(TaskRegistrationForm, self).__init__(*args, **kwargs)

        # this is to get only persons assigned to the project
        # but the self._projectId is empty, don't why
        #self.fields['assign'] = forms.ModelChoiceField(queryset = 
        #    ProjectResource.objects.filter(project_id = self._projectId)) 

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Nom'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['placeholder'] = 'Statut'
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['placeholder'] = 'Contenu'
        self.fields['assign'].widget.attrs['class'] = 'form-control'
        self.fields['assign'].widget.attrs['placeholder'] = 'Collaborateur'

class SubTaskRegistrationForm(forms.ModelForm):
    assign = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    name = forms.CharField(max_length=80)
    status = forms.ChoiceField(choices=STATUS)
    content = forms.Textarea()

    class Meta:
        model = SubTask
        fields = ['name', 'content', 'status']
        labels = {'name': 'Nom'}

    def save(self, commit=True):
        task = Task.objects.get(id=self._taskId)
        for resource in ProjectResource.objects.filter(project_id = task.project.id) :
            if resource.resource != task.project.author:
                projectNotification = ProjectNotification(
                    projectId=task.project.id, 
                    projectName = self.cleaned_data['name'],
                    description = self.cleaned_data['name'] + " Created",
                    notify = resource.resource,
                    when=datetime.date.today(),
                    author=task.project.author)
                projectNotification.save()

        subtask = super(SubTaskRegistrationForm, self).save(commit=False)
        subtask.name = self.cleaned_data['name']
        subtask.status = self.cleaned_data['status']
        subtask.content = self.cleaned_data['content']
        subtask.task = get_object_or_404(Task, id = self._taskId)
        subtask.assign = self.cleaned_data['assign']
        subtask.save()

        if commit:
            subtask.save()

        return subtask

    def __init__(self, *args, **kwargs):
        self._taskId = kwargs.pop('taskId', None)
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Nom'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['placeholder'] = 'Statut'
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['placeholder'] = 'Contenu'
        self.fields['assign'].widget.attrs['class'] = 'form-control'
        self.fields['assign'].widget.attrs['placeholder'] = 'Collaborateur'
