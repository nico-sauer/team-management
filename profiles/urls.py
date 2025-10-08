from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import *

#@ team these arent permanent yet (need to switch some from router
# and vice-versa now that views/viewsets have changed/are changing)

urlpatterns = [
    path('add/<int:pk>', MedicalRecordsView.as_view(), name='MedicalRecordsView'),
    #path('list/', AthleteProfileList.as_view(), name='athlete-list'),
    #path('detail<int:pk>', ProfileDetail.as_view(), name='athlete-detail'),
    #path('user/<int:pk>', UserDetail.as_view(), name='user_detail'),
    path("members/", views.athlete_list, name="athletes-list"),
    path("members/details/<int:id>", views.athlete_details, name="athlete-details"),
    path("staff/", views.staff_list, name="staff-list"),
    path("staff/details/<int:id>", views.staff_details, name="staff-details"),
    path("members/medical/<int:id>", views.medical_records, name="medical-records")
]


router = DefaultRouter()
router.register("athletes", views.AthleteViewSet)
#router.register("staff", views.StaffViewSet)
router.register("manage/athletes", views.ManagerAccessAthleteViewSet, basename="manage-athletes")
router.register("manage/staff", views.ManagerAccessStaffViewSet, basename="manage-staff")
router.register("athletes/medical", views.MedicalRecords, basename="medical")
#router.register("athletes/medical/add", plans.views.MedicalRecordsView, basename="add")
router.register("athletes/nutri", views.DieticianAccess, basename="nutri")
router.register("athletes/train", views.TrainerAccess, basename="train")
router.register("athletes/meals", views.ChefAccess, basename="meal")
urlpatterns += router.urls