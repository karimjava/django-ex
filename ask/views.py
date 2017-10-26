from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from main import filters
# Create your views here.


class UsersViewSet(viewsets.ModelViewSet):
    model = Users
    queryset = model.objects.all()
    serializer_class = UserSerializers
    filter_backends = (filters.MainSearchFilter, )


class QuestionsViewSet(viewsets.ModelViewSet):
    model = questions
    queryset = model.objects.all()
    serializer_class = QuestionSerializers
    filter_backends = (filters.OwnerSearchFilter, filters.MainSearchFilter, filters.MainOrdereringFilter)

class ResultViewSet(viewsets.ModelViewSet):
    model = Result
    queryset = model.objects.all()
    serializer_class = ResultSerializers
