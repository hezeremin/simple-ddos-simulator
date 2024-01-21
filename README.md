# DDoS Simulator (ddos-sim)

**DDoS Simulator**, Python tabanlı basit bir araçtır. Bu araç, DDoS saldırılarını simüle etmek amacıyla geliştirilmiştir. Ağ dayanıklılığı testleri ve güvenlik değerlendirmeleri için kullanılabilir.

## Kurulum

Proje, Python dilinde yazılmıştır. Projeyi bilgisayarınıza klonlamak için aşağıdaki komutu kullanabilirsiniz:

git clone https://github.com/hezeremin/simple-ddos-simulator.git

# Kullanım
Proje ana dizininde, terminal veya komut istemcisine şu komutu yazarak DDoS saldırısını başlatabilirsiniz
Komut, sahte IP'ler ve rastgele kullanıcı ajanları kullanarak HTTP GET istekleri göndererek belirli bir hedefe saldırı simüle edecektir.

# Parametreler
fake_ips: Sahte IP sayısı.
target: Hedef IP adresi.
change_data: Port ve IP değişikliği isteniyorsa (E/H).
port: Hedef port numarası (varsayılan: 80).
fake_ip: Sahte IP adresi (varsayılan: rastgele seçilen).
duration: Saldırı süresi (saniye).

# Notlar
**Bu araç, gerçek bir saldırı aracı değildir ve yasalara uygun bir şekilde kullanılmalıdır.**
**Yasal sorumluluklar ve etik kurallara dikkat edilmelidir.**
