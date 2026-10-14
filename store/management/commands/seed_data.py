import os
import io
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from store.models import Category, Product, Banner
from PIL import Image, ImageDraw


def create_sample_image(width, height, bg_color, title_text, accent_color=(0, 113, 227)):
    """
    Generates a crisp minimalist placeholder image using Pillow.
    """
    image = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Draw subtle modern geometry
    draw.rounded_rectangle(
        [(width * 0.1, height * 0.1), (width * 0.9, height * 0.9)],
        radius=int(min(width, height) * 0.06),
        outline=accent_color,
        width=int(min(width, height) * 0.01) or 2
    )

    # Draw center visual icon/shape
    cx, cy = width // 2, height // 2
    r = int(min(width, height) * 0.15)
    draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=accent_color)

    # Save to in-memory bytes buffer
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=90)
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = "Seed database with initial categories, products, banners, and test users."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Initializing AURA database seeding..."))

        # 1. Superuser
        admin_user, created = User.objects.get_or_create(username="admin")
        admin_user.email = "admin@aurastore.com"
        admin_user.set_password("AdminPass123!")
        admin_user.first_name = "Super"
        admin_user.last_name = "Admin"
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save()
        self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} superuser: admin / AdminPass123!"))

        # 2. Test Customer
        customer_user, created = User.objects.get_or_create(username="customer")
        customer_user.email = "customer@aurastore.com"
        customer_user.set_password("CustomerPass123!")
        customer_user.first_name = "Alex"
        customer_user.last_name = "Morgan"
        customer_user.is_staff = False
        customer_user.is_superuser = False
        customer_user.is_active = True
        customer_user.save()
        self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} test customer: customer / CustomerPass123!"))

        # 3. Categories
        categories_data = [
            {
                "name": "Audio",
                "slug": "audio",
                "bg": (245, 245, 247),
                "accent": (40, 40, 42)
            },
            {
                "name": "Laptops",
                "slug": "laptops",
                "bg": (240, 242, 245),
                "accent": (0, 113, 227)
            },
            {
                "name": "Smartphones",
                "slug": "smartphones",
                "bg": (248, 249, 250),
                "accent": (70, 75, 80)
            },
            {
                "name": "Wearables",
                "slug": "wearables",
                "bg": (243, 244, 246),
                "accent": (230, 80, 50)
            },
        ]

        category_objs = {}
        for cdata in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cdata["slug"],
                defaults={"name": cdata["name"], "is_active": True}
            )
            cat.name = cdata["name"]
            cat.is_active = True
            if not cat.image:
                img_file = create_sample_image(600, 600, cdata["bg"], cdata["name"], cdata["accent"])
                cat.image.save(f"{cdata['slug']}_category.jpg", img_file, save=False)
            cat.save()
            category_objs[cdata["slug"]] = cat
            self.stdout.write(f"Category: {cat.name}")

        # 4. Hero Banners
        banners_data = [
            {
                "title": "Aura Studio Max. Sound without boundaries.",
                "subtitle": "Custom acoustic chamber with spatial calibration and zero audible distortion.",
                "button_text": "Discover Audio",
                "button_link": "/category/audio/",
                "order": 1,
                "bg": (20, 20, 24),
                "accent": (0, 113, 227)
            },
            {
                "title": "AuraBook Ultra. Pure Titanium. Extreme Performance.",
                "subtitle": "High-efficiency silicon delivering unprecedented speed and 22 hours of silent operation.",
                "button_text": "Explore Laptops",
                "button_link": "/category/laptops/",
                "order": 2,
                "bg": (24, 28, 36),
                "accent": (50, 150, 250)
            },
            {
                "title": "Aura Titanium Pro. Sculpted for the future.",
                "subtitle": "Aerospace-grade alloy enclosure, micro-ceramic display, and precision optical sensors.",
                "button_text": "Explore Phones",
                "button_link": "/category/smartphones/",
                "order": 3,
                "bg": (18, 18, 20),
                "accent": (160, 160, 170)
            },
        ]

        for bdata in banners_data:
            banner, created = Banner.objects.get_or_create(
                title=bdata["title"],
                defaults={
                    "subtitle": bdata["subtitle"],
                    "button_text": bdata["button_text"],
                    "button_link": bdata["button_link"],
                    "order": bdata["order"],
                    "is_active": True,
                }
            )
            banner.subtitle = bdata["subtitle"]
            banner.button_text = bdata["button_text"]
            banner.button_link = bdata["button_link"]
            banner.order = bdata["order"]
            banner.is_active = True
            if not banner.image:
                img_file = create_sample_image(1920, 800, bdata["bg"], bdata["title"], bdata["accent"])
                banner.image.save(f"banner_{banner.order}.jpg", img_file, save=False)
            banner.save()
            self.stdout.write(f"Banner: {banner.title}")

        # 5. Products
        products_data = [
            # Laptops
            {
                "name": "AuraBook Ultra 16",
                "slug": "aurabook-ultra-16",
                "category": "laptops",
                "price": 2499.00,
                "is_featured": True,
                "description": (
                    "The ultimate workstation for architects, composers, and computational scientists.\n\n"
                    "Features an all-aluminum thermal architecture, 120Hz Liquid OLED display with 1600 nits peak HDR brightness, "
                    "and 6-speaker spatial audio array."
                ),
                "bg": (238, 240, 245),
                "accent": (0, 113, 227),
            },
            {
                "name": "AuraBook Air 14",
                "slug": "aurabook-air-14",
                "category": "laptops",
                "price": 1299.00,
                "is_featured": True,
                "description": (
                    "Impossibly thin at just 11.2mm, yet astonishingly capable.\n\n"
                    "Fanless silent design engineered for all-day mobility with up to 18 hours of continuous battery endurance."
                ),
                "bg": (245, 245, 247),
                "accent": (100, 110, 125),
            },
            {
                "name": "AuraStudio Display 27",
                "slug": "aurastudio-display-27",
                "category": "laptops",
                "price": 1599.00,
                "is_featured": False,
                "description": (
                    "An expansive 5K Retina workspace with 14 million pixels, nano-texture glass coating, "
                    "integrated 12MP Center Stage camera, and studio-grade 3-mic beamforming array."
                ),
                "bg": (242, 244, 248),
                "accent": (80, 85, 95),
            },

            # Audio
            {
                "name": "Aura Pro Wireless Headphones",
                "slug": "aura-pro-wireless-headphones",
                "category": "audio",
                "price": 449.00,
                "is_featured": True,
                "description": (
                    "Over-ear acoustics engineered from custom biocellulose diaphragms and neodymium motor rings.\n\n"
                    "Dynamic spatial audio with head tracking places sound naturally around you in three-dimensional space."
                ),
                "bg": (242, 242, 245),
                "accent": (30, 30, 32),
            },
            {
                "name": "Aura Pods Spatial Edition",
                "slug": "aura-pods-spatial",
                "category": "audio",
                "price": 249.00,
                "is_featured": True,
                "description": (
                    "Next-level active noise cancellation powered by real-time acoustic sensors measuring noise 48,000 times per second.\n\n"
                    "IP54 sweat and water resistance with MagSafe wireless charging case."
                ),
                "bg": (248, 248, 250),
                "accent": (0, 113, 227),
            },
            {
                "name": "Aura Soundbar Spatial 360",
                "slug": "aura-soundbar-spatial-360",
                "category": "audio",
                "price": 899.00,
                "is_featured": False,
                "description": (
                    "Room-filling high-fidelity cinema sound in a single minimalist unibody aluminum enclosure.\n\n"
                    "Equipped with 11 discrete drivers, upward-firing height channels, and automatic room calibration."
                ),
                "bg": (240, 240, 242),
                "accent": (50, 50, 55),
            },

            # Smartphones
            {
                "name": "Aura Phone Titanium Pro Max",
                "slug": "aura-phone-titanium-pro-max",
                "category": "smartphones",
                "price": 1199.00,
                "is_featured": True,
                "description": (
                    "Forged from Grade 5 titanium, creating our lightest and most durable pro handset ever.\n\n"
                    "Next-gen 3nm processor, periscope optical zoom, and ceramic shielding offering unparalleled drops and scratch resilience."
                ),
                "bg": (235, 237, 240),
                "accent": (70, 75, 85),
            },
            {
                "name": "Aura Phone 16 Standard",
                "slug": "aura-phone-16-standard",
                "category": "smartphones",
                "price": 799.00,
                "is_featured": False,
                "description": (
                    "Vibrant aerospace-grade aluminum chassis with infused glass back.\n\n"
                    "48MP Fusion camera system with 2x optical-quality telephoto and all-day battery life."
                ),
                "bg": (245, 246, 248),
                "accent": (0, 113, 227),
            },
            {
                "name": "Aura MagCharge Wireless Stand",
                "slug": "aura-magcharge-wireless-stand",
                "category": "smartphones",
                "price": 89.00,
                "is_featured": False,
                "description": (
                    "Solid CNC milled anodized aluminum charging dock.\n\n"
                    "Delivers up to 15W high-speed magnetic alignment charging with optimal landscape view angles for StandBy mode."
                ),
                "bg": (244, 244, 246),
                "accent": (90, 95, 105),
            },

            # Wearables
            {
                "name": "Aura Watch Titanium Ultra",
                "slug": "aura-watch-titanium-ultra",
                "category": "wearables",
                "price": 799.00,
                "is_featured": True,
                "description": (
                    "Built for endurance and precision navigation in extreme environments.\n\n"
                    "49mm aerospace titanium case, dual-frequency GPS, 100m water resistance, and up to 72 hours of low-power battery life."
                ),
                "bg": (238, 240, 242),
                "accent": (230, 80, 50),
            },
            {
                "name": "Aura Watch Series 10",
                "slug": "aura-watch-series-10",
                "category": "wearables",
                "price": 399.00,
                "is_featured": False,
                "description": (
                    "Our thinnest smartwatch display ever, offering up to 30% more active screen area.\n\n"
                    "Comprehensive cardiovascular insights, ECG monitoring, sleep apnea detection, and fast charging to 80% in 30 minutes."
                ),
                "bg": (246, 246, 248),
                "accent": (0, 113, 227),
            },
            {
                "name": "Aura Milanese Loop Band",
                "slug": "aura-milanese-loop-band",
                "category": "wearables",
                "price": 99.00,
                "is_featured": False,
                "description": (
                    "A modern interpretation of a design developed in Milan at the end of the 19th century.\n\n"
                    "Woven on specialized Italian machines, the smooth stainless steel mesh wraps fluidly around your wrist."
                ),
                "bg": (242, 243, 245),
                "accent": (140, 140, 150),
            },
        ]

        for pdata in products_data:
            cat = category_objs[pdata["category"]]
            product, created = Product.objects.get_or_create(
                slug=pdata["slug"],
                defaults={
                    "name": pdata["name"],
                    "description": pdata["description"],
                    "price": pdata["price"],
                    "category": cat,
                    "is_active": True,
                    "is_featured": pdata["is_featured"],
                }
            )
            product.name = pdata["name"]
            product.description = pdata["description"]
            product.price = pdata["price"]
            product.category = cat
            product.is_active = True
            product.is_featured = pdata["is_featured"]
            if not product.image:
                img_file = create_sample_image(800, 800, pdata["bg"], pdata["name"], pdata["accent"])
                product.image.save(f"{pdata['slug']}.jpg", img_file, save=False)
            product.save()
            self.stdout.write(f"Product: {product.name} (${product.price})")

        self.stdout.write(self.style.SUCCESS("\nSuccessfully seeded all sample categories, products, banners, and users!"))
        self.stdout.write(self.style.SUCCESS("Credentials for testing:"))
        self.stdout.write(self.style.SUCCESS("  - Superuser:  admin / AdminPass123!"))
        self.stdout.write(self.style.SUCCESS("  - Customer:   customer / CustomerPass123!"))
