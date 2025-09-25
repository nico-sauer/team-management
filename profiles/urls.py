from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
]


router = DefaultRouter()
router.register("athletes", views.AthleteViewSet)
router.register("staff", views.StaffViewSet)
router.register("manage/athletes", views.ManagerAccessAthleteViewSet, basename="manage-athletes")
router.register("manage/staff", views.ManagerAccessStaffViewSet, basename="manage-staff")
router.register("athletes/medical", views.MedicalStaffAccess, basename="medical")
router.register("athletes/nutri", views.DieticianAccess, basename="nutri")
router.register("athletes/train", views.TrainerAccess, basename="train")
router.register("athletes/meals", views.ChefAccess, basename="meal")
urlpatterns += router.urls