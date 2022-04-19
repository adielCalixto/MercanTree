from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()