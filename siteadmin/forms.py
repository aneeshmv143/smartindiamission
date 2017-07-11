from django import forms

class CourseForm(forms.Form):
	course_category = forms.CharField(max_length=24)
	course_code = forms.CharField(max_length=255)
	course_name = forms.CharField(max_length=255)
	course_duration = forms.CharField(max_length=24)
	description = forms.CharField(max_length=255, required=False)