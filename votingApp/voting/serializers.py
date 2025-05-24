from rest_framework import serializers
from .models import CustomUser, Candidate
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('university_id', 'first_name', 'last_name', 'department', 'password', 'confirm_password')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return CustomUser.objects.create_user(**validated_data)

# Django LoginSerializer should match field names from the request
class LoginSerializer(serializers.Serializer):
    university_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Use username=data['university_id'] if your authentication backend expects 'username'
        user = authenticate(username=data['university_id'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid university ID or password.")
        data['user'] = user
        return data


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'
