from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework import permissions, viewsets, status

from .models import Group, Student, Lesson, Product, RegistrationRequest
from .serializers import GroupSerializer, StudentSerializer, \
    LessonSerializer, ProductSerializer, ProductForCustomerSerializer, RegistrationRequestSerializer


class RegistrationRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows student to purchase product.
    """
    queryset = RegistrationRequest.objects.all()
    serializer_class = RegistrationRequestSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited by admin
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed or edited by admin
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed by customers or edited by admin
    """
    serializer_classes = {
        'list': ProductForCustomerSerializer,
        'get': ProductForCustomerSerializer,
    }
    default_serializer_class = ProductSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)
    queryset = Product.objects.all()


class LessonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows lessons to be viewed or edited by admin
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

