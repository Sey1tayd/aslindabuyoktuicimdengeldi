from django.db.utils import ProgrammingError, OperationalError
from .models import Category


def categories(request):
    """Tüm sayfalarda kategorileri kullanılabilir yap"""
    category_mapping = {
        'At Koşu Ekipmanları': {
            'css_class': 'cat--racing',
            'image': 'kosum-takimi.jpg',
            'slug_map': 'kosum-takimi'
        },
        'Tımar Ekipmanları': {
            'css_class': 'cat--grooming',
            'image': 'timar.jpg',
            'slug_map': 'timar'
        },
        'At Bakım Ekipmanları': {
            'css_class': 'cat--care',
            'image': 'bakim.jpg',
            'slug_map': 'bakim'
        },
        'Nalbant Ekipmanları': {
            'css_class': 'cat--farrier',
            'image': 'nalbant.jpg',
            'slug_map': 'nalbant'
        },
        'Binici Ekipmanları': {
            'css_class': 'cat--rider',
            'image': 'binici.jpg',
            'slug_map': 'binici'
        },
        'Araba ve Fayton Takımı': {
            'css_class': 'cat--carriage',
            'image': 'eyer.jpg',
            'slug_map': 'eyer'
        }
    }
    
    try:
        categories = Category.objects.filter(is_active=True).order_by('sort_order')[:6]
    except (ProgrammingError, OperationalError):
        categories = []
    
    categories_with_mapping = []
    for category in categories:
        mapping = category_mapping.get(category.name, {
            'css_class': 'cat--racing',
            'image': 'kosum-takimi.jpg',
            'slug_map': category.slug if hasattr(category, 'slug') else category.name.lower().replace(' ', '-')
        })
        categories_with_mapping.append({
            'category': category,
            'mapping': mapping
        })
    
    return {
        'categories_with_mapping': categories_with_mapping
    }

