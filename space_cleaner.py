import pygame
import random
import math

# Pygame başlatma
pygame.init()

# Ekran ayarları
GENISLIK = 800
YUKSEKLIK = 600
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Uzay Savaşçısı")

# Renkler
BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)
KIRMIZI = (255, 0, 0)
SARI = (255, 255, 0)
MAVI = (0, 0, 255)

class SavasUcagi:
    def __init__(self):
        self.genislik = 50
        self.yukseklik = 40
        self.x = GENISLIK // 2
        self.y = YUKSEKLIK - 60
        self.hiz = 7
        self.puan = 0
        self.can = 100
        self.mermiler = []
        
    def ciz(self):
        # Gövde
        pygame.draw.polygon(ekran, MAVI, [
            (self.x, self.y - self.yukseklik//2),
            (self.x - self.genislik//2, self.y + self.yukseklik//2),
            (self.x + self.genislik//2, self.y + self.yukseklik//2)
        ])
        # Kanatlar
        pygame.draw.polygon(ekran, BEYAZ, [
            (self.x - self.genislik//2, self.y),
            (self.x - self.genislik, self.y + self.yukseklik//3),
            (self.x - self.genislik//3, self.y)
        ])
        pygame.draw.polygon(ekran, BEYAZ, [
            (self.x + self.genislik//2, self.y),
            (self.x + self.genislik, self.y + self.yukseklik//3),
            (self.x + self.genislik//3, self.y)
        ])
        
    def hareket(self):
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT] and self.x > self.genislik//2:
            self.x -= self.hiz
        if tuslar[pygame.K_RIGHT] and self.x < GENISLIK - self.genislik//2:
            self.x += self.hiz
            
    def ates_et(self, offset=0):
        mermi = Mermi(self.x + offset, self.y - self.yukseklik//2)
        self.mermiler.append(mermi)

class Mermi:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hiz = 10
        self.boyut = 5
        
    def ciz(self):
        pygame.draw.circle(ekran, SARI, (self.x, self.y), self.boyut)
        
    def hareket(self):
        self.y -= self.hiz

class DusmanGemi:
    TIPLER = {
        'normal': {'can': 1, 'hiz': (2, 4), 'puan': 20, 'renk': KIRMIZI},
        'hizli': {'can': 1, 'hiz': (5, 7), 'puan': 30, 'renk': (255, 165, 0)},  # Turuncu
        'guclu': {'can': 3, 'hiz': (1, 3), 'puan': 50, 'renk': (128, 0, 128)}  # Mor
    }
    
    def __init__(self, tip='normal'):
        self.tip = tip
        self.ozellikler = self.TIPLER[tip]
        self.genislik = 40
        self.yukseklik = 30
        self.x = random.randint(self.genislik, GENISLIK-self.genislik)
        self.y = random.randint(-100, 0)
        self.hiz = random.randint(*self.ozellikler['hiz'])
        self.can = self.ozellikler['can']
        self.vuruldu = False
        self.patlama_sayaci = 0
        
    def hasar_al(self):
        self.can -= 1
        if self.can <= 0:
            self.vuruldu = True
            return True
        return False
        
    def ciz(self):
        if self.vuruldu:
            # Patlama efekti
            pygame.draw.circle(ekran, KIRMIZI, (self.x, self.y), 
                             20 + self.patlama_sayaci)
        else:
            # Düşman gemi (tip'e göre farklı şekiller)
            if self.tip == 'normal':
                pygame.draw.polygon(ekran, self.ozellikler['renk'], [
                    (self.x, self.y + self.yukseklik//2),
                    (self.x - self.genislik//2, self.y - self.yukseklik//2),
                    (self.x + self.genislik//2, self.y - self.yukseklik//2)
                ])
            elif self.tip == 'hizli':
                pygame.draw.polygon(ekran, self.ozellikler['renk'], [
                    (self.x, self.y - self.yukseklik//2),
                    (self.x - self.genislik//2, self.y),
                    (self.x - self.genislik//4, self.y + self.yukseklik//2),
                    (self.x + self.genislik//4, self.y + self.yukseklik//2),
                    (self.x + self.genislik//2, self.y)
                ])
            elif self.tip == 'guclu':
                pygame.draw.rect(ekran, self.ozellikler['renk'],
                               (self.x - self.genislik//2, self.y - self.yukseklik//2,
                                self.genislik, self.yukseklik))
                
    def hareket(self):
        self.y += self.hiz
        if self.y > YUKSEKLIK + self.yukseklik:
            self.y = random.randint(-100, 0)
            self.x = random.randint(self.genislik, GENISLIK-self.genislik)

    def sifirla(self):
        """Düşman gemiyi başlangıç durumuna getirir"""
        self.y = random.randint(-100, 0)
        self.x = random.randint(self.genislik, GENISLIK-self.genislik)
        self.vuruldu = False
        self.patlama_sayaci = 0
        self.can = self.ozellikler['can']  # Canı yenile

class GucArtirici:
    TIPLER = {
        'hiz': {'renk': (0, 255, 255), 'sure': 5},  # Cyan
        'cift_ates': {'renk': (255, 255, 0), 'sure': 7},  # Sarı
        'kalkan': {'renk': (0, 255, 0), 'sure': 4}  # Yeşil
    }
    
    def __init__(self):
        self.tip = random.choice(list(self.TIPLER.keys()))
        self.ozellikler = self.TIPLER[self.tip]
        self.x = random.randint(20, GENISLIK-20)
        self.y = random.randint(-100, 0)
        self.hiz = 2
        self.boyut = 15
        
    def ciz(self):
        pygame.draw.circle(ekran, self.ozellikler['renk'], 
                         (self.x, self.y), self.boyut)
        
    def hareket(self):
        self.y += self.hiz
        return self.y > YUKSEKLIK + self.boyut

def mesafe_hesapla(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def oyunu_baslat():
    ucak = SavasUcagi()
    dusmanlar = []
    guc_artiricilar = []
    aktif_gucler = {'hiz': 0, 'cift_ates': 0, 'kalkan': 0}
    
    # Başlangıç düşmanlarını oluştur
    for _ in range(3):
        dusmanlar.append(DusmanGemi('normal'))
    for _ in range(2):
        dusmanlar.append(DusmanGemi('hizli'))
    dusmanlar.append(DusmanGemi('guclu'))
    
    saat = pygame.time.Clock()
    oyun_zamani = 0
    oyun_devam = True
    
    while oyun_devam and ucak.can > 0:
        oyun_zamani += 1
        
        # Her 10 saniyede bir güç artırıcı oluştur
        if oyun_zamani % 600 == 0:  # 60 FPS × 10 saniye
            guc_artiricilar.append(GucArtirici())
            
        # Aktif güçlerin sürelerini kontrol et
        for guc in list(aktif_gucler.keys()):
            if aktif_gucler[guc] > 0:
                aktif_gucler[guc] -= 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                oyun_devam = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if aktif_gucler['cift_ates'] > 0:
                        # Çift ateş
                        ucak.ates_et(-10)
                        ucak.ates_et(10)
                    else:
                        ucak.ates_et()
        
        # Güç artırıcıları kontrol et
        for guc in guc_artiricilar[:]:
            guc.hareket()
            guc.ciz()
            
            if mesafe_hesapla(ucak.x, ucak.y, guc.x, guc.y) < 30:
                aktif_gucler[guc.tip] = guc.ozellikler['sure'] * 60  # 60 FPS
                guc_artiricilar.remove(guc)
        
        ucak.hareket()
        
        ekran.fill(SIYAH)
        
        # Mermileri hareket ettir ve çiz
        for mermi in ucak.mermiler[:]:
            mermi.hareket()
            mermi.ciz()
            
            # Menzil dışına çıkan mermileri sil
            if mermi.y < 0:
                ucak.mermiler.remove(mermi)
                
            # Mermi-düşman çarpışma kontrolü
            for dusman in dusmanlar:
                if not dusman.vuruldu and mesafe_hesapla(mermi.x, mermi.y, 
                                                        dusman.x, dusman.y) < 30:
                    if dusman.hasar_al():
                        ucak.puan += dusman.ozellikler['puan']
                    if mermi in ucak.mermiler:
                        ucak.mermiler.remove(mermi)
                
        # Düşmanları hareket ettir ve çiz
        for dusman in dusmanlar:
            dusman.hareket()
            dusman.ciz()
            
            if dusman.vuruldu:
                dusman.patlama_sayaci += 1
                if dusman.patlama_sayaci > 10:
                    dusman.sifirla()
            
            # Düşman-oyuncu çarpışma kontrolü
            elif mesafe_hesapla(ucak.x, ucak.y, dusman.x, dusman.y) < 40:
                hasar = 20 if not aktif_gucler['kalkan'] else 10
                ucak.can -= hasar
                dusman.vuruldu = True
        
        ucak.ciz()
        
        # Puan ve can göstergesi
        font = pygame.font.Font(None, 36)
        puan_text = font.render(f'Puan: {ucak.puan}', True, BEYAZ)
        can_text = font.render(f'Can: {ucak.can}', True, BEYAZ)
        ekran.blit(puan_text, (10, 10))
        ekran.blit(can_text, (10, 50))
        
        # Güç göstergelerini çiz
        y_offset = 90
        for guc, sure in aktif_gucler.items():
            if sure > 0:
                guc_text = font.render(f'{guc}: {sure//60}s', True, BEYAZ)
                ekran.blit(guc_text, (10, y_offset))
                y_offset += 30
        
        pygame.display.flip()
        saat.tick(60)
        
    # Oyun sonu ekranı
    if not oyun_devam:
        return
        
    ekran.fill(SIYAH)
    game_over_text = font.render(f'OYUN BİTTİ! Toplam Puan: {ucak.puan}', True, BEYAZ)
    ekran.blit(game_over_text, (GENISLIK//2 - 150, YUKSEKLIK//2))
    pygame.display.flip()
    pygame.time.wait(3000)
    
    pygame.quit()

if __name__ == "__main__":
    oyunu_baslat() 