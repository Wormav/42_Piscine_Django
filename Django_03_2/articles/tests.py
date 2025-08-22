from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from .models import Article, UserFavouriteArticle


class AuthenticationRequiredViewsTestCase(TestCase):
    """Test that certain views require authentication"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.article = Article.objects.create(
            title="Test Article",
            author=self.user,
            synopsis="Test synopsis",
            content="Test content",
        )

    def test_favourites_view_requires_authentication(self):
        """Test that favourites view is not accessible to anonymous users"""
        response = self.client.get(reverse("articles:favourites"))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        # Check if redirected to login with next parameter
        self.assertTrue(response["Location"].startswith("/en/login/"))

    def test_publications_view_requires_authentication(self):
        """Test that publications view is not accessible to anonymous users"""
        response = self.client.get(reverse("articles:publications"))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        # Check if redirected to login with next parameter
        self.assertTrue(response["Location"].startswith("/en/login/"))

    def test_publish_view_requires_authentication(self):
        """Test that publish view is not accessible to anonymous users"""
        response = self.client.get(reverse("articles:publish"))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        # Check if redirected to login with next parameter
        self.assertTrue(response["Location"].startswith("/en/login/"))

    def test_favourites_view_accessible_to_authenticated_users(self):
        """Test that favourites view is accessible to authenticated users"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("articles:favourites"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "favourite"
        )  # Should contain favourite-related content

    def test_publications_view_accessible_to_authenticated_users(self):
        """Test that publications view is accessible to authenticated users"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("articles:publications"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "publication"
        )  # Should contain publication-related content

    def test_publish_view_accessible_to_authenticated_users(self):
        """Test that publish view is accessible to authenticated users"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("articles:publish"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Publish")  # Should contain publish form


class AuthenticatedUserRegistrationTestCase(TestCase):
    """Test that authenticated users cannot access registration form"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_authenticated_user_cannot_access_register_form(self):
        """Test that already logged in users cannot access registration form"""
        # First login the user
        self.client.login(username="testuser", password="testpass123")

        # Try to access registration form
        response = self.client.get(reverse("articles:register"))

        # Should be redirected to home page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response["Location"].startswith("/en/")
        )  # Should redirect to home

    def test_anonymous_user_can_access_register_form(self):
        """Test that anonymous users can access registration form"""
        response = self.client.get(reverse("articles:register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")  # Should contain registration form


class DuplicateFavouriteTestCase(TestCase):
    """Test that users cannot add the same article to favourites twice"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.article = Article.objects.create(
            title="Test Article",
            author=self.user,
            synopsis="Test synopsis",
            content="Test content",
        )

    def test_cannot_add_same_article_to_favourites_twice_via_model(self):
        """Test that the model prevents duplicate favourites"""
        # Add article to favourites once
        UserFavouriteArticle.objects.create(user=self.user, article=self.article)

        # Try to add the same article again - should raise IntegrityError
        with self.assertRaises(IntegrityError):
            UserFavouriteArticle.objects.create(user=self.user, article=self.article)

    def test_cannot_add_same_article_to_favourites_twice_via_view(self):
        """Test that the view prevents duplicate favourites"""
        self.client.login(username="testuser", password="testpass123")

        # Add article to favourites via view
        self.client.post(
            reverse("articles:add_favourite", kwargs={"pk": self.article.pk})
        )

        # Check that it was added successfully
        self.assertTrue(
            UserFavouriteArticle.objects.filter(
                user=self.user, article=self.article
            ).exists()
        )

        # Try to add the same article again
        self.client.post(
            reverse("articles:add_favourite", kwargs={"pk": self.article.pk})
        )

        # Should still only have one favourite entry
        favourite_count = UserFavouriteArticle.objects.filter(
            user=self.user, article=self.article
        ).count()
        self.assertEqual(favourite_count, 1)

    def test_toggle_favourite_handles_duplicates_correctly(self):
        """Test that toggle favourite view handles duplicates correctly"""
        self.client.login(username="testuser", password="testpass123")

        # First toggle should add to favourites
        self.client.post(
            reverse("articles:toggle_favourite", kwargs={"pk": self.article.pk})
        )
        self.assertTrue(
            UserFavouriteArticle.objects.filter(
                user=self.user, article=self.article
            ).exists()
        )

        # Second toggle should remove from favourites
        self.client.post(
            reverse("articles:toggle_favourite", kwargs={"pk": self.article.pk})
        )
        self.assertFalse(
            UserFavouriteArticle.objects.filter(
                user=self.user, article=self.article
            ).exists()
        )

        # Third toggle should add back to favourites
        self.client.post(
            reverse("articles:toggle_favourite", kwargs={"pk": self.article.pk})
        )
        self.assertTrue(
            UserFavouriteArticle.objects.filter(
                user=self.user, article=self.article
            ).exists()
        )


class ViewTemplateTestCase(TestCase):
    """Test that views use correct templates"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_favourites_view_uses_correct_template(self):
        """Test that favourites view uses the correct template"""
        response = self.client.get(reverse("articles:favourites"))
        self.assertTemplateUsed(response, "articles/favourites.html")

    def test_publications_view_uses_correct_template(self):
        """Test that publications view uses the correct template"""
        response = self.client.get(reverse("articles:publications"))
        self.assertTemplateUsed(response, "articles/publications.html")

    def test_publish_view_uses_correct_template(self):
        """Test that publish view uses the correct template"""
        response = self.client.get(reverse("articles:publish"))
        self.assertTemplateUsed(response, "articles/publish.html")


class UserPermissionsTestCase(TestCase):
    """Test user permissions and access controls"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user1 = User.objects.create_user(username="user1", password="testpass123")
        self.user2 = User.objects.create_user(username="user2", password="testpass123")
        self.article = Article.objects.create(
            title="Test Article",
            author=self.user1,
            synopsis="Test synopsis",
            content="Test content",
        )

    def test_user_can_only_see_own_publications(self):
        """Test that users only see their own publications"""
        # Login as user1
        self.client.login(username="user1", password="testpass123")
        response = self.client.get(reverse("articles:publications"))
        self.assertContains(response, "Test Article")

        # Login as user2
        self.client.logout()
        self.client.login(username="user2", password="testpass123")
        response = self.client.get(reverse("articles:publications"))
        self.assertNotContains(response, "Test Article")

    def test_different_users_have_separate_favourites(self):
        """Test that different users have separate favourite lists"""
        # User1 adds article to favourites
        UserFavouriteArticle.objects.create(user=self.user1, article=self.article)

        # Login as user1 and check favourites
        self.client.login(username="user1", password="testpass123")
        response = self.client.get(reverse("articles:favourites"))
        self.assertContains(response, "Test Article")

        # Login as user2 and check favourites
        self.client.logout()
        self.client.login(username="user2", password="testpass123")
        response = self.client.get(reverse("articles:favourites"))
        self.assertNotContains(response, "Test Article")
