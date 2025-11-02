from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('kategoriler/', views.category_list, name='category_list'),
    path('kategori/<slug:slug>/', views.category_detail, name='category_detail'),
    path('urunler/', views.product_list, name='product_list'),
    path('urun/<str:product_name>/', views.product_detail, name='product_detail'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('api/search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('cikis/', views.logout_view, name='logout'),
]
