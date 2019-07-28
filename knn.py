# Veriyi biçimlendirmek ve bazı belirli hesaplamalar yapabilmek
# için gerekli kütüphaneler içe aktarılıyor.
import pandas as pd
import numpy as np
import math
import operator

# Eğitim verileri ve test için ayrılmış verilerin bulunduğu,
# dosyaların path'leri kullanım kolaylığı olması için değişkene
# aktarılıyor.
egitim_dosya = './project_data.csv'
test_dosya = './project_data-test.csv'

# KNN Algoritmasının gerçekleştiği ana fonksiyon
# egitim_verileri, içerisinde veri nitelikleri ve target değerleri
# olan eğitim için kullanacağımız verilerdir.
# test_verileri, egitim verileri içerisinden bir kısmını ayırdığımız
# verilerdir. Test verilerine ihtiyaç duymamızın sebebi, Algoritmamızın
# yeni gelen veriler üzerindeki çalışma başarımını ölçmektir.
# gercek_sonuclar ise test için ayırdığımız test_verileri nin gerçekte sahip
# olduğu target değerleridir.


def knn(k, egitim_verileri, test_verileri, gercek_sonuclar, weighted_values):

    test_sonuclar = []  # test için ayırdığımız verilerimizin sonuçlarının
    # ekleneceği dizi

    # test_verileri içerisindeki her bir verinin ait olduğu sınıf bulunuyor...
    for test_veri in test_verileri:
        # sonuc_bul fonksiyonuyla, her bir test_verimizin, eğitim verilerimiz
        # içerisinden en benzer k tanesine göre ait olduğu sınıf bulunuyor.
        # Sınıftan kasıt (target = 0, target = 1) durumudur. (Kalp hastalığı
        # yok, Kalp hastalığı var)
        sonuc = sonuc_bul(test_veri, egitim_verileri, k, weighted_values)
        test_sonuclar.append(sonuc)

    # test verilerimizin Knn Algoritmamızın işlenmesi sonucu elde edilen sonuçlar ile
    # gerçek sonuçlarının karşılaştırılması
    basarim = basarim_hesapla(test_sonuclar, gercek_sonuclar)

    return basarim

# Excel dosyamızdan verilerimiz yükleniyor...


def veri_yukle(path):
    veriler = pd.read_csv(path)
    return veriler

# Yüklenen verileri DataFrame formatından dizi formatına çeviriyoruz.
# Bu fonksiyona gönderilen Heart değeri, target değerinin dahil edilip, edilmeyeceğini
# belirliyor.


def dizi_cevir(DataFrame, Heart):
    dizi = []
    if(Heart):
        for index, satir in DataFrame.iterrows():
                # target niteliği dahil ediliyor...
            dizi_satir = [round(satir[i], 3) for i in range(11)]#14
            dizi.append(dizi_satir)
    else:
        for index, satir in DataFrame.iterrows():
                # target niteliği dahil edilmiyor, 13. niteliğe kadar olan
                # veriler alınıyor.
            dizi_satir = [round(satir[i], 3) for i in range(10)]#13
            dizi.append(dizi_satir)
    return dizi

# Veri setimizde başarım hesabını yapabilmek için test verilerinin
# gerçekte olan değerleri alınıyor.


def gercek_sonuc_yukle(path):
    veriler = pd.read_csv(path)
    # sadece target niteliğinin değerleri alınıyor.
    direction_veri = veriler['target'].values
    return direction_veri

# Bir test verisinin bütün eğitim verilerine olan uzaklıkları hesaplanıyor...


def mesafe_bul(test_veri, egitim_verileri, weighted_values):
    komsu_mesafeler = []
    for egitim_veri in egitim_verileri:
        # test verisinin her bir eğitim verisine olan öklid mesafesi bulunuyor.
        mesafe = oklid_hesapla(test_veri, egitim_veri, weighted_values)
        komsu_mesafeler.append((egitim_veri, mesafe))
    return komsu_mesafeler

# Öklid mesafesi hesaplanıyor...


def oklid_hesapla(veri1, veri2, weighted_values):
    uzunluk = len(veri1)
    mesafe = 0
    for i in range(uzunluk):
        mesafe += pow((veri1[i] - veri2[i]), 2) * weighted_values[i]
    return math.sqrt(mesafe)

# En yakın k tane komşu bulunuyor...
# komsular parametresi, eğitim verilerinin nitelik değerlerini
# ve test_verisine olan uzaklığı içeriyor.


def yakin_komsular_bul(komsular, k):
    yakin_komsular = []
    # komsular dizisinin 1. indisinde mesafeler yer aldığı için,
    # mesafelere göre küçükten büyüğe sıralama yapılıyor.
    komsular.sort(key=operator.itemgetter(1))
    for x in range(k):
        # En yakın k tane komşu alınıyor...
        yakin_komsular.append(komsular[x][0])
    return yakin_komsular

# Seçilen en yakın k tane komşunun hangi sınıfa dahil olduğu bulunarak,
# Bu k tane komşu içerisinde en çok hangi sınıf mevcutsa, test Algoritmamıza
# göre hesaplanmış sınıfı da o sınıf oluyor.


