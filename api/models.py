from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100, help_text="Task name")
    completed = models.BooleanField(default=False)
    status = models.IntegerField()

    def __str__(self):
        return self.title