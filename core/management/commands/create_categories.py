from django.core.management.base import BaseCommand
from core.models import Category
import sys


class Command(BaseCommand):
    help = 'Homepage kategorilerini sisteme kaydeder'

    def handle(self, *args, **options):
        # Windows konsol encoding sorununu çöz
        if sys.platform == 'win32':
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

        categories_data = [
            {
                'name': 'At Koşu Ekipmanları',
                'slug': 'kosum-takimi',
                'description': 'At koşu ekipmanları ve aksesuarları',
                'sort_order': 1,
            },
            {
                'name': 'Tımar Ekipmanları',
                'slug': 'timar',
                'description': 'At tımar ekipmanları ve bakım ürünleri',
                'sort_order': 2,
            },
            {
                'name': 'At Bakım Ekipmanları',
                'slug': 'bakim',
                'description': 'At bakım ekipmanları ve ürünleri',
                'sort_order': 3,
            },
            {
                'name': 'Nalbant Ekipmanları',
                'slug': 'nalbant',
                'description': 'Nalbant ekipmanları ve aksesuarları',
                'sort_order': 4,
            },
            {
                'name': 'Binici Ekipmanları',
                'slug': 'binici',
                'description': 'Binici ekipmanları ve aksesuarları',
                'sort_order': 5,
            },
            {
                'name': 'Araba ve Fayton Takımı',
                'slug': 'eyer',
                'description': 'Araba ve fayton takımı ekipmanları',
                'sort_order': 6,
            },
        ]

        created_count = 0
        updated_count = 0

        for cat_data in categories_data:
            category, created = Category.objects.update_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'sort_order': cat_data['sort_order'],
                    'is_active': True,
                }
            )
            
            if created:
                created_count += 1
                print(f'[OK] Kategori olusturuldu: {category.name}')
            else:
                updated_count += 1
                print(f'[UPDATE] Kategori guncellendi: {category.name}')

        print(f'\nToplam: {created_count} yeni kategori olusturuldu, {updated_count} kategori guncellendi.')

