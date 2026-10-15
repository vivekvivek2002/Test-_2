from django.test import TestCase, Client, override_settings
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
            is_featured=True,
            in_stock=True
        )
        self.standard_product = Product.objects.create(
            name="Aura In-Ear Air",
            slug="aura-in-ear-air",
            description="Ultra-light wireless earbuds with active noise cancellation.",
            price=199.00,
            category=self.active_category,
            is_active=True,
            is_featured=False,
            in_stock=True
        )
        self.backordered_product = Product.objects.create(
            name="Aura Studio Subwoofer",
            slug="aura-studio-subwoofer",
            description="Low frequency acoustic pressure chamber.",
            price=799.00,
            category=self.active_category,
            is_active=True,
            is_featured=False,
            in_stock=False
        )
        self.inactive_product = Product.objects.create(
            name="Archived Headset 2021",
            slug="archived-headset",
            description="Legacy model no longer sold.",
            price=99.00,
            category=self.active_category,
            is_active=False,
            is_featured=False,
            in_stock=False
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
        self.assertContains(response, 'Aura Studio Subwoofer')
        # Inactive product must not be shown
        self.assertNotContains(response, 'Archived Headset 2021')

    def test_category_sorting_and_filtering(self):
        # 1. Price Ascending
        resp_asc = self.client.get(reverse('store:category_detail', kwargs={'slug': 'audio'}) + '?sort=price_asc')
        self.assertEqual(resp_asc.status_code, 200)
        prods_asc = list(resp_asc.context['products'])
        self.assertEqual(prods_asc[0], self.standard_product)  # $199
        self.assertEqual(prods_asc[-1], self.backordered_product)  # $799

        # 2. Price Descending
        resp_desc = self.client.get(reverse('store:category_detail', kwargs={'slug': 'audio'}) + '?sort=price_desc')
        prods_desc = list(resp_desc.context['products'])
        self.assertEqual(prods_desc[0], self.backordered_product)  # $799
        self.assertEqual(prods_desc[-1], self.standard_product)  # $199

        # 3. In Stock Only
        resp_stock = self.client.get(reverse('store:category_detail', kwargs={'slug': 'audio'}) + '?stock=in_stock')
        prods_stock = list(resp_stock.context['products'])
        self.assertIn(self.standard_product, prods_stock)
        self.assertIn(self.featured_product, prods_stock)
        self.assertNotIn(self.backordered_product, prods_stock)

    def test_inactive_category_returns_404(self):
        response = self.client.get(reverse('store:category_detail', kwargs={'slug': 'secret-prototypes'}))
        self.assertEqual(response.status_code, 404)

    def test_product_detail_view(self):
        response = self.client.get(reverse('store:product_detail', kwargs={'slug': 'aura-studio-pro'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_detail.html')
        self.assertContains(response, 'Aura Studio Pro')
        self.assertContains(response, '$499.00')
        self.assertContains(response, 'In Stock')
        self.assertContains(response, 'Studio reference acoustic monitors')
        self.assertContains(response, 'Related Audio')

    def test_inactive_product_returns_404(self):
        response = self.client.get(reverse('store:product_detail', kwargs={'slug': 'archived-headset'}))
        self.assertEqual(response.status_code, 404)

    @override_settings(DEBUG=False)
    def test_custom_404_handler(self):
        response = self.client.get('/definitely-non-existent-page-url/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
        self.assertContains(response, "The page you're looking for can't be found", status_code=404)

    def test_admin_accessible(self):
        self.client.login(username='admin_test', password='TestPassword123!')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AURA Administration')
