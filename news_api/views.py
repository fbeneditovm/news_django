from rest_framework import viewsets
from .models import NewsArticle, Employee, ClientUser
from .serializers import NewsArticleSerializer, EmployeeSerializer, ClientUserSerializer

# Create your views here.
class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class ClientUserViewSet(viewsets.ModelViewSet):
    queryset = ClientUser.objects.all()
    serializer_class = ClientUserSerializer