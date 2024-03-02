from datetime import datetime

from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=30)
    cost = models.FloatField()
    author = models.CharField(max_length=30)
    creation_time = models.DateTimeField()
    min_students_per_group = models.PositiveIntegerField(default=0)
    max_students_per_group = models.PositiveIntegerField(default=10)

    @property
    def groups(self):
        return Group.objects.filter(product=self)

    @property
    def lessons_amount(self):
        return Lesson.objects.filter(product=self).count()

    def all_students(self):
        return [student for group in self.groups for student in group.students]

    def check_student_access(self, student):
        return student in self.groups


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=30)
    link = models.CharField(max_length=30)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Student(models.Model):
    id = models.IntegerField(primary_key=True)

    @property
    def groups(self):
        return Group.objects.filter(students__group__students=self)


class Group(models.Model):
    group_name = models.CharField(max_length=30)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)


class RegistrationRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        Algorithm for assigning student to a group for the product

        A new student always goes to a group with less students.
        The restrictions for one product are the same for the groups
        """
        if self.product.groups.count == 0:
            if self.product.creation_time < datetime.now():
                new_group_name = str(self.product.product_name + self.product.groups.count())
                new_group = Group(new_group_name, self.product)
                new_group.save()
            else:
                pass

        selected_group = self.product.groups[0]
        for group in self.product.groups:
            if selected_group.students.count() > group.students.count():
                selected_group = group

        if selected_group.students.count() == self.product.max_students_per_group:
            if self.product.creation_time < datetime.now():
                new_group_name = str(self.product.product_name + self.product.groups.count())
                new_group = Group(new_group_name, self.product)
                new_group.save()

                for group in Group.objects.filter(product=self.product):
                    group.students.clear()

                students = self.product.all_students()
                students.append(self.student)
                count_students = 0
                while len(students) > count_students:
                    for group in self.product.groups:
                        group.students.add(students[count_students])

                        count_students += 1
            else:
                pass
        else:
            selected_group.students.add(self.student)

        return super(RegistrationRequest, self).save(*args, **kwargs)