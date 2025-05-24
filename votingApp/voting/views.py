from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from .models import CustomUser, Candidate
from .serializers import RegisterSerializer, LoginSerializer, CandidateSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({'success': True, 'message': 'Login successful', 'user_id': user.id})
        return Response({'success': False, 'message': 'Invalid university ID or password'}, status=400)




class CandidateList(APIView):
    def get(self, request):
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        candidate_id = request.data.get("candidate_id")

        # Validate user_id and candidate_id presence
        if not user_id or not candidate_id:
            return Response({"message": "user_id and candidate_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Safely get user and candidate or return 404
        user = get_object_or_404(CustomUser, id=user_id)

        if user.has_voted:
            return Response({"message": "Already voted"}, status=status.HTTP_403_FORBIDDEN)

        candidate = get_object_or_404(Candidate, id=candidate_id)
        candidate.vote_count += 1
        candidate.save()

        user.has_voted = True
        user.save()

        return Response({"message": "Vote successful"})
