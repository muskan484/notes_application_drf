from rest_framework import views
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


class UserSignUp(views.APIView):
    """
    API View for user sign-up functionality. Users can sign up using this endpoint by providing necessary information.

    Permissions:
    - This view is accessible to any user.

    HTTP Methods:
    - POST: Accepts user sign-up data in the request body.
    
    Returns:
    - Upon successful sign-up, returns a success message and status code 201.
    - In case of validation errors, returns error messages and status code 400.
    """
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Signup Successful! Please log in to access the application and start taking notes."}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
class UserLogin(views.APIView):
    """
    API View for user login functionality. Users can log in using this endpoint by providing their username and password.

    Permissions:
    - This view is accessible to any user.

    HTTP Methods:
    - POST: Accepts user login credentials in the request body.

    Returns:
    - Upon successful login, returns an access token and status code 200.
    - If the user is not found or authentication fails, returns error messages and status code 404.
    """
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get("password")

        user = authenticate(username = username, password = password)

        if user is not None:
            token = RefreshToken.for_user(user)
            return Response({"Access_token":str(token.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({"Message":"User not found"},status=status.HTTP_404_NOT_FOUND)