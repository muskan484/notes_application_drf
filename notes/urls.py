from django.urls import path
from .views import (ShareNote,
                    CreateNote,
                    NoteVersionHistoryView,
                    RetrieveUpdateDeleteNote)

urlpatterns = [
    path('create',CreateNote.as_view(), name='create-note'),
    path('<int:id>',RetrieveUpdateDeleteNote.as_view(), name='retrieve-update-delete-note'),
    path('share',ShareNote.as_view(), name='share-note'),
    path("version-history/<int:id>",NoteVersionHistoryView.as_view(), name='note-version-history')
]