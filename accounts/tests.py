from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AccountsAuthenticationAndProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='SecurePassword123!',
            first_name='John',
            last_name='Doe'
        )

    def test_registration_view_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertContains(response, 'Create Your AURA Account')

    def test_registration_success(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'password1': 'NewUserSecret987!',
            'password2': 'NewUserSecret987!',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertTrue(User.objects.filter(username='newuser').exists())
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.email, 'jane@example.com')
        self.assertEqual(new_user.first_name, 'Jane')

    def test_registration_duplicate_email(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'duplicateemailuser',
            'first_name': 'Fake',
            'last_name': 'User',
            'email': 'john@example.com',  # already taken by self.user
            'password1': 'Password12345!',
            'password2': 'Password12345!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'An account with this email address already exists.')

    def test_login_success(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'johndoe',
            'password': 'SecurePassword123!',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertContains(response, 'John Doe')

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'johndoe',
            'password': 'WrongPassword!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_logout(self):
        self.client.login(username='johndoe', password='SecurePassword123!')
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/home.html')

    def test_profile_requires_login(self):
        # Unauthenticated request should redirect to login
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_profile_view_and_update(self):
        self.client.login(username='johndoe', password='SecurePassword123!')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'john@example.com')

        # Update profile
        update_response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'Jonathan',
            'last_name': 'Doeman',
            'email': 'jonathan.doeman@example.com',
        }, follow=True)
        self.assertEqual(update_response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Jonathan')
        self.assertEqual(self.user.last_name, 'Doeman')
        self.assertEqual(self.user.email, 'jonathan.doeman@example.com')
        self.assertContains(update_response, 'Jonathan Doeman')
