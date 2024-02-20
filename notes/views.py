from datetime import datetime
from rest_framework import status
from .models import Note, NoteHistory
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .serializers import (NoteSerializer,
                          NoteHistorySerializer)


class CreateNote(CreateAPIView):
    """
    API View for creating a new note. Users can create a new note by providing the note content.

    Permissions:
    - This view is accessible to only authenticated users

    HTTP Methods:
    - POST: Accepts note data in the request body to create a new note.

    Returns:
    - Upon successful creation, returns a success message and status code 201.
    - In case of validation errors, returns error messages and status code 400.
    """
    serializer_class = NoteSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        data["owner"] = request.user.id
        serializer = NoteSerializer(data = data)

        if serializer.is_valid():
            note = serializer.save()
            NoteHistory.objects.create(
                note=note,
                user=request.user,
                change="Note created",
            )
            return Response({"Message":"Note created"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class RetrieveUpdateDeleteNote(APIView):
    """
    API View for retrieving, updating, and deleting a specific note based on the note's ID.
    The view ensures that only the note owner or shared users can perform updates or deletions.

    Permissions:
    - This view is accessible to authenticated and shared users for retrieving and updating. 
    - For deleting the note user should be the owner of the note

    HTTP Methods:
    - GET: Retrieves the details of a specific note.
    - PUT: Updates the content of a specific note.
    - DELETE: Deletes a specific note.

    Returns:
    - For GET requests, returns the details of the note and status code 200.
    - For PUT requests, returns a success message upon successful update and status code 200.
    - For DELETE requests, returns a success message upon successful deletion and status code 204.
    - In case of errors such as invalid data, missing note, or lack of permissions, appropriate error messages
      with status codes 400, 404, or 403 are returned.
    """
    def get(self, request, *args, **kwargs):
        note_id = kwargs['id']
        user_notes = list(Note.objects.filter(id = note_id).values())
        return Response(user_notes, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        data = request.data
        try:
            note_content = data['content']
            if not note_content:
                return Response({"Message":"Note content is required"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"Message":"Note key is required"},status=status.HTTP_400_BAD_REQUEST)

        note_id = kwargs.get("id")
        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return Response({"Message":"Note not found"}, status=status.HTTP_404_NOT_FOUND)
        
        shared_users = list(note.shared_users.all())
        if request.user == note.owner or request.user in shared_users:
            current_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            updated_note = f"{note.content}\n{note_content}"
            note.content = updated_note
            note.save()
            NoteHistory.objects.create(
                note= note,
                user = request.user,
                timestamp = current_time,
                change = f"Note updated: Added '{note_content}' by user {request.user}",
            )
            return Response({"Message":"Note updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"Message":"You do not have permission to edit this note"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        note_id = kwargs.get("id")
        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return Response({"Message":"Note not found"}, status=status.HTTP_404_NOT_FOUND)
    
        if request.user == note.owner:
            note.delete()
            return Response({"Message":"Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Message":"You do not have permission to delete this note"}, status=status.HTTP_403_FORBIDDEN)
    
class ShareNote(APIView):
    """
    API View for sharing a note with other users by providing the note ID and a list of usernames to share the note with.

    Permissions:
    - Only the owner of the note can share it with other users.

    HTTP Method:
    - POST: Shares the note with the specified users.

    Returns:
    - Returns a success message upon successful sharing and status code 200.
    - In case of errors such as note or user not found, or other exceptions, appropriate
      error messages with status codes 404 or 400 are returned.
    """
    def post(self, request, *args, **kwargs):
        try:
            note_id = request.data.get("note_id")
            shared_users = request.data.get("shared_users")

            note = Note.objects.get(id= note_id)
            if note.owner != request.user:
                return Response({"Message":"You are not the owner of this note, permission denied"}, status=status.HTTP_403_FORBIDDEN)
            
            for username in shared_users:
                user = User.objects.get(username = username)
                note.shared_users.add(user)
            note.save()

            return Response({"Message":"Note shared successfully"},status=status.HTTP_200_OK)
        except Note.DoesNotExist:
            return Response({"Message":"Note not found"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"Message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class NoteVersionHistoryView(APIView):
    """
    API View for retrieving the version history of a specific note based on the note's ID.

    Permissions:
    - authenticated users and shared users can access the version history of a note.

    HTTP Method:
    - GET: Retrieves the version history of the specified note.

    Returns:
    - Returns the version history of the note and status code 200.
    - In case of errors such as note history not found or note not found, appropriate error messages
      with status codes 404 are returned.
    """
    def get(self, request, *args, **kwargs):
        note_id = kwargs.get("id")
        try:
            note = Note.objects.get(id = note_id)      
            shared_users = list(note.shared_users.all())
            if request.user == note.owner or request.user in shared_users:
                note_history = NoteHistory.objects.filter(note=note)
                serializer = NoteHistorySerializer(note_history, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except NoteHistory.DoesNotExist:
            return Response({"Message":"Note history not found"}, status=status.HTTP_404_NOT_FOUND)
        except Note.DoesNotExist:
            return Response({"Message":"Note not found"},status=status.HTTP_404_NOT_FOUND)
