from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Your first name must be more than 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name must be more than 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address.")
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TaskManager(models.Manager):
    def validator(self, form):
        errors = {}
        if len(form['title']) < 3:
            errors['length'] = "A task must consist of at least 3 characters!"
        if len(form['title']) == 0:
            errors['empty'] = "A task must be provided!"
        if len(form['description']) < 3:
            errors["length"] = "Description should be at least 3 characters!"
        if len(form['description']) == 0:
            errors['empty'] = "A description must be provided!"
        if len(form['points']) >  3:
            errors['length'] = "Points must contain only numbers up to 3 digits!"
        if len(form['points']) == 0:
            errors['empty'] = "Points must be provided!"
        return errors

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    points = models.IntegerField()
    creator = models.ForeignKey(User, related_name="created_tasks", on_delete=models.CASCADE)
    completed_by = models.ManyToManyField(User, related_name="completed_tasks")
    likes = models.ManyToManyField(User, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TaskManager()

class Comment(models.Model):
    content = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    