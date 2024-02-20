from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            "email":{"required":True}
        }

    def save(self):
        data = self.validated_data

        if User.objects.filter(email = data['email']).exists():
            raise serializers.ValidationError({"Error":"A user with that email id already exists."})
        
        user_data = {
            "username" : data['username'],
            "email" : data['email']
        }
        account = User(**user_data)
        account.set_password(data['password'])
        try:
            account.save()
        except Exception as e:
            raise serializers.ValidationError({"Error": str(e)})
        return account
