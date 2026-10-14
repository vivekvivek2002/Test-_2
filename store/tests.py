from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from store.models import Category, Product, Banner


class StoreStorefrontTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Categories
        self.active_category = Category.objects.create(
            name="Audio",
            slug="audio",
            is_active=True
        )
        self.inactive_category = Category.objects.create(
            name="Secret Prototypes",
            slug="secret-prototypes",
            is_active=False
        )

        # Products
        self.featured_product = Product.objects.create(
            name="Aura Studio Pro",
            slug="aura-studio-pro",
            description="Studio reference acoustic monitors with spatial tuning.",
            price=499.00,
            category=self.active_category,
            is_active=True,
            is_featured=True
        )
        self.standard_product = Product.objects.create(
            name="Aura In-Ear Air",
            slug="aura-in-ear-air",
            description="Ultra-light wireless earbuds with active noise cancellation.",
            price=199.00,
            category=self.active_category,
            is_active=True,
            is_featured=False
        )
        self.inactive_product = Product.objects.create(
            name="Archived Headset 2021",
            slug="archived-headset",
            description="Legacy model no longer sold.",
            price=99.00,
            category=self.active_category,
            is_active=False,
            is_featured=False
        )

        # Banners
        self.active_banner = Banner.objects.create(
            title="Aura Pro 2026",
            subtitle="Engineered for silence and absolute clarity.",
            button_text="Discover Now",
            button_link="/product/aura-studio-pro/",
            is_active=True,
            order=1
        )
        self.inactive_banner = Banner.objects.create(
            title="Old Campaign",
            subtitle="Old banner",
            button_text="Learn",
            button_link="/",
            is_active=False,
            order=99
        )

        # Superuser
        self.admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin@aura.test',
            password='TestPassword123!'
        )

    def test_homepage_view(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/home.html')
        
        # Active banner shown, inactive not shown
        self.assertContains(response, 'Aura Pro 2026')
        self.assertNotContains(response, 'Old Campaign')
        
        # Featured product shown in featured section
        self.assertContains(response, 'Aura Studio Pro')
        
        # Categories shown
        self.assertContains(response, 'Audio')
        self.assertNotContains(response, 'Secret Prototypes')

    def test_category_detail_view(self):
        response = self.client.get(reverse('store:category_detail', kwargs={'slug': 'audio'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_list.html')
        self.assertContains(response, 'Aura Studio Pro')
        self.assertContains(response, 'Aura In-Ear Air')
        # Inactive product must not be shown
        self.assertNotContains(response, 'Archived Headset 2021')

    def test_inactive_category_returns_404(self):
        response = self.client.get(reverse('store:category_detail', kwargs={'slug': 'secret-prototypes'}))
        self.assertEqual(response.status_code, 404)

    def test_product_detail_view(self):
        response = self.client.get(reverse('store:product_detail', kwargs={'slug': 'aura-studio-pro'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_detail.html')
        self.assertContains(response, 'Aura Studio Pro')
        self.assertContains(response, '$499.00')
        self.assertContains(response, 'Studio reference acoustic monitors')
        self.assertContains(response, 'Related Audio')

    def test_inactive_product_returns_404(self):
        response = self.client.get(reverse('store:product_detail', kwargs={'slug': 'archived-headset'}))
        self.assertEqual(response.status_code, 404)

    def test_admin_accessible(self):
        self.client.login(username='admin_test', password='TestPassword123!')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AURA Administration')
