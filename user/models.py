from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


# 自定义用户模型
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("student", "学生"),
        ("teacher", "教师"),
        ("doctor", "医生"),
        ("admin", "管理员"),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    teacher_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)  # 用于管理员审核身份

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username


# 医生信息模型
class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    specialty = models.TextField()

    class Meta:
        verbose_name = '医生信息'
        verbose_name_plural = '医生信息'

    def __str__(self):
        return f'{self.user.username} - {self.title}'


# 科室信息模型
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = '科室'
        verbose_name_plural = '科室'

    def __str__(self):
        return self.name


# 接下来，我们还需要在新的应用中创建排班和挂号模型，我们暂时先把它们定义在 `user` 应用里。

# 医生排班模型
class Schedule(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    available_slots = models.IntegerField(default=10)  # 可用号源数量

    class Meta:
        verbose_name = '医生排班'
        verbose_name_plural = '医生排班'
        unique_together = ('doctor', 'date', 'start_time')  # 确保一个医生同一时间只有一个排班


# 挂号记录模型
class Appointment(models.Model):
    STATUS_CHOICES = (
        ("pending", "待审核"),
        ("confirmed", "已确认"),
        ("cancelled", "已取消"),
        ("completed", "已完成"),
    )
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name = '挂号记录'
        verbose_name_plural = '挂号记录'