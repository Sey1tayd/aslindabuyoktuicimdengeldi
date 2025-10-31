# GLB Dosyalarını Yükleme - Çözüm Rehberi

## Sorun
Railway'in load balancer timeout limiti (30 saniye) nedeniyle admin panelinden 100MB'lık GLB dosyaları yüklenemiyor (502 timeout hatası).

## Önerilen Çözümler

### Çözüm 1: Dosyaları Optimize Etme (EN KOLAY)

GLB dosyalarınızı optimize ederek boyutunu küçültün:

1. **GLTF/GLB Optimizer** kullanın:
   ```bash
   npm install -g gltf-pipeline
   gltf-pipeline -i model.glb -o model_optimized.glb --draco.compressionLevel 10
   ```

2. **Online araçlar**:
   - https://glb-packer.com/optimize
   - https://gltf.report/

3. Optimize edilmiş dosyalar (50MB altı) admin panelinden yüklenecektir.

### Çözüm 2: Admin Panelinde Adım Adım Yükleme

1. **Önce küçük bir test dosyası yükleyin** (1-2MB) - bu çalışıyorsa sistem hazır
2. **Büyük dosyayı parçalara bölün** (mümkünse):
   - Model'i birden fazla parçaya ayırın
   - Her parçayı ayrı ShowcaseModel olarak yükleyin
3. **Veya optimize edilmiş versiyonu yükleyin**

### Çözüm 3: Lokal Ortamdan Migration

Dosyaları lokal ortamınızda hazırlayıp, Railway'e deploy ederken dahil edin:

1. GLB dosyalarınızı `media/showcase/` klasörüne yerleştirin
2. Git'e ekleyin (dikkat: repo boyutu artacak)
3. Railway'e push edin
4. Admin panelinden model bilgilerini girin (dosya zaten var)

**Not**: Bu yöntem repo boyutunu büyütür, sadece birkaç dosya için uygundur.

### Çözüm 4: Alternative Storage (Gelecek İçin)

AWS S3 veya Cloudinary gibi cloud storage kullanarak:
- Dosyalar direkt S3'e yüklenir (Railway timeout'u aşılmış olur)
- `django-storages` paketi gerekir
- Daha profesyonel çözüm ama ek kurulum gerektirir

## Şu An İçin Önerilen

**Çözüm 1 (Optimize Etme)** en pratik ve hızlı çözümdür:
- GLB dosyalarınızı optimize edin
- 50MB altına indirin
- Admin panelinden normal şekilde yükleyin

## Dosya Optimize Etme Araçları

- **gltf-pipeline** (Command line)
- **glTF-Transform** (Node.js)
- **Blender** (3D model editörü - GLB export sırasında optimize seçenekleri)
- **Online optimizers** (yukarıda listelenenler)

