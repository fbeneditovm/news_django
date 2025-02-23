from django.shortcuts import render
from rest_framework import viewsets
from .models import Employee, ClientUser
from .serializers import EmployeeSerializer, ClientUserSerializer

# Create your views here.

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class ClientUserViewSet(viewsets.ModelViewSet):
    queryset = ClientUser.objects.all()
    serializer_class = ClientUserSerializer