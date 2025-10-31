# Railway - Büyük Dosya Yükleme (GLB 100MB)

## Sorun
100MB'lık GLB dosyaları yüklerken 502 (Gateway Timeout) hatası alınıyor.

## Çözüm

### 1. Gunicorn Timeout Ayarları (Procfile'da)
- `--timeout 300`: Request timeout'u 300 saniye (5 dakika)
- `--limit-request-line 8190`: Request line limit'i artırıldı
- `--limit-request-fields 32768`: Form field limit'i artırıldı
- `--limit-request-field_size 1048576`: Her field için 1MB limit

### 2. Django Settings (settings.py)
- `FILE_UPLOAD_MAX_MEMORY_SIZE = 2.5MB`: Küçük dosyalar memory'de, büyükler disk'e yazılır
- `DATA_UPLOAD_MAX_MEMORY_SIZE = None`: Form data limit'i kaldırıldı

### 3. Railway Environment Variables (Opsiyonel)

Eğer hala sorun yaşıyorsanız, Railway Dashboard'da şu environment variable'ları ekleyin:

- **GUNICORN_TIMEOUT**: `300`
- **GUNICORN_WORKERS**: `2`

### 4. Railway Volume

Büyük dosyalar için Railway Volume kullanın:
- Settings > Volumes
- Mount path: `/data/media`
- Size: En az 2-3GB (100MB x 8 model = 800MB + buffer)

## Notlar

- 100MB'lık dosyalar yüklenirken biraz zaman alabilir (30-60 saniye)
- Upload sırasında sayfayı kapatmayın veya yenilemeyin
- Dosya yükleme başarılı olursa Railway Volume'da `/data/media/showcase/` altında görünecek
- Eğer hala timeout alıyorsanız, dosyayı daha küçük parçalara bölebilir veya optimize edebilirsiniz

