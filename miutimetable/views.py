from django.shortcuts import render
from .models import AcademicYear, Semester, Faculty, Course, Timetable
from django.utils.html import format_html

def timetable_view(request):
    academic_years = AcademicYear.objects.all()
    semesters = Semester.objects.all()
    faculties = Faculty.objects.all()
    courses = Course.objects.all()

    # Filter timetables based on selected criteria
    academic_year_id = request.GET.get('academic_year')
    semester_id = request.GET.get('semester')
    course_id = request.GET.get('courses')

    timetables = Timetable.objects.all()

    if academic_year_id:
        timetables = timetables.filter(academic_year_id=academic_year_id)
    if semester_id:
        timetables = timetables.filter(semester_id=semester_id)
    if course_id:
        timetables = timetables.filter(course_unit__course_id=course_id)

    timetable_data = {
        'Monday': {'slot_1': [], 'slot_2': [], 'slot_3': [], 'slot_4': []},
        'Tuesday': {'slot_1': [], 'slot_2': [], 'slot_3': [], 'slot_4': []},
        'Wednesday': {'slot_1': [], 'slot_2': [], 'slot_3': [], 'slot_4': []},
        'Thursday': {'slot_1': [], 'slot_2': [], 'slot_3': [], 'slot_4': []},
        'Friday': {'slot_1': [], 'slot_2': [], 'slot_3': [], 'slot_4': []},
        'Saturday': {'slot_1': [], 'slot_2': [], 'slot_3': [], 'slot_4': []},
        'Sunday': {'slot_1': [], 'slot_2': [], 'slot_3': [], 'slot_4': []},
    }

    for timetable in timetables:
        day = timetable.day_of_week
        start_time = timetable.start_time.strftime('%H:%M')
        
        if start_time < '10:00':
            slot = 'slot_1'
        elif start_time < '13:00':
            slot = 'slot_2'
        elif start_time < '16:00':
            slot = 'slot_3'
        else:
            slot = 'slot_4'

        timetable_data[day][slot].append(
            format_html(
                '<li style="text-align: left;"><strong>{}</strong> {} ({})</li>',
                timetable.course_unit.code,
                timetable.course_unit.name,
                timetable.course_unit.lecturer.name
            )
        )

    context = {
        'academic_years': academic_years,
        'semesters': semesters,
        'faculties': faculties,
        'courses': courses,
        'timetables': timetables,
        'timetable_data': timetable_data,
    }

    return render(request, 'timetable.html', context)

def general_timetable_view(request):
    timetables = Timetable.objects.all()
    
    timetable_data = {
        'Monday': {'slot_1': [], 'slot_2': [], 'slot_3': [], 'slot_4': []},
        'Tuesday': {'slot_1': [], 'slot_2': [], 'slot_3': [], 'slot_4': []},
        'Wednesday': {'slot_1': [], 'slot_2': [], 'slot_3': [], 'slot_4': []},
        'Thursday': {'slot_1': [], 'slot_2': [], 'slot_3': [], 'slot_4': []},
        'Friday': {'slot_1': [], 'slot_2': [], 'slot_3': [], 'slot_4': []},
        'Saturday': {'slot_1': [], 'slot_2': [], 'slot_3': [], 'slot_4': []},
        'Sunday': {'slot_1': [], 'slot_2': [], 'slot_3': [], 'slot_4': []},
    }

    for timetable in timetables:
        day = timetable.day_of_week
        start_time = timetable.start_time.strftime('%H:%M')

        if start_time < '10:00':
            slot = 'slot_1'
        elif start_time < '13:00':
            slot = 'slot_2'
        elif start_time < '16:00':
            slot = 'slot_3'
        else:
            slot = 'slot_4'

        course_info = format_html(
            '<li style="text-align: left; padding:2px; margin-left:7px;"><strong>{}</strong><br> {} ({})</li>',
            timetable.course_unit.code,
            timetable.course_unit.name,
            timetable.course_unit.lecturer.name
        )
        timetable_data[day][slot].append(course_info)

    context = {
        'timetables': timetables,
        'timetable_data': timetable_data,
    }

    return render(request, 'general_timetable.html', context)
