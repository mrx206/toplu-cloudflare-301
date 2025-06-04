# toplu-cloudflare-301
Cloudflare üzerinden alan adlarını toplu bir şekilde 301'lemek için kullanılan bi scripttir. **Site listelerindeki domainler alt alta olsun**. 301leme işlemi sıra ile gidecektir. **Yani 1.listedeki 1.domain, 2.listedeki 1.domaine 301lenecektir. 1.listede 95.sıradaki 2.listedeki 95.sırasına 301lenecektir.**

- **cf-301.py dosyasını düzenleyip içerisinde yer alan "CLOUDFLARE_API_KEY" ve "CLOUDFLARE_EMAIL" kısımlarını kendinize göre düzenleyin.**
- **liste1.txt kısmına 301lemek istediğiniz eski domainleri yazın. domain formatı site.com, site2.com şeklinde olsun. www, https gibi kısımlar olmasın sadece domain isimleri yer alsın. sadece(site.com)**
- **liste2.txt kısmında yeni adresinizde www var ise www olarak yazın. yoksa 1.örnekteki gibi sade halde yazın. (site.com, www.site.com)**
- cf-301.py dosyasını çalıştırın ve sonuçlar ekranda görünecektir.
