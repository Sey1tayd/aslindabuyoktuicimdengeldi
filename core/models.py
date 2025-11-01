from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """At ekipmanları kategorileri"""
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Açıklama")
    icon = models.CharField(max_length=50, blank=True, verbose_name="İkon")
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name="Kategori Görseli")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['sort_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    """Markalar"""
    name = models.CharField(max_length=100, verbose_name="Marka Adı")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, verbose_name="Logo")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    website = models.URLField(blank=True, verbose_name="Website")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Marka"
        verbose_name_plural = "Markalar"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Ürünler"""
    STOCK_CHOICES = [
        ('in_stock', 'Stokta'),
        ('limited', 'Sınırlı'),
        ('pre_order', 'Ön Sipariş'),
        ('out_of_stock', 'Stokta Yok'),
    ]

    name = models.CharField(max_length=200, verbose_name="Ürün Adı")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Açıklama")
    short_description = models.CharField(max_length=300, blank=True, verbose_name="Kısa Açıklama")
    
    # İlişkiler
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategori")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Marka")
    
    # Fiyat ve Stok
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Eski Fiyat")
    stock_status = models.CharField(max_length=20, choices=STOCK_CHOICES, default='in_stock', verbose_name="Stok Durumu")
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Stok Miktarı")
    
    # Görseller
    main_image = models.ImageField(upload_to='products/', verbose_name="Ana Görsel")
    image_2 = models.ImageField(upload_to='products/', blank=True, verbose_name="İkinci Görsel")
    image_3 = models.ImageField(upload_to='products/', blank=True, verbose_name="Üçüncü Görsel")
    
    # Özellikler
    weight = models.CharField(max_length=50, blank=True, verbose_name="Ağırlık")
    dimensions = models.CharField(max_length=100, blank=True, verbose_name="Boyutlar")
    material = models.CharField(max_length=100, blank=True, verbose_name="Malzeme")
    color = models.CharField(max_length=50, blank=True, verbose_name="Renk")
    size = models.CharField(max_length=50, blank=True, verbose_name="Beden")
    
    # 3D Model
    sketchfab_model_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Sketchfab Model ID",
        help_text="Sketchfab model ID'si (örnek: 07882e7524534be984ae3e7faca25517). Ürün için 3D model göstermek isterseniz bu alanı doldurun."
    )
    
    # Durumlar
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan")
    is_new = models.BooleanField(default=False, verbose_name="Yeni Ürün")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, verbose_name="Meta Başlık")
    meta_description = models.TextField(blank=True, verbose_name="Meta Açıklama")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:product_detail', kwargs={'product_name': self.slug})

    def get_discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return round(((self.old_price - self.price) / self.old_price) * 100)
        return 0
    
    def _extract_sketchfab_model_id(self):
        """Sketchfab model ID'sini çıkar - tam URL veya sadece ID kabul eder"""
        if not self.sketchfab_model_id:
            return None
        
        model_id = self.sketchfab_model_id.strip()
        
        # Eğer tam URL girildiyse, model ID'yi çıkar
        if 'sketchfab.com' in model_id:
            import re
            match = re.search(r'/models/([a-fA-F0-9]+)', model_id)
            if match:
                return match.group(1)
        
        # Zaten sadece model ID girilmişse
        return model_id
    
    @property
    def is_sketchfab(self):
        """Sketchfab modeli mi kontrol et"""
        return bool(self._extract_sketchfab_model_id())
    
    @property
    def get_sketchfab_embed_url(self):
        """Sketchfab embed URL'ini döndür - dokunmatik ve etkileşimli"""
        model_id = self._extract_sketchfab_model_id()
        if model_id:
            params = [
                "autostart=1",
                "preload=1",
                "autospin=0.2",
                "ui_controls=1",
                "ui_theme=dark",
                "transparent=1",
                "camera=0",
                "scrollwheel=1",
                "ui_infos=0",
                "ui_hint=0",
                "ui_stop=0",
                "ui_fullscreen=1",
                "dnt=1"  # izleme azaltma
            ]
            return f"https://sketchfab.com/models/{model_id}/embed?{'&'.join(params)}"
        return None

    def __str__(self):
        return self.name


class HeroSection(models.Model):
    """Ana sayfa kahraman bölümü"""
    title = models.CharField(max_length=200, verbose_name="Başlık")
    subtitle = models.CharField(max_length=300, verbose_name="Alt Başlık")
    image = models.ImageField(upload_to='hero/', verbose_name="Görsel")
    primary_button_text = models.CharField(max_length=100, verbose_name="Birincil Buton Metni")
    primary_button_url = models.CharField(max_length=200, verbose_name="Birincil Buton URL")
    secondary_button_text = models.CharField(max_length=100, verbose_name="İkincil Buton Metni")
    secondary_button_url = models.CharField(max_length=200, verbose_name="İkincil Buton URL")
    tag_text = models.CharField(max_length=100, blank=True, verbose_name="Etiket Metni")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kahraman Bölümü"
        verbose_name_plural = "Kahraman Bölümleri"
        ordering = ['sort_order']

    def __str__(self):
        return self.title


