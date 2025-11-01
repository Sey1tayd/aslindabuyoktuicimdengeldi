# Sketchfab Model Ekleme Rehberi - Admin Panel

## Admin Panelinden Sketchfab 3D Model Nasıl Eklenir?

### 1. Admin Paneline Giriş
1. Django admin paneline giriş yapın: `http://yourdomain.com/admin/`
2. Kullanıcı adı ve şifrenizle giriş yapın

### 2. Showcase Modelleri Bölümüne Git
1. Sol menüden **"Showcase 3D Modelleri"** (Showcase Models) bölümüne tıklayın
2. **"+ Add Showcase 3D Model"** butonuna tıklayın

### 3. Model Bilgilerini Doldur

#### Temel Bilgiler
- **Başlık**: Model için başlık (örnek: "ÖZEL KOLEKSİYON")
- **Konu**: Konu başlığı (örnek: "Kalite ve Güven")
- **Açıklama**: Model hakkında açıklama metni

#### 3D Model Bölümü - Sketchfab Kullanımı

**Sketchfab Model ID'yi Ekleyin:**
1. **"Sketchfab Model ID"** alanına Sketchfab model ID'sini girin
   - Örnek: `07882e7524534be984ae3e7faca25517`
   - Model ID'yi nasıl bulacağız? Aşağıya bakın ⬇️

2. **Model URL** ve **Model Dosyası** alanlarını boş bırakın (Sketchfab kullanıyorsanız)

**Sketchfab Model ID Nasıl Bulunur?**

1. Sketchfab.com'a gidin: https://sketchfab.com
2. Modelinizi seçin veya paylaşmak istediğiniz modeli bulun
3. Model sayfasında **"Share"** butonuna tıklayın
4. **"Embed"** sekmesine geçin
5. Embed kodunda şu şekilde bir URL göreceksiniz:
   ```
   https://sketchfab.com/models/07882e7524534be984ae3e7faca25517/embed
   ```
6. URL'deki model ID'sini kopyalayın: `07882e7524534be984ae3e7faca25517`

**Alternatif Yol:**
- Model URL'sinden direkt olarak: 
  - Model URL: `https://sketchfab.com/3d-models/model-07882e7524534be984ae3e7faca25517`
  - Model ID: `07882e7524534be984ae3e7faca25517` (URL'deki son kısım)

#### Buton Ayarları
- **Buton Metni**: Buton üzerinde görünecek metin (varsayılan: "KEŞFET")
- **Buton URL**: Butona tıklandığında gidilecek URL (örnek: `/products/`)

#### Görünüm Ayarları
- **Rozet Metni**: Model üzerinde görünecek rozet metni (örnek: "KALİTE GÜVENCE")
- **Aktif**: Model aktif mi? (✓ işaretli olmalı)
- **Sıralama**: Carousel'de görünme sırası (0 = ilk, 1 = ikinci, vb.)

### 4. Kaydet
**"SAVE"** butonuna tıklayın

### 5. Sonuç
Model artık ana sayfadaki carousel'de Sketchfab üzerinden gösterilecek!

---

## Örnek Model Ekleme

```
Başlık: ÖZEL KOLEKSİYON
Konu: Kalite ve Güven
Açıklama: At ekipmanları ve koşum takımları konusunda yılların deneyimi ile kaliteli ürünler sunuyoruz.

Sketchfab Model ID: 07882e7524534be984ae3e7faca25517
Model URL: (BOŞ BIRAKIN)
Model Dosyası: (BOŞ BIRAKIN)

Buton Metni: KEŞFET
Buton URL: /

Rozet Metni: KALİTE GÜVENCE
Aktif: ✓
Sıralama: 0
```

---

## Önemli Notlar

1. **Öncelik Sırası:**
   - Sketchfab Model ID varsa → Sketchfab kullanılır
   - Yoksa Model URL varsa → CDN/URL kullanılır
   - Yoksa Model Dosyası varsa → Lokal dosya kullanılır

2. **Sketchfab Kullanırken:**
   - Model URL ve Model Dosyası alanlarını boş bırakın
   - Sadece Sketchfab Model ID'yi doldurun

3. **Birden Fazla Model:**
   - Her model için ayrı bir kayıt oluşturun
   - Sıralama numarasına göre carousel'de sırayla görünür

4. **Aktif/Pasif:**
   - Aktif olmayan modeller carousel'de görünmez

---

## Sorun Giderme

**Model görünmüyor mu?**
- "Aktif" checkbox'ının işaretli olduğundan emin olun
- Sketchfab Model ID'nin doğru olduğundan emin olun
- Sayfayı yenileyin (Ctrl+F5)

**Model ID bulamıyorum:**
- Sketchfab model sayfasında "Share" → "Embed" sekmesine bakın
- URL'deki model ID'sini kopyalayın

