from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Team, Group


class UserTests(TestCase):
    
    #test the creation of a new user
    def test_create_user(self):
        db = get_user_model()
        
        user = db.objects.create_user(
            email='testuser@mail.com',first_name='test', last_name='user', password='test1234!',)
        self.assertEqual(user.email, 'testuser@mail.com')
        self.assertEqual(user.first_name, 'test')
        self.assertEqual(user.last_name, 'user')
        self.assertFalse(user.is_superuser, False)
        self.assertFalse(user.is_staff, False)
        self.assertEqual(str(user), "testuser@mail.com")
        
    #test the creation of a new superuser    
    def test_create_superuser(self):
        db = get_user_model()
        
        super_user = db.objects.create_superuser(
            email='testuser@mail.com',
            first_name='test',
            last_name='user',
            password='test1234!',
            )
        self.assertEqual(super_user.email, 'testuser@mail.com')
        self.assertEqual(super_user.first_name, 'test')
        self.assertEqual(super_user.last_name, 'user')
        self.assertTrue(super_user.is_superuser, True)
        self.assertTrue(super_user.is_staff, True)
        self.assertEqual(str(super_user), "testuser@mail.com")
        
    #test the creation of a new user with a missing email     
    def test_missing_email(self):
        db = get_user_model()
        
        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='',
                first_name='test',
                last_name='user',
                password='test1234!',
                is_superuser = False,
            )
    #test the creation of a new team        
    def test_create_team(self):
                
        db = get_user_model()
        
        user = db.objects.create_user(
            email='testuser5@mail.com',
            first_name='test',
            last_name='user', password='test1234!',
            )
        team_id_db = Team.objects.create(team_name='new team', manager=user)
        user.team_id = team_id_db
        self.assertEqual(user.team_id, team_id_db)
        self.assertEqual(str(team_id_db), 'new team')