###############################################
# Python Alıştırmalar
###############################################

###############################################
# GÖREV 1: Veri yapılarının tipleriniz inceleyiniz.
###############################################

x = 8
type(x)

y = 3.2
type(y)

z = 8j + 18
type(z)

a = "Hello World"
type(a)

b = True
type(b)

c = 23 < 22
type(c)


l = [1, 2, 3, 4,"String",3.2, False]

type(l)

d = {"Name": "Jake",
     "Age": [27,56],
     "Adress": "Downtown"}

type(d)
t = ("Machine Learning", "Data Science")

type(t)

s = {"Python", "Machine Learning", "Data Science","Python"}

type(s)


###############################################
# GÖREV 2: Verilen string ifadenin tüm harflerini büyük harfe çeviriniz. Virgül ve nokta yerine space koyunuz, kelime kelime ayırınız.
###############################################

text = "The goal is to turn data into information, and information into insight."

####


def convert_to_uppercase(string):
    new_text = ""
    for letter in string:
        new_text += letter.upper()
    return new_text



def change_place(string):

    string = string.replace(",", " ")
    string = string.replace(".", " ")
    string = string.split("")

    print(string)

new_text = convert_to_uppercase(text)
change_place(new_text)




###############################################
# GÖREV 3: Verilen liste için aşağıdaki görevleri yapınız.
###############################################

lst = ["D","A","T","A","S","C","I","E","N","C","E"]

# Adım 1: Verilen listenin eleman sayısına bakın.
len(lst)


# Adım 2: Sıfırıncı ve onuncu index'teki elemanları çağırın.
first_index = lst[0]
first_index_2 = lst[-11]

last_index = lst[10]
last_index_2 = lst[-1]

print(f"Sıfırıncı indeks: {first_index}")
print(f"Onuncu indeks: {last_index}")

# Adım 3: Verilen liste üzerinden ["D","A","T","A"] listesi oluşturun.
Data = lst[0 : 4]
print(Data)

# Adım 4: Sekizinci index'teki elemanı silin.
#lst.remove("N")
del lst[8]
print(lst)

# Adım 5: Yeni bir eleman ekleyin.

lst.append("X")
print(lst)

# Adım 6: Sekizinci index'e  "N" elemanını tekrar ekleyin.

lst.insert(8,"N")
print(lst)


###############################################
# GÖREV 4: Verilen sözlük yapısına aşağıdaki adımları uygulayınız.
###############################################

dict = {'Christian': ["America",18],
        'Daisy':["England",12],
        'Antonio':["Spain",22],
        'Dante':["Italy",25]}


# Adım 1: Key değerlerine erişiniz.

dict.keys()

# Adım 2: Value'lara erişiniz.

dict.values()

# Adım 3: Daisy key'ine ait 12 değerini 13 olarak güncelleyiniz.

dict["Daisy"] = ["England", 13]
#dict.update({"Daisy": ["England", 13]})
print(dict)
# Adım 4: Key değeri Ahmet value değeri [Turkey,24] olan yeni bir değer ekleyiniz.

dict.update({"Ahmet": ["Turkey", 24]})
print(dict)


# Adım 5: Antonio'yu dictionary'den siliniz.

# pop() & del

dict.pop("Antonio")
print(dict)
#del dict["Antonio"]

###############################################
# GÖREV 5: Arguman olarak bir liste alan, listenin içerisindeki tek ve çift sayıları ayrı listelere atıyan ve bu listeleri return eden fonskiyon yazınız.
###############################################

l = [2,13,18,93,22]

def separate_odd_even(list):
    odd_list = []
    even_list = []
    for number in list:
        if number % 2 == 0:
            even_list.append(number)
        else:
            odd_list.append(number)

    return odd_list, even_list

odd_list, even_list = separate_odd_even(l)

print(odd_list, even_list)
print(odd_list)
print(even_list)





###############################################
# GÖREV 6: Aşağıda verilen listede mühendislik ve tıp fakülterinde dereceye giren öğrencilerin isimleri bulunmaktadır.
# Sırasıyla ilk üç öğrenci mühendislik fakültesinin başarı sırasını temsil ederken son üç öğrenci de tıp fakültesi öğrenci sırasına aittir.
# Enumarate kullanarak öğrenci derecelerini fakülte özelinde yazdırınız.
###############################################

ogrenciler = ["Ali","Veli","Ayşe","Talat","Zeynep","Ece"]

for index, ogrenci in enumerate(ogrenciler, ):
    if index < 3:
        print(f"Mühendislik Fakültesi {index+1}. öğrenci: {ogrenci}")

    else:
        print(f"Tıp Fakültesi {index - 2}. öğrenci: {ogrenci}")

###############################################
# GÖREV 7: Aşağıda 3 adet liste verilmiştir. Listelerde sırası ile bir dersin kodu, kredisi ve kontenjan bilgileri yer almaktadır. Zip kullanarak ders bilgilerini bastırınız.
###############################################

ders_kodu = ["CMP1005","PSY1001","HUK1005","SEN2204"]
kredi = [3,4,2,4]
kontenjan = [30,75,150,25]

#list(zip(ders_kodu, kredi, kontenjan))
# [('CMP1005', 3, 30),('PSY1001', 4, 75),('HUK1005', 2, 150),('SEN2204', 4, 25)]

for kod , kred , kont in zip(ders_kodu, kredi, kontenjan) :
    print(f"kredi {kred} olan {kod} kodlu dersin kontenjanı {kont} kişidir. ")

###############################################
# GÖREV 8: Aşağıda 2 adet set verilmiştir.
# Sizden istenilen eğer 1. küme 2. kümeyi kapsiyor ise ortak elemanlarını eğer kapsamıyor ise 2. kümenin 1. kümeden farkını yazdıracak fonksiyonu tanımlamanız beklenmektedir.
###############################################

kume1 = set(["data", "python"])
kume2 = set(["data", "function", "qcut", "lambda", "python", "miuul"])

def fonk(kume1, kume2):

    if kume1.issuperset(kume2) == True:
        return kume1.intersection(kume2)
    else:
        return kume2.difference(kume1)

result = fonk(kume1,kume2)

print(result)




