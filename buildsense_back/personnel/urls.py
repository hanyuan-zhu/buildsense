from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, EmployeeChangeLogViewSet, EmployeeEntryViewSet, EmployeeTransferViewSet, EmployeeResignationViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'employee_changes', EmployeeChangeLogViewSet)
router.register(r'employee_entries', EmployeeEntryViewSet, basename='employee_entry')
router.register(r'employee_transfers', EmployeeTransferViewSet, basename='employee_transfer')
router.register(r'employee_resignations', EmployeeResignationViewSet, basename='employee_resignation')

urlpatterns = [
    path('', include(router.urls)),
    path('employee_changes/<int:pk>/approve/', EmployeeChangeLogViewSet.as_view({'put': 'approve'}), name='employee-change-approve'),
    path('employee_changes/<int:pk>/reject/', EmployeeChangeLogViewSet.as_view({'put': 'reject'}), name='employee-change-reject'),
]