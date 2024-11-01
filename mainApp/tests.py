from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save
from mainApp.signals import save_user_profile

class RankChangeTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Disconnect the signal to prevent automatic Profile creation
        post_save.disconnect(save_user_profile, sender=User)

    @classmethod
    def tearDownClass(cls):
        # Reconnect the signal after tests
        post_save.connect(save_user_profile, sender=User)
        super().tearDownClass()

    def setUp(self):
        # Create users with unique emails manually
        user1 = User.objects.create_user(username="user1", password="password")
        user2 = User.objects.create_user(username="user2", password="password")
        user3 = User.objects.create_user(username="user3", password="password")

        # Create profiles with unique bc_email values
        self.user1_profile = Profile.objects.create(username=user1, name="User1", points=100, bc_email="user1@bc.edu", school="CSOM")
        self.user2_profile = Profile.objects.create(username=user2, name="User2", points=50, bc_email="user2@bc.edu", school="MCAS")
        self.user3_profile = Profile.objects.create(username=user3, name="User3", points=25, bc_email="user3@bc.edu", school="LSEHD")

    def test_initial_rank(self):
        """Test the initial ranking of users based on points."""
        user1_rank = Profile.objects.filter(points__gt=self.user1_profile.points).count() + 1
        user2_rank = Profile.objects.filter(points__gt=self.user2_profile.points).count() + 1
        user3_rank = Profile.objects.filter(points__gt=self.user3_profile.points).count() + 1

        self.assertEqual(user1_rank, 1)  # User1 should be ranked 1st
        self.assertEqual(user2_rank, 2)  # User2 should be ranked 2nd
        self.assertEqual(user3_rank, 3)  # User3 should be ranked 3rd

    def test_rank_increase(self):
        """Test if a user’s rank increases after gaining points."""
        self.user2_profile.points = 110  # Give User2 more points than User1
        self.user2_profile.save()
        
        user1_rank = Profile.objects.filter(points__gt=self.user1_profile.points).count() + 1
        user2_rank = Profile.objects.filter(points__gt=self.user2_profile.points).count() + 1

        self.assertEqual(user2_rank, 1)  # Now User2 should be ranked 1st
        self.assertEqual(user1_rank, 2)  # User1 should now be ranked 2nd

    def test_rank_decrease(self):
        """Test if a user’s rank decreases after losing points."""
        # Lower User1’s points below User2 and User3
        self.user1_profile.points = 20
        self.user1_profile.save()

        # Refresh ranks after points update
        user1_rank = Profile.objects.filter(points__gt=self.user1_profile.points).count() + 1
        user2_rank = Profile.objects.filter(points__gt=self.user2_profile.points).count() + 1
        user3_rank = Profile.objects.filter(points__gt=self.user3_profile.points).count() + 1

        # Verify ranks based on updated points
        self.assertEqual(user2_rank, 1)  # User2 should be ranked 1st
        self.assertEqual(user3_rank, 2)  # User3 should now be ranked 2nd
        self.assertEqual(user1_rank, 3)  # User1 should now be ranked 3rd

