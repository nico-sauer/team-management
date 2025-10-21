from django.test import TestCase
from users.models import CustomUser
from .models import Meals, WeeklyMealPlan, TrainingSessions, WeeklySessions, TDEE
from django.urls import reverse
from plans.views import calculate_macros
# =====================
# Model Tests
# =====================

class MealsModelTest(TestCase):
    """Test creation and fields of Meals model."""
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
    """Test WeeklyMealPlan model logic and relations."""
    # This test ensures WeeklyMealPlan links a meal and user to a specific day.
    def setUp(self):
        self.user = CustomUser.objects.create(email="user@test.com", password="testpass")
        self.meal = Meals.objects.create(name="Meal", chef=self.user)
        self.plan = WeeklyMealPlan.objects.create(day="Monday", meal=self.meal, user=self.user)

    def test_weekly_meal_plan(self):
        self.assertEqual(self.plan.day, "Monday")
        self.assertEqual(self.plan.meal, self.meal)
        self.assertEqual(self.plan.user, self.user)

class AddMealViewTest(TestCase):
    """Test add meal and delete meal views (GET, POST, permissions)."""
    def setUp(self):
        self.user = CustomUser.objects.create(email="chef@test.com", password="testpass")
        self.client.force_login(self.user)

    def test_addmeal_get(self):
        # Should render the add meal page for authenticated user
        response = self.client.get(reverse("addmeal"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "plans/addmeal.html")

    def test_addmeal_post(self):
        # Should create a meal with valid POST data
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
        # Should delete a meal owned by the user
        meal = Meals.objects.create(name="DeleteMe", chef=self.user)
        response = self.client.post(reverse("deletemeal"), {"mealtodelete": meal.id})
        self.assertFalse(Meals.objects.filter(id=meal.id).exists())

    def test_deletemeal_invalid_id(self):
        # Should return 404 when trying to delete a meal that doesn't exist
        response = self.client.post(reverse("deletemeal"), {"mealtodelete": 9999})
        self.assertEqual(response.status_code, 404)


    def test_addmeal_unauthenticated(self):
        # Should redirect to login if user is not authenticated
        self.client.logout()
        response = self.client.get(reverse("addmeal"))
        self.assertEqual(response.status_code, 302)  # redirect to login

class TrainingSessionsModelTest(TestCase):
    """Test TrainingSessions model creation and fields."""
    # This test checks that a TrainingSessions object is created with correct fields.
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
    """Test WeeklySessions model creation and relations."""
    # This test ensures WeeklySessions links a session and user to a specific day.
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
    """Test add training schedule view (GET, POST)."""
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
        # Should render the add training schedule page for authenticated user
        response = self.client.get(reverse("addtrainingschedule"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "plans/addtrainingschedule.html")

    def test_addtrainingschedule_post(self):
        # Should create a weekly session with valid POST data
        response = self.client.post(reverse("addtrainingschedule"), {
            "day": "Wednesday",
            "session_select": self.session.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(WeeklySessions.objects.filter(day="Wednesday", session=self.session, user=self.user).exists())

class MealPlanViewTest(TestCase):
    """Test meal plan view for correct template and content."""
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
    """Test calculate_macros utility function with weekly meals."""
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

    class CalculateMacrosEmptyTest(TestCase):
        # This test checks that calculate_macros returns zeros for an empty queryset (edge case).
        def test_empty_meals_queryset(self):
            result = calculate_macros(WeeklyMealPlan.objects.none())
            self.assertEqual(result["average_fat"], 0)
            self.assertEqual(result["average_carb"], 0)
            self.assertEqual(result["average_protein"], 0)
            self.assertEqual(result["average_calories"], 0)
            self.assertIsInstance(result, dict)


class TDEEModelTest(TestCase):
    # This test checks creation and default values for the TDEE model.
    def setUp(self):
        self.user = CustomUser.objects.create(email="user@test.com", password="testpass")
        self.tdee = TDEE.objects.create(user=self.user, calories=2500)

    def test_tdee_creation(self):
        # Should create TDEE object with specified calories
        self.assertEqual(self.tdee.user, self.user)
        self.assertEqual(self.tdee.calories, 2500)

    def test_default_calories(self):
        # Should default calories to 0 if not specified
        tdee = TDEE.objects.create(user=self.user)
        self.assertEqual(tdee.calories, 0)


# =====================
# Permissions and Error Handling Tests
# =====================

class DeleteMealAsOtherUserTest(TestCase):
    """Test that only the owner can delete their meal."""
    def setUp(self):
        self.user1 = CustomUser.objects.create(email="user1@test.com", password="testpass")
        self.user2 = CustomUser.objects.create(email="user2@test.com", password="testpass")
        self.meal = Meals.objects.create(name="NotYours", chef=self.user1)
        self.client.force_login(self.user2)

    def test_delete_meal_as_other_user(self):
        # Should not allow deletion of a meal by a non-owner
        response = self.client.post(reverse("deletemeal"), {"mealtodelete": self.meal.id})
        self.assertTrue(Meals.objects.filter(id=self.meal.id).exists())
        self.assertIn(response.status_code, [403, 404])

class DeleteMealFromPlanInvalidTest(TestCase):
    """Test deleting a non-existent meal from a plan returns error."""
    def setUp(self):
        self.user = CustomUser.objects.create(email="user@test.com", password="testpass")
        self.client.force_login(self.user)

    def test_delete_nonexistent_meal_from_plan(self):
        # Should return 404 or 500 when trying to delete a meal that doesn't exist in the plan
        response = self.client.post(reverse("deletefromplan"), {
            "mealtodelete": 9999,
            "daydelete": "Monday"
        })
        self.assertIn(response.status_code, [404, 500])

class AddMealInvalidPostTest(TestCase):
    """Test that meal is not created if required fields are missing."""
    def setUp(self):
        self.user = CustomUser.objects.create(email="chef@test.com", password="testpass")
        self.client.force_login(self.user)

    def test_add_meal_missing_title(self):
        # Should not create a meal if title is missing
        response = self.client.post(reverse("addmeal"), {
            "carbgrams": 10,
            "fatgrams": 5,
            "proteingrams": 15,
            "calories": 200
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Meals.objects.filter(totalcarb=10, chef=self.user).exists())
