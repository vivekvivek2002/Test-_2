from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from store.models import Category, Product, Banner


class StoreModelAndAdminTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Audio",
            slug="audio",
            is_active=True
        )
        self.product = Product.objects.create(
            name="Aura Pro Headphones",
            slug="aura-pro-headphones",
            description="High fidelity noise cancelling audio experience.",
            price=349.00,
            category=self.category,
            is_active=True,
            is_featured=True
        )
        self.banner = Banner.objects.create(
            title="Next Gen Sound",
            subtitle="Engineered for silence and sonic depth.",
            button_text="Discover Now",
            button_link="/product/aura-pro-headphones/",
            is_active=True,
            order=1
        )
        self.admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin@aura.test',
            password='TestPassword123!'
        )

    def test_category_creation(self):
        self.assertEqual(str(self.category), "Audio")
        self.assertEqual(self.category.get_absolute_url(), "/category/audio/")
        self.assertTrue(self.category.is_active)

    def test_product_creation(self):
        self.assertEqual(str(self.product), "Aura Pro Headphones")
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(float(self.product.price), 349.00)
        self.assertTrue(self.product.is_featured)
        self.assertTrue(self.product.is_active)

    def test_banner_creation(self):
        self.assertEqual(str(self.banner), "Next Gen Sound")
        self.assertEqual(self.banner.order, 1)
        self.assertTrue(self.banner.is_active)

    def test_admin_accessible(self):
        client = Client()
        client.login(username='admin_test', password='TestPassword123!')
        
        # Admin index
        response = client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AURA Administration')
        self.assertContains(response, 'Categories')
        self.assertContains(response, 'Products')
        self.assertContains(response, 'Banners')

        # Model changelist pages
        cat_resp = client.get('/admin/store/category/')
        self.assertEqual(cat_resp.status_code, 200)
        self.assertContains(cat_resp, 'Audio')

        prod_resp = client.get('/admin/store/product/')
        self.assertEqual(prod_resp.status_code, 200)
        self.assertContains(prod_resp, 'Aura Pro Headphones')

        banner_resp = client.get('/admin/store/banner/')
        self.assertEqual(banner_resp.status_code, 200)
        self.assertContains(banner_resp, 'Next Gen Sound')
