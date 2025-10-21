from django.test import TestCase
from users.models import CustomUser
from .models import Meals, WeeklyMealPlan, TrainingSessions, WeeklySessions, TDEE
from django.urls import reverse

class MealsModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="chef@test.com", password="testpass")
        self.meal = Meals.objects.create(
            name="Test Meal",
            totalfat=10,
            totalcarb=20,
            totalprotein=30,
            calories=400,
            chef=self.user,
            dietary_requirements="Vegan"
        )

    def test_meal_creation(self):
        self.assertEqual(self.meal.name, "Test Meal")
        self.assertEqual(self.meal.totalfat, 10)
        self.assertEqual(self.meal.chef.email, "chef@test.com")

class WeeklyMealPlanTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="user@test.com", password="testpass")
        self.meal = Meals.objects.create(name="Meal", chef=self.user)
        self.plan = WeeklyMealPlan.objects.create(day="Monday", meal=self.meal, user=self.user)

    def test_weekly_meal_plan(self):
        self.assertEqual(self.plan.day, "Monday")
        self.assertEqual(self.plan.meal, self.meal)
        self.assertEqual(self.plan.user, self.user)

class AddMealViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="chef@test.com", password="testpass")
        self.client.force_login(self.user)

    def test_addmeal_get(self):
        response = self.client.get(reverse("addmeal"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "plans/addmeal.html")

    def test_addmeal_post(self):
        response = self.client.post(reverse("addmeal"), {
            "mealtitle": "Test Meal",
            "carbgrams": 10,
            "fatgrams": 5,
            "proteingrams": 15,
            "calories": 200
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Meals.objects.filter(name="Test Meal").exists())

