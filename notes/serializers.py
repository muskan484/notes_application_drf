from .models import Note, NoteHistory
from rest_framework.serializers import ModelSerializer

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

class NoteHistorySerializer(ModelSerializer):
    class Meta:
        model = NoteHistory
        fields = "__all__"