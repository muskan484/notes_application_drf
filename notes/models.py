from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    content = models.TextField(blank=False)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name='owned_notes',blank = True)
    shared_users = models.ManyToManyField(User,related_name='shared_notes',blank = True)

    def __str__(self) -> str:
        return f"Note id{self.id} - Owner: {self.owner.username}"

class NoteHistory(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    change = models.TextField()