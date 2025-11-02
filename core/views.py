import os
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import logout
from .models import Category, Product, ShowcaseModel


def _get_products_by_category():
    """Kategorilere göre ürün dosyalarını getir - helper fonksiyon"""
    # Ürün dosyalarını kategorilere göre grupla
    category_products = {}
    
    static_root = getattr(settings, 'STATIC_ROOT', None)
    if static_root:
        products_dir = os.path.join(static_root, 'images', 'New folder')
    else:
        products_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'New folder')
    
    if not os.path.exists(products_dir):
        return category_products
    
    all_files = [f for f in os.listdir(products_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    category_keywords = {
        'eyer': ['araba', 'hamut', 'fayton', 'takimi'],
        'kosum-takimi': ['gem', 'getir', 'kolon', 'uzengi', 'dizgin', 'baslik', 'yular', 'martingal', 'gogusluk', 'araka', 'pert', 'tokatli', 'lastikli', 'ithal', 'yerli', 'dortlu', 'uclu', 'zincirli', 'capraz', 'v_alinsalik', 'burunsalik', 'metal_islemeli', 'rugan', 'zincir_islemeli'],
        'timar': ['firca', 'kil', 'tarak', 'gebre', 'kasagi', 'maya', 'bicagi', 'temizleme', 'tuy', 'toplayici', 'plastik_firca', 'kil_firca', 'fircali', 'ahsap', 'plastik_kasagi'],
        'bakim': ['bandaj', 'yele', 'blanket', 'ter', 'maskesi', 'absorbine', 'red_cell', 'elite', 'electroltyle', 'animalintex', 'cool_cast', 'powerflex', 'polar', 'at_maskesi', 'tam_boy', 'yarim_boy', 'ter_ve_su'],
        'nalbant': ['nal', 'civi', 'cekm', 'pensesi', 'kerpeten', 'dovme', 'nalbant', 'acik_nal', 'kapali_nal'],
        'binici': ['eyer', 'eldiven', 'togu', 'yelegi', 'chaps', 'mahmuz', 'binici', 'suvari', 'western', 'avrupa', 'alman', 'endurance', 'pony', 'konfor', 'idman', 'yaprak', 'pelus', 'uzengi_kayisi', 'krom_uzengi', 'plastik_uzengi', 'kazan_uzengi']
    }
    
    matched_files_all = set()
    for cat_slug, keywords in category_keywords.items():
        matched_files = [
            file for file in all_files 
            if file not in matched_files_all 
            and any(keyword.lower() in file.lower() for keyword in keywords)
        ]
        for file in matched_files:
            matched_files_all.add(file)
        category_products[cat_slug] = sorted(matched_files)
    
    unmatched = [f for f in all_files if f not in matched_files_all]
    if unmatched:
        category_products['diger'] = sorted(unmatched)
    
    return category_products


def home(request):
    """Ana sayfa"""
    showcase_models = ShowcaseModel.objects.filter(is_active=True).order_by('sort_order')[:8]
    
    # Kategori mapping: CSS class ve görsel dosya adları
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
    
    categories = Category.objects.filter(is_active=True).order_by('sort_order')[:6]
    
    # Kategorilere mapping bilgisini ekle
    categories_with_mapping = []
    for category in categories:
        mapping = category_mapping.get(category.name, {
            'css_class': 'cat--racing',
            'image': 'kosum-takimi.jpg',
            'slug_map': category.slug if hasattr(category, 'slug') else category.name.lower().replace(' ', '-')
        })
        # Eğer kategori modelinde image varsa onu kullan, yoksa fallback static dosya kullan
        if category.image:
            mapping['image'] = None  # Template'te category.image.url kullanılacak
            mapping['use_media_image'] = True
        else:
            mapping['use_media_image'] = False
        categories_with_mapping.append({
            'category': category,
            'mapping': mapping
        })
    
    category_products = _get_products_by_category()
    
    # Kategori bazında ürün listeleri oluştur (path'lerle birlikte)
    category_with_products = {}
    for cat_data in categories_with_mapping:
        category = cat_data['category']
        mapped_slug = cat_data['mapping']['slug_map']
        
        products = category_products.get(mapped_slug, [])
        # Her ürün için static path oluştur
        # Django static tag otomatik olarak boşlukları encode eder, bu yüzden normal path kullan
        products_with_paths = [{'name': p, 'path': f'images/New folder/{p}'} for p in products]
        category_with_products[category.name] = products_with_paths
    
    # New Arrivals için rastgele ürün seç (path'lerle birlikte)
    all_products = []
    for products in category_products.values():
        all_products.extend(products)
    
    # Eğer ürün varsa rastgele seç
    if all_products:
        random.shuffle(all_products)
        new_arrivals_files = all_products[:4] if len(all_products) >= 4 else all_products
        # Path'lerle birlikte hazırla
        new_arrivals = [{'name': p, 'path': f'images/New folder/{p}'} for p in new_arrivals_files]
    else:
        new_arrivals = []
    
    # Öne çıkan ürünler - static dosyalardan rastgele 10-15 ürün
    all_products_for_featured = []
    for products in category_products.values():
        all_products_for_featured.extend(products)
    
    if all_products_for_featured:
        random.shuffle(all_products_for_featured)
        featured_count = min(15, len(all_products_for_featured))
        featured_products_files = all_products_for_featured[:featured_count]
        featured_products_static = [{'name': p, 'path': f'images/New folder/{p}'} for p in featured_products_files]
    else:
        featured_products_static = []
    
    context = {
        'showcase_models': showcase_models,
        'categories': categories,
        'categories_with_mapping': categories_with_mapping,
        'category_mapping': category_mapping,
        'category_with_products': category_with_products,
        'new_arrivals_files': new_arrivals,
        'featured_products_static': featured_products_static,
    }
    
    return render(request, 'core/home.html', context)


def category_list(request):
    """Kategori listesi"""
    categories = Category.objects.filter(is_active=True).order_by('sort_order', 'name')
    return render(request, 'core/category_list.html', {'categories': categories})


def category_detail(request, slug):
    """Kategori detay sayfası - static dosyalardan ürünleri göster"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    # Kategori adına göre slug bul
    category_slug_map = {
        'At Koşu Ekipmanları': 'kosum-takimi',
        'Tımar Ekipmanları': 'timar',
        'At Bakım Ekipmanları': 'bakim',
        'Nalbant Ekipmanları': 'nalbant',
        'Binici Ekipmanları': 'binici',
        'Araba ve Fayton Takımı': 'eyer'
    }
    
    mapped_slug = category_slug_map.get(category.name, slug)
    category_products = _get_products_by_category()
    product_files = category_products.get(mapped_slug, [])
    
    # Ürünleri path'lerle birlikte hazırla
    products_with_paths = [{'name': p, 'path': f'images/New folder/{p}'} for p in product_files]
    
    # Sayfalama
    paginator = Paginator(products_with_paths, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': products_page,
        'products_count': len(product_files),
    }
    return render(request, 'core/category_detail.html', context)


def product_list(request):
    """Ürün listesi - static dosyalardan tüm ürünleri göster"""
    category_products = _get_products_by_category()
    
    # Tüm ürünleri birleştir
    all_products = []
    for products in category_products.values():
        all_products.extend(products)
    
    # Kategori filtresi
    category_filter = request.GET.get('category')
    if category_filter:
        category_obj = Category.objects.filter(slug=category_filter, is_active=True).first()
        if category_obj:
            category_name_map = {
                'At Koşu Ekipmanları': 'kosum-takimi',
                'Tımar Ekipmanları': 'timar',
                'At Bakım Ekipmanları': 'bakim',
                'Nalbant Ekipmanları': 'nalbant',
                'Binici Ekipmanları': 'binici',
                'Araba ve Fayton Takımı': 'eyer'
            }
            mapped_slug = category_name_map.get(category_obj.name)
            if mapped_slug and mapped_slug in category_products:
                all_products = category_products[mapped_slug]
        else:
            category_slug_map = {
                'at-kosu-ekipmanlari': 'kosum-takimi',
                'timar-ekipmanlari': 'timar',
                'at-bakim-ekipmanlari': 'bakim',
                'nalbant-ekipmanlari': 'nalbant',
                'binici-ekipmanlari': 'binici',
                'araba-ve-fayton-takimi': 'eyer'
            }
            mapped_slug = category_slug_map.get(category_filter, category_filter)
            if mapped_slug in category_products:
                all_products = category_products[mapped_slug]
    
    # Arama filtresi
    search_query = request.GET.get('search', '').strip()
    if search_query:
        search_lower = search_query.lower()
        all_products = [p for p in all_products if search_lower in p.lower()]
    
    # Ürünleri path'lerle birlikte hazırla ve Product objelerini de eşleştir
    products_with_data = []
    for p in sorted(all_products):
        product_data = {
            'name': p,
            'path': f'images/New folder/{p}',
            'db_product': None
        }
        # Product modelinde bu ürün var mı kontrol et (Sketchfab için)
        product_display_name = p.rsplit('.', 1)[0] if '.' in p else p
        product_slug_candidate = slugify(product_display_name)
        db_product = Product.objects.filter(slug=product_slug_candidate, is_active=True).first()
        if not db_product:
            db_product = Product.objects.filter(name__icontains=product_display_name, is_active=True).first()
        if db_product:
            product_data['db_product'] = db_product
        products_with_data.append(product_data)
    
    paginator = Paginator(products_with_data, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True).order_by('name')
    
    context = {
        'products': products_page,
        'categories': categories,
        'current_category': category_filter,
        'search_query': search_query,
        'products_count': len(products_with_data),
    }
    return render(request, 'core/product_list.html', context)


def product_detail(request, product_name):
    """Ürün detay sayfası - static dosyalardan"""
    from urllib.parse import unquote
    from django.http import Http404
    
    # URL decode et
    product_file_name = unquote(product_name)
    
    # Dosya adını kontrol et
    if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
        products_dir = os.path.join(settings.STATIC_ROOT, 'images', 'New folder')
    else:
        products_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'New folder')
    
    product_path = os.path.join(products_dir, product_file_name)
    
    # Dosya var mı kontrol et
    if not os.path.exists(product_path) or not product_file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        raise Http404("Ürün bulunamadı")
    
    # Ürün adını dosya adından çıkar (uzantıyı kaldır)
    if "." in product_file_name:
        product_display_name = product_file_name.rsplit('.', 1)[0]
    else:
        product_display_name = product_file_name
    
    # Kategori bul
    category_products = _get_products_by_category()
    product_category_slug = None
    product_category = None
    
    for cat_slug, products in category_products.items():
        if product_file_name in products:
            product_category_slug = cat_slug
            product_category = Category.objects.filter(slug=cat_slug, is_active=True).first()
            break
    
    # İlgili ürünler - aynı kategoriden
    related_products = []
    if product_category_slug and product_category_slug in category_products:
        cat_products = category_products[product_category_slug]
        # Aynı kategoriden farklı ürünleri al
        related_files = [p for p in cat_products if p != product_file_name][:4]
        related_products = [{'name': p, 'path': f'images/New folder/{p}'} for p in related_files]
    
    # Product modelinde bu ürün var mı kontrol et (Sketchfab için)
    product_slug_candidate = slugify(product_display_name)
    db_product = Product.objects.filter(slug=product_slug_candidate, is_active=True).first()
    if not db_product:
        db_product = Product.objects.filter(name__icontains=product_display_name, is_active=True).first()
    
    context = {
        'product': {
            'name': product_display_name,
            'file_name': product_file_name,
            'path': f'images/New folder/{product_file_name}',
            'category': product_category,
        },
        'db_product': db_product,  # Database'deki Product objesi (Sketchfab için)
        'related_products': related_products,
    }
    return render(request, 'core/product_detail.html', context)


def blog_list(request):
    """Blog listesi"""
    posts = BlogPost.objects.filter(is_active=True).order_by('-created_at')
    
    # Sayfalama
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, 'core/blog_list.html', {'posts': posts})


def blog_detail(request, slug):
    """Blog detay sayfası"""
    post = get_object_or_404(BlogPost, slug=slug, is_active=True)
    
    # İlgili yazılar
    related_posts = BlogPost.objects.filter(
        category=post.category,
        is_active=True
    ).exclude(id=post.id).order_by('-created_at')[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'core/blog_detail.html', context)


def search_suggestions(request):
    """Arama önerileri AJAX"""
    query = request.GET.get('q', '')
    suggestions = []
    
    if len(query) >= 2:
        # Ürün önerileri
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query)
        ).filter(is_active=True)[:5]
        
        suggestions = [{
            'name': product.name,
            'url': product.get_absolute_url(),
            'type': 'Ürün'
        } for product in products]
        
        # Kategori önerileri
        categories = Category.objects.filter(
            name__icontains=query
        ).filter(is_active=True)[:3]
        
        category_suggestions = [{
            'name': category.name,
            'url': f'/kategori/{category.slug}/',
            'type': 'Kategori'
        } for category in categories]
        
        suggestions.extend(category_suggestions)
    
    return JsonResponse({'suggestions': suggestions})


def logout_view(request):
    """Çıkış yap"""
    logout(request)
    return redirect('core:home')