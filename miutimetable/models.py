from django.db import models

class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Semester(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Lecturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CourseUnit(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course)  # Many-to-Many relationship
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Timetable(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course_unit = models.ForeignKey(CourseUnit, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.course_unit.name} - {self.day_of_week} - {self.start_time} to {self.end_time}"

class CourseLoad(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lecturer} - {self.course}"