class PromoSection(models.Model):
    """Promosyon bölümleri"""
    title = models.CharField(max_length=200, verbose_name="Başlık")
    description = models.TextField(verbose_name="Açıklama")
    image = models.ImageField(upload_to='promos/', verbose_name="Görsel")
    button_text = models.CharField(max_length=100, verbose_name="Buton Metni")
    button_url = models.CharField(max_length=200, verbose_name="Buton URL")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Promosyon Bölümü"
        verbose_name_plural = "Promosyon Bölümleri"
        ordering = ['sort_order']

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    """Blog yazıları"""
    title = models.CharField(max_length=200, verbose_name="Başlık")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(verbose_name="Özet")
    content = models.TextField(verbose_name="İçerik")
    image = models.ImageField(upload_to='blog/', verbose_name="Görsel")
    category = models.CharField(max_length=100, verbose_name="Kategori")
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog Yazısı"
        verbose_name_plural = "Blog Yazıları"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class ShowcaseModel(models.Model):
    """3D Model showcase - Sketchfab modelleri için"""
    title = models.CharField(max_length=200, verbose_name="Başlık")
    topic = models.CharField(max_length=100, verbose_name="Konu", help_text="Örn: Kalite ve Güven")
    description = models.TextField(verbose_name="Açıklama")
    sketchfab_model_id = models.CharField(
        max_length=100,
        blank=False,
        verbose_name="Sketchfab Model ID",
        help_text="Sketchfab model ID'si ZORUNLUDUR (örnek: 07882e7524534be984ae3e7faca25517). Sadece Model ID'yi veya tam embed URL'yi girebilirsiniz."
    )
    button_text = models.CharField(max_length=100, default="KEŞFET", verbose_name="Buton Metni")
    button_url = models.CharField(max_length=200, default="/", verbose_name="Buton URL")
    badge_text = models.CharField(max_length=100, verbose_name="Rozet Metni", help_text="Örn: KALİTE GÜVENCE")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def _extract_sketchfab_model_id(self):
        """Sketchfab model ID'sini çıkar - tam URL veya sadece ID kabul eder"""
        if not self.sketchfab_model_id:
            return None
        
        model_id = self.sketchfab_model_id.strip()
        
        # Eğer tam URL girildiyse, model ID'yi çıkar
        if 'sketchfab.com' in model_id:
            # https://sketchfab.com/models/4dd909743761457e8d916a142a1e3e95/embed
            # veya
            # https://sketchfab.com/models/4dd909743761457e8d916a142a1e3e95
            import re
            match = re.search(r'/models/([a-fA-F0-9]+)', model_id)
            if match:
                return match.group(1)
        
        # Zaten sadece model ID girilmişse
        return model_id
    
    @property
    def is_sketchfab(self):
        """Sketchfab modeli mi kontrol et"""
        return bool(self._extract_sketchfab_model_id())
    
    @property
    def get_sketchfab_embed_url(self):
        """Sketchfab embed URL'ini döndür - dokunmatik ve etkileşimli"""
        model_id = self._extract_sketchfab_model_id()
        if model_id:
            params = [
                "autostart=1",
                "preload=1",
                "autospin=0.2",
                "ui_controls=1",
                "ui_theme=dark",
                "transparent=1",
                "camera=0",
                "scrollwheel=1",
                "ui_infos=0",
                "ui_hint=0",
                "ui_stop=0",
                "ui_fullscreen=1",
                "dnt=1"  # izleme azaltma
            ]
            return f"https://sketchfab.com/models/{model_id}/embed?{'&'.join(params)}"
        return None
    
    class Meta:
        verbose_name = "Showcase 3D Model"
        verbose_name_plural = "Showcase 3D Modelleri"
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return f"{self.title} - {self.topic}"


class SiteSettings(models.Model):
    """Site ayarları"""
    site_name = models.CharField(max_length=100, default="İhsan At Ekipmanları", verbose_name="Site Adı")
    site_description = models.TextField(default="Pistten ahıra, tüm ekipman tek yerde.", verbose_name="Site Açıklaması")
    logo = models.ImageField(upload_to='site/', blank=True, verbose_name="Logo")
    favicon = models.ImageField(upload_to='site/', blank=True, verbose_name="Favicon")
    
    # İletişim
    email = models.EmailField(default="destek@ihsan.tack", verbose_name="E-posta")
    phone = models.CharField(max_length=20, default="0(850) xxx xx xx", verbose_name="Telefon")
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp")
    
    # Sosyal medya
    instagram_url = models.URLField(blank=True, verbose_name="Instagram URL")
    youtube_url = models.URLField(blank=True, verbose_name="YouTube URL")
    
    # Güven mesajları
    trust_message_1 = models.CharField(max_length=100, default="Hızlı kargo", verbose_name="Güven Mesajı 1")
    trust_message_2 = models.CharField(max_length=100, default="30 gün iade", verbose_name="Güven Mesajı 2")
    trust_message_3 = models.CharField(max_length=100, default="Güvenli ödeme", verbose_name="Güven Mesajı 3")

    class Meta:
        verbose_name = "Site Ayarları"
        verbose_name_plural = "Site Ayarları"

    def __str__(self):
        return self.site_name