from rest_framework import serializers
from adminapp.models import tbl_hod,tbl_tutor
from .models import tbl_student
#serializer for login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    login_id = serializers.CharField()  # can be tutor_id / hod_id / student_id
    role = serializers.ChoiceField(choices=[('hod', 'HOD'), ('tutor', 'Tutor'), ('student', 'Student')])

    def validate(self, data):
        email = data.get('email')
        login_id = data.get('login_id')
        role = data.get('role')
        if role == 'tutor':
            try:
                tutor = tbl_tutor.objects.get(email=email, tutor_id=login_id)
            except tbl_tutor.DoesNotExist:
                raise serializers.ValidationError("Invalid Tutor credentials.")
            data['user'] = tutor

        elif role == 'student':
            try:
                student = tbl_student.objects.get(email=email, student_id=login_id)
            except tbl_student.DoesNotExist:
                raise serializers.ValidationError("Invalid Student credentials.")
            data['user'] = student

        data['role'] = role
        return data

#serializer for tutor
from adminapp.models import tbl_tutor
class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_tutor
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.image:
            rep['image'] = instance.image.url
        return rep
    

#serializer for student
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_student
        fields = '__all__'

#serializer for student request for a leave
from rest_framework import serializers
from .models import StudentRequest

class StudentRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.name", read_only=True)
    tutor_name = serializers.CharField(source="tutor.name", read_only=True)
    hod_name = serializers.CharField(source="hod.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = StudentRequest
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.qr_code:
            rep['qr_code'] = instance.qr_code.url
        return rep

#serializer for student profile and update profile
from rest_framework import serializers
from .models import tbl_student,Attendance

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_student
        fields = '__all__'



#code for view departments and courses
from adminapp.models import tbl_department
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_department
        fields = '__all__'

from adminapp.models import tbl_course
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_course
        fields = '__all__'

# serializers.py
#serialzer for mark attendance
from rest_framework import serializers
from .models import MarkAttendance
class MarkAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)  # Custom ID from tbl_student

    class Meta:
        model = MarkAttendance
        fields = ['id', 'student', 'student_id', 'student_name', 'date', 'time']

#serialzer for jobs and company
from adminapp.models import Tbl_Job,Company
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__' 


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbl_Job
        fields = '__all__'












# serializers.py
from rest_framework import serializers
from .models import JobApplication

class JobApplicationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'student', 'student_name', 'job', 'job_title', 'resume', 'status', 'applied_at']
        read_only_fields = ['status', 'applied_at']  # status is controlled by system
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.resume:
            rep['resume'] = instance.resume.url
        return rep