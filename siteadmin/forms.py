from django import forms
from django.forms import ModelForm

from course.models import CourseCategory, Course


# Add a new course category
class CategoryForm(ModelForm):
    class Meta:
        model = CourseCategory
        fields = '__all__'


# To add new course
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


# To add new subject
class SubjectForm(forms.Form):
    course = forms.CharField(max_length=4)
    subject_code = forms.CharField(max_length=255)
    subject_name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=1024, required=False)
