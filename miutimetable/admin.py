from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from django.forms import BaseModelFormSet
from .models import AcademicYear, Semester, Faculty, Course, Lecturer, CourseUnit, Timetable

# Custom Widget for Horizontal Checkboxes
class HorizontalCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []  # Ensure value is a list

        # Generate checkboxes with inline CSS for six items per line
        output = []
        output.append('<div style="display: flex; flex-wrap: wrap;">')
        for index, (option_value, option_label) in enumerate(self.choices):
            checked = 'checked' if option_value in value else ''
            output.append(
                f'<label class="checkbox-inline" style="flex: 1 0 16.66%; box-sizing: border-box; padding: 0 10px;">'
                f'<input type="checkbox" name="{name}" value="{option_value}" {checked}> {option_label}'
                f'</label>'
            )
            if (index + 1) % 6 == 0:
                output.append('<div style="flex-basis: 100%;"></div>')  # Ensure new line after six items
        output.append('</div>')

        return mark_safe(''.join(output))

# Custom Form for CourseUnit
class CourseUnitForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=HorizontalCheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CourseUnit
        fields = '__all__'

# Custom Form for Inline Course
class CourseInlineForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        course_unit = kwargs.pop('course_unit', None)
        super().__init__(*args, **kwargs)
        if course_unit:
            self.fields['course'].queryset = Course.objects.filter(courseunit__id=course_unit.id)

# Custom Formset for Inline Course
class CourseInlineFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.course_unit = kwargs.pop('course_unit', None)
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['course_unit'] = self.course_unit
        return kwargs

# Inline Admin for Course
class CourseInline(admin.TabularInline):
    model = CourseUnit.courses.through
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.course_unit = obj
        return formset

    def get_formset_kwargs(self, request, obj=None, **kwargs):
        kwargs = super().get_formset_kwargs(request, obj, **kwargs)
        kwargs['formset'] = CourseInlineFormSet
        return kwargs

# Inline Admin for Timetable
class TimetableInline(admin.TabularInline):
    model = Timetable
    extra = 0

# Admin for AcademicYear
@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [TimetableInline]

# Admin for Semester
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [TimetableInline]

# Admin for Faculty
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Admin for Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty')
    search_fields = ('name', 'faculty__name')
    list_filter = ('faculty',)

# Admin for Lecturer
@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact')
    search_fields = ('name', 'contact')

# Admin for CourseUnit
@admin.register(CourseUnit)
class CourseUnitAdmin(admin.ModelAdmin):
    form = CourseUnitForm
    list_display = ('code', 'name', 'display_courses', 'lecturer', 'academic_year', 'semester')

    def display_courses(self, obj):
        return ", ".join(course.name for course in obj.courses.all())
    display_courses.short_description = 'Courses'

    search_fields = ('code', 'name', 'lecturer__name', 'academic_year__name', 'semester__name')
    list_filter = ('lecturer', 'academic_year', 'semester')
    inlines = [CourseInline, TimetableInline]

# Admin for Timetable
@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('academic_year', 'semester', 'course_unit', 'day_of_week', 'start_time', 'end_time')
    search_fields = ('academic_year__name', 'semester__name', 'course_unit__name', 'day_of_week')
    list_filter = ('academic_year', 'semester', 'course_unit', 'day_of_week')
