import requests
import json

# Cloudflare API bilgileri
CLOUDFLARE_API_KEY = 'api buraya yazılacak'
CLOUDFLARE_EMAIL = 'mail adresi buraya yazılacak'

# 1. ve 2. liste dosyaları
list1 = "liste1.txt"
list2 = "liste2.txt"
output_file = "redirects_log.txt"
error_file = "kontrolet.txt"

# HTTP başlıkları
headers = {
    "X-Auth-Key": CLOUDFLARE_API_KEY,
    "X-Auth-Email": CLOUDFLARE_EMAIL,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def get_zone_id(domain):
    # Zone ID'yi almak için Cloudflare API'sini kullanarak sorgu yap
    response = requests.get("https://api.cloudflare.com/client/v4/zones", headers=headers, params={"name": domain})
    if response.status_code == 200:
        result = response.json()
        if result['result']:
            return result['result'][0]['id']
    else:
        print(f"Zone ID alınamadı: {domain}, Hata: {response.content}")
        log_error(domain)
    return None

def create_redirect_rule(old_url, new_url):
    return {
        "targets": [
            {"target": "url", "constraint": {"operator": "matches", "value": old_url}}
        ],
        "actions": [
            {"id": "forwarding_url", "value": {"url": new_url, "status_code": 301}}
        ],
        "priority": 1,
        "status": "active"
    }

def add_page_rule(zone_id, rule_data):
    cloudflare_page_rules_endpoint = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/pagerules"
    response = requests.post(cloudflare_page_rules_endpoint, headers=headers, json=rule_data)
    if response.status_code in [200, 201]:
        print(f"Page rule added successfully: {rule_data['targets'][0]['constraint']['value']}")
    else:
        print(f"Failed to add page rule: {response.content}")
        print(f"Error Details: {response.json().get('messages', [])}")
        log_error(rule_data['targets'][0]['constraint']['value'])

def log_redirect(old_domain, new_domain):
    with open(output_file, 'a') as log_file:
        log_file.write(f"{old_domain} || {new_domain}\n")

def log_error(domain):
    with open(error_file, 'a') as error_log:
        error_log.write(f"{domain}\n")

def main():
    try:
        # 1. ve 2. liste dosyalarını oku
        with open(list1, 'r') as file1, open(list2, 'r') as file2:
            domains1 = [line.strip() for line in file1.readlines()]
            domains2 = [line.strip() for line in file2.readlines()]

        # Listelerin uzunluğunu kontrol et
        if len(domains1) != len(domains2):
            print("Listeler eşit uzunlukta olmalı.")
            return

        # Her domain için yönlendirme kurallarını oluştur
        for old_domain, new_domain in zip(domains1, domains2):
            zone_id = get_zone_id(old_domain)
            if not zone_id:
                log_error(old_domain)
                continue

            # www'lu ve www'suz yönlendirmeler için kurallar oluştur
            rule_non_www = create_redirect_rule(f"{old_domain}/*", f"https://{new_domain}/$1")
            rule_www = create_redirect_rule(f"www.{old_domain}/*", f"https://{new_domain}/$1")

            # Cloudflare'a yönlendirme kurallarını ekle
            add_page_rule(zone_id, rule_non_www)
            add_page_rule(zone_id, rule_www)

            # Yönlendirme işlemini log dosyasına yaz
            log_redirect(old_domain, new_domain)

    except FileNotFoundError as e:
        print(f"Dosya bulunamadı: {e}")
        log_error(str(e))
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        log_error(str(e))

if __name__ == "__main__":
    main()
