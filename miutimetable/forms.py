from django import forms
from .models import AcademicYear, Semester, Faculty, Course, CourseUnit, Lecturer, Timetable

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['academic_year', 'semester', 'course_unit', 'day_of_week', 'start_time', 'end_time']

class CourseUnitForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CourseUnit
        fields = '__all__'  # or specify the fields you want to include