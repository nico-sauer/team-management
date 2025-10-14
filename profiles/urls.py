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
    path("athletes/", views.athlete_list, name="athletes-list"),
    path("athletes/details/<int:id>", views.athlete_details, name="athlete-details"),
    path("staff/", views.staff_list, name="staff-list"),
    path("staff/details/<int:id>", views.staff_details, name="staff-details"),
    path("athletes/medical/<int:id>", views.medical_records, name="medical-records"),
    path("athletes/dietary/<int:id>", views.dietary, name="medical-dietary")
]   


router = DefaultRouter()
router.register("api/athletes", views.AthleteViewSet)
#router.register("staff", views.StaffViewSet)
router.register("api/manage/athletes", views.ManagerAccessAthleteViewSet, basename="manage-athletes")
router.register("api/manage/staff", views.ManagerAccessStaffViewSet, basename="manage-staff")
router.register("api/athletes/medical", views.MedicalRecords, basename="medical")
#router.register("athletes/medical/add", plans.views.MedicalRecordsView, basename="add")
router.register("api/athletes/nutri", views.DieticianAccess, basename="nutri")
router.register("api/athletes/train", views.TrainerAccess, basename="train")
router.register("api/athletes/meals", views.ChefAccess, basename="meal")
urlpatterns += router.urls