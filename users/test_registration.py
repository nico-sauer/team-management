from django.test import TestCase
from users.forms import CustomUserCreationForm, ROLE_CHOICES
from users.models import CustomUser
from profiles.models import AthleteProfile, StaffProfile
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


class RegistrationFormTests(TestCase):
    def setUp(self):
        # create a dummy group to avoid foreign key issues
        Group.objects.get_or_create(name='Athletes')

    def test_role_choices_include_athlete(self):
        roles = [r[0] for r in ROLE_CHOICES]
        self.assertIn('Athlete', roles)

    def test_save_creates_athlete_profile(self):
        # simulate a manager creating an athlete user via the form
        manager = get_user_model().objects.create_user(email='m@example.com', password='pass')
        form_data = {
            'first_name': 'Ath',
            'last_name': 'Lete',
            'email': 'athlete@example.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!',
            'role': 'Athlete',
        }
        form = CustomUserCreationForm(current_user=manager, data=form_data)
        self.assertTrue(form.is_valid(), form.errors.as_json())
        user = form.save()
        # Refresh from DB and check athlete profile
        athlete = AthleteProfile.objects.filter(user=user).first()
        self.assertIsNotNone(athlete)
        self.assertEqual(athlete.first_name, 'Ath')
        self.assertEqual(athlete.last_name, 'Lete')
