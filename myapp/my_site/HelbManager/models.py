from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
#from simple_history.models import HistoricalRecords

# Create your models here.

# the project in the db with title, ...
class Project(models.Model) :    
    STATUS = (
            (1, 'Not started'),
            (2, 'In progress'),
            (3, 'Done'),
        )
    title = models.CharField(max_length = 25)
    content = models.TextField()
    resources = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ProjectResource', related_name="resources")
    date_posted = models.DateTimeField(default=timezone.now) #For the time now
    start_date = models.DateField(default=None, blank=True, null=True)
    end_date = models.DateField(default=None, blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, blank=True, null=True)
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name = "user_name") #If the user doesn't exist, what we do with his old posts 

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk':self.pk})

class ProjectResource(models.Model):
    resource = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.resource.username

class Task(models.Model):
    STATUS = (
        (1, 'Not started'),
        (2, 'In progress'),
        (3, 'Done'),
        (4, 'In revision'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assign = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    content = models.TextField()
    status = models.PositiveSmallIntegerField(choices=STATUS, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk':self.pk})


class SubTask(models.Model):
    STATUS = (
        (1, 'Not started'),
        (2, 'In progress'),
        (3, 'Done'),
        (4, 'In revision'),
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assign = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    content = models.TextField()
    status = models.PositiveSmallIntegerField(choices=STATUS, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk':self.pk})

class ProjectHistory(models.Model):
    projectId = models.SmallIntegerField()
    entityId = models.SmallIntegerField()
    entityType = models.CharField(max_length=10)
    entityName = models.CharField(max_length=200, default="")
    fromValue = models.SmallIntegerField()
    toValue = models.SmallIntegerField()
    when = models.DateField()
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name = "created_user")

    def __str__(self):
        return self.toValue

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk':self.projectId})


class ProjectNotification(models.Model):
    projectId = models.SmallIntegerField()
    projectName = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=200, default="")
    when = models.DateField()
    read = models.BooleanField(default=False)
    notify = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name = "notify_user")
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name = "notification_created_user")

    def __str__(self):
        return self.toValue

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk':self.projectId})