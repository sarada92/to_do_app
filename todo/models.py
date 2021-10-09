from django.db import models

# Create your models here.
class TodoUsers(models.Model):
    username = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username


class TodoApp(models.Model):
    added_date = models.DateTimeField()
    text = models.CharField(max_length=200)
    username = models.ForeignKey(TodoUsers, on_delete=models.CASCADE)
     
    def __str__(self):
        return self.text