from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    channel_id = models.IntegerField()
    reward = models.IntegerField()
    photo = models.ImageField(upload_to="tasks/", null=True)

class TaskCompletion(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey("users.TgUser", on_delete=models.CASCADE)

    created_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True)