def uygun_sonuc(komsular):
    dict = {}
    for komsu in komsular:
        # en yakın k tane komşu içerisindeki her bir komşunun dahil olduğu
        # sınıf komsu[-1] ile bulunarak sayılıyor.
        if(komsu[-1] in dict):
            dict[komsu[-1]] += 1
        else:
            dict[komsu[-1]] = 1

    # dict sözlüğü, test verimize en yakın k tane veri içerisindeki sınıfların sayısıdır.
    # Sınıfların sayısına göre, dict tersten(büyükten küçüğe) sıralanıyor.
    sort = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
    # En yakın k tane veri içerisinde en çok ait olunan sınıf döndürülüyor...
    return sort[0][0]

# Sonuc_bul fonksiyonuyla test_verisinin, eğitim_verilerine göre uzaklıkları hesaplanarak
# En benzer k tane veriye göre sınıfı bulunuyor.
# Eğitim verilerinin sonuç değerini de içerdiğini unutmayın.
# Eğitim verilerinin dahil olduğu sınıflara göre test_verisinin sınıfı
# belirlenir.


def sonuc_bul(test_veri, egitim_verileri, k, weighted_values):
    komsular = mesafe_bul(test_veri, egitim_verileri, weighted_values)
    yakin_komsular = yakin_komsular_bul(komsular, k)
    sonuc = uygun_sonuc(yakin_komsular)
    return sonuc

# Test verilerimize KNN Algoritmamızın uygulanmasıyla elde edilen sonuçlar ile
# test verilerimizin gerçek değerleri karşılaştırılarak, Algoritmamızın ne oranda
# başarılı çalıştığı hesaplanıyor.


def basarim_hesapla(test, gercek):
    length = len(test)
    basarim = 0
    for i in range(length):
        if(test[i] == gercek[i]):
            basarim += 1

    basarim = (basarim / float(length)) * 100.0

    return basarim

# MAX-MIN normalleştirme işlemi yapılıyor. Veri hazırlama aşamasında
# bu normalleştirme türüne değinmiştik.


def normalization(veri):
    for i in range(len(veri[0])):
        max = veri[0][i]
        min = veri[0][i]
        for j in range(len(veri)):
            if(veri[j][i] > max):
                max = veri[j][i]
            elif(veri[j][i] < min):
                min = veri[j][i]
        for j in range(len(veri)):
            veri[j][i] = (veri[j][i] - min) / (max - min)
    return veri

def find_optimized_weighted(k, egitim_dizi, test_dizi, gercek_sonuclar):
	sutun_sayi = 13
	basarim = []
	weighted_values = []
	for i in range(sutun_sayi):
		weighted_values.append(1)
	for i in range(sutun_sayi):
		weighted_values[i] = 10
		basarim.append(knn(k, egitim_dizi, test_dizi, gercek_sonuclar, weighted_values))
		weighted_values[i] = 1
	max_value = max(basarim)
	min_value = min(basarim)
	for i in range(sutun_sayi):
		weighted_values[i] = (basarim[i] - min_value) / max_value
	print(weighted_values)
	return weighted_values

def main():
    # Test verimiz excel dosyasından yükleniyor...
    test_verileri = veri_yukle(test_dosya)
    # DataFrame olarak elde ettiğimiz verilerimizi
    test_dizi = dizi_cevir(test_verileri, Heart=False)
    # Kolaylıkla işleyebilmek için dizi formatına çeviriyoruz.

    # Eğitim verileri, excel dosyasından yükleniyor...
    egitim_verileri = veri_yukle(egitim_dosya)
    # Verileri kolayca işleyebilmek için dizi formatına çeviriyoruz.
    egitim_dizi = dizi_cevir(egitim_verileri, Heart=True)

    # Eğitim verimizde tutarlılık ve dengeyi sağlayabilmek için normalization
    # uyguluyoruz.
    normalization(egitim_dizi)
    # Test verimizde tutarlılık ve dengeyi sağlayabilmek için normalization
    # uyguluyoruz.
    normalization(test_dizi)

    # Başarım hesabını yapabilmek için test verilerinin gerçek sonuç
    # değerlerini yüklüyoruz.
    gercek_sonuclar = gercek_sonuc_yukle(test_dosya)

    weighted_values = find_optimized_weighted(5, egitim_dizi, test_dizi, gercek_sonuclar)
    
    basarim = knn(5, egitim_dizi, test_dizi, gercek_sonuclar, weighted_values)

    print(f"Başarım Oranı : {basarim}")
    # eğitim aşamasında kaç tane benzer verinin dikkate alınması gerektiğini
    # k değeri ile belirtiyoruz. k = 5 seçildi. En yakın 5 veri dikkate alınacak.
    # Niteliklerine göre hangi sınıfa dahil olduklarını bulacağımız
    # test_verisi, ve bu verilerin dahil oldukları sınıfları bulmak için benzerlik
    # hesabında kullandığımız egitim_verisi parametre olarak gönderilmektedir.
    # Bu değerlerin yanısıra test_verilerinin Algoritmamıza göre başarımının ölçülmesi
    # için bu verilerin gerçek değerleri gönderilmektedir.


if __name__ == "__main__":
    main()
