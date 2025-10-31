# Railway Deployment - Media Files Setup

## Sorun
Railway'de admin panelinden yüklenen resimler görünmüyor çünkü Railway'in filesystem'i **ephemeral** (geçici) dir. Her deploy sırasında dosyalar silinir.

## Çözüm: Railway Volumes Kullanımı

### 1. Railway Dashboard'da Volume Oluşturma

1. Railway projenizde **Settings** sekmesine gidin
2. **Volumes** bölümüne gidin
3. **Create Volume** butonuna tıklayın
4. Volume adı verin (örn: `media-files`)
5. Mount path: `/data/media` (bu path varsayılan olarak ayarlanmıştır)
6. Size: İhtiyacınıza göre (örn: 1GB)

### 2. Environment Variable (Opsiyonel)

Eğer farklı bir mount path kullanmak isterseniz:
- Railway Dashboard > Settings > Variables
- Yeni variable ekleyin:
  - Key: `RAILWAY_VOLUME_MOUNT_PATH`
  - Value: `/data/media` (veya istediğiniz path)

### 3. Deployment Sonrası

1. Proje deploy edildikten sonra
2. Admin panelinden yeniden resim yükleyin
3. Resimler artık Railway Volume'da kalıcı olarak saklanacak

### 4. Mevcut Resimleri Yükleme

Eğer lokal ortamda `media/` klasöründe resimleriniz varsa:

```bash
# Lokal ortamdan Railway container'a kopyalama
# Railway CLI kullanarak:

railway connect
railway run bash

# Sonra container içinde:
# Mevcut resimleri yüklemek için admin panelini kullanın veya
# direkt olarak volume mount path'e kopyalayın
```

### Alternatif Çözüm: Cloud Storage (AWS S3, Cloudinary)

Eğer daha profesyonel bir çözüm isterseniz, AWS S3 veya Cloudinary gibi cloud storage servisleri kullanabilirsiniz. Bu durumda `django-storages` paketi kullanılmalıdır.

## Not

- Media dosyaları artık `/data/media` path'inde saklanacak
- Bu path kalıcıdır ve deploy'lardan etkilenmez
- Statik dosyalar (CSS, JS) zaten WhiteNoise ile serve ediliyor

