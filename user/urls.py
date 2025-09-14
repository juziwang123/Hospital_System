from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DoctorProfileViewSet, DepartmentViewSet, ScheduleViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'doctors', DoctorProfileViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'appointments', AppointmentViewSet)

# ... 其他导入
from .views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]