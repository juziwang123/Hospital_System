from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, DoctorProfile, Department, Schedule, Appointment


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type', 'is_verified']
    list_filter = ['user_type', 'is_verified']
    search_fields = ['username', 'email', 'student_id', 'teacher_id']


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'title']
    list_filter = ['department', 'title']
    search_fields = ['user__username', 'department__name']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'start_time', 'end_time', 'available_slots']
    list_filter = ['doctor', 'date']
    search_fields = ['doctor__user__username']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_time', 'status']
    list_filter = ['status']
    search_fields = ['patient__username', 'doctor__user__username']
