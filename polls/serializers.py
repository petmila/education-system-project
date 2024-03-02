from .models import Group, Student, Lesson, Product, RegistrationRequest
from rest_framework import serializers


class ProductForCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'cost', 'author', 'creation_time', 'lessons_amount']


class RegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationRequest
        fields = ['student', 'product']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'cost', 'author', 'creation_time', 'max_students_per_group', 'min_students_per_group']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['product', 'group_name', 'students']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['product', 'lesson_name', 'link']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id']