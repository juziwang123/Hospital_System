from rest_framework import serializers
from .models import CustomUser, DoctorProfile, Department, Schedule, Appointment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'phone_number']

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = DoctorProfile
        fields = ['id', 'user', 'department', 'department_name', 'title', 'specialty']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.username', read_only=True)
    department_name = serializers.CharField(source='doctor.department.name', read_only=True)

    class Meta:
        model = Schedule
        fields = ['id', 'doctor', 'doctor_name', 'department', 'department_name', 'date', 'start_time', 'end_time', 'available_slots']

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.username', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.username', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'patient_name', 'doctor', 'doctor_name', 'schedule', 'appointment_time', 'status']
# 用于注册的序列化器
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'user_type', 'phone_number']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data.get('user_type', 'student'),
            phone_number=validated_data.get('phone_number')
        )
        return user

# 用于登录的序列化器
class LoginSerializer(serializers.MdelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']