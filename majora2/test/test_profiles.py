import datetime

from django.test import Client, TestCase
from django.contrib.auth.models import User

from majora2 import models

class BasicUserTest(TestCase):
    def setUp(self):
        self.c = Client()

        # Create a user, but do not approve them
        user = User.objects.create(username='unapproved_user', email='unapproved@example.org')
        user.set_password('password')
        user.is_active = False
        user.save()

        # Create a user, but do approve them
        user = User.objects.create(username='approved_user', email='approved@example.org')
        user.set_password('password')
        user.is_active = True
        user.save()

    def test_nologin_without_registered(self):
        can_login = self.c.login(username='not_registered', password='secret')
        self.assertFalse(can_login)

    def test_nologin_without_approval(self):
        can_login = self.c.login(username='unapproved_user', password='password')
        self.assertFalse(can_login)

    def test_login_with_approval(self):
        can_login = self.c.login(username='approved_user', password='password')
        self.assertTrue(can_login)

    def test_nologin_with_approval_badpass(self):
        can_login = self.c.login(username='approved_user', password='badpass')
        self.assertFalse(can_login)


class ProfileTest(TestCase):
    def setUp(self):
        self.c = Client()

        # Create an institute
        hoot = models.Institute(code="HOOT", name="Hypothetical University of Hooting")
        hoot.save()

        # Create a user awaiting site approval
        user = User.objects.create(username='profiled_user_00', email='profile_00@example.org')
        user.set_password('password')
        user.is_active = False
        user.save()
        profile = models.Profile(user=user, institute=hoot, is_site_approved=False)
        profile.save()

        # Create a user awaiting syadmin approval
        user = User.objects.create(username='profiled_user_01', email='profile_10@example.org')
        user.set_password('password')
        user.is_active = False
        user.save()
        profile = models.Profile(user=user, institute=hoot, is_site_approved=True) # site leads mark this field
        profile.save()

        # Create a fully approved profile user
        user = User.objects.create(username='profiled_user_11', email='profile_11@example.org')
        user.set_password('password')
        user.is_active = True # sysadmins mark this field
        user.save()
        profile = models.Profile(user=user, institute=hoot, is_site_approved=True)
        profile.save()


class ProfileAPIKeyTest(TestCase):
    def setUp(self):
        self.c = Client()

        # Create an institute and user profile
        hoot = models.Institute(code="HOOT", name="Hypothetical University of Hooting")
        hoot.save()
        self.org = hoot

        # Create a fully approved profile user
        user = User.objects.create(username='profiled_user_11', email='profile_11@example.org')
        user.set_password('password')
        user.is_active = True # sysadmins mark this field
        user.save()
        profile = models.Profile(user=user, institute=hoot, is_site_approved=True)
        profile.save()

        self.user = user

        # Create an API key def
        kd = models.ProfileAPIKeyDefinition(
                                            key_name = "Kipper's Magic Key",
                                            lifespan = datetime.timedelta(days=7),
                                            is_service_key=False,
                                            is_read_key=False,
                                            is_write_key=False,
        )
        kd.save()

    def test_profile_institute(self):
        self.assertEqual(self.org.code, self.user.profile.institute.code)
        self.assertEqual(self.org.name, self.user.profile.institute.name)
