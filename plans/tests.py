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

    def test_deletemeal(self):
        meal = Meals.objects.create(name="DeleteMe", chef=self.user)
        response = self.client.post(reverse("deletemeal"), {"mealtodelete": meal.id})
        self.assertFalse(Meals.objects.filter(id=meal.id).exists())

    def test_deletemeal_invalid_id(self):
        response = self.client.post(reverse("deletemeal"), {"mealtodelete": 9999})
        self.assertEqual(response.status_code, 404)

    def test_addmeal_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse("addmeal"))
        self.assertEqual(response.status_code, 302)  # redirect to login

class TrainingSessionsModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="trainer@test.com", password="testpass")
        self.session = TrainingSessions.objects.create(
            name="Morning Cardio",
            type="Cardio",
            description="Cardio session for all athletes",
            trainer=self.user
        )

    def test_training_session_creation(self):
        self.assertEqual(self.session.name, "Morning Cardio")
        self.assertEqual(self.session.type, "Cardio")
        self.assertEqual(self.session.trainer, self.user)

class WeeklySessionsModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="athlete@test.com", password="testpass")
        self.trainer = CustomUser.objects.create(email="trainer@test.com", password="testpass")
        self.session = TrainingSessions.objects.create(
            name="Strength",
            type="Strength",
            description="Strength training",
            trainer=self.trainer
        )
        self.weekly_session = WeeklySessions.objects.create(
            day="Tuesday",
            session=self.session,
            user=self.user
        )

    def test_weekly_session_creation(self):
        self.assertEqual(self.weekly_session.day, "Tuesday")
        self.assertEqual(self.weekly_session.session, self.session)
        self.assertEqual(self.weekly_session.user, self.user)

class AddTrainingScheduleViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="trainer@test.com", password="testpass")
        self.client.force_login(self.user)
        self.session = TrainingSessions.objects.create(
            name="Evening Yoga",
            type="Flexibility",
            description="Yoga session",
            trainer=self.user
        )

    def test_addtrainingschedule_get(self):
        response = self.client.get(reverse("addtrainingschedule"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "plans/addtrainingschedule.html")

    def test_addtrainingschedule_post(self):
        response = self.client.post(reverse("addtrainingschedule"), {
            "day": "Wednesday",
            "session_select": self.session.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(WeeklySessions.objects.filter(day="Wednesday", session=self.session, user=self.user).exists())

class MealPlanViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="athlete@test.com", password="testpass")
        self.client.force_login(self.user)
        self.meal = Meals.objects.create(name="Healthy Meal", chef=self.user)
        WeeklyMealPlan.objects.create(day="monday_breakfast", meal=self.meal, user=self.user)

    def test_mealplan_get(self):
        response = self.client.get(reverse("mealplan"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "plans/mealplan.html")
        self.assertContains(response, "Healthy Meal")

class CalculateMacrosTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="athlete@test.com", password="testpass")
        self.meal1 = Meals.objects.create(name="Meal1", totalfat=10, totalcarb=20, totalprotein=30, calories=400, chef=self.user)
        self.meal2 = Meals.objects.create(name="Meal2", totalfat=20, totalcarb=30, totalprotein=40, calories=500, chef=self.user)
        WeeklyMealPlan.objects.create(day="Monday", meal=self.meal1, user=self.user)
        WeeklyMealPlan.objects.create(day="Tuesday", meal=self.meal2, user=self.user)

    def test_calculate_macros(self):
        from plans.views import calculate_macros
        weekly_meals = WeeklyMealPlan.objects.filter(user=self.user)
        macros = calculate_macros(weekly_meals)
        self.assertIn("average_fat", macros)
        self.assertIn("average_carb", macros)
        self.assertIn("average_protein", macros)
        self.assertIn("average_calories", macros)
