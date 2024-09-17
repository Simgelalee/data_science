
###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

###############################################################
# İş Problemi (Business Problem)
###############################################################
# FLO müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.
# Buna yönelik olarak müşterilerin davranışları tanımlanacak ve bu davranış öbeklenmelerine göre gruplar oluşturulacak..

###############################################################
# Veri Seti Hikayesi
###############################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından
# elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi

###############################################################
# GÖREVLER
###############################################################
import pandas as pd
import numpy as np
import datetime as dt

# GÖREV 1: Veriyi Anlama (Data Understanding) ve Hazırlama

           # 1. flo_data_20K.csv verisini okuyunuz.

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 1000)
df_ = pd.read_csv(r"C:\Users\ASUS\Desktop\Miuul\CRM_analytics_hafta_3\FLOMusteriSegmentasyonu-221114-233246\FLOMusteriSegmentasyonu\flo_data_20k.csv")
df = df_.copy()
           # 2. Veri setinde
                     # a. İlk 10 gözlem,
df.head(10)
                     # b. Değişken isimleri,
df.columns
                     # c. Betimsel istatistik,
df.describe()
                     # d. Boş değer,
df.isnull().sum()
df.isna().sum()
                     # e. Değişken tipleri, incelemesi yapınız.
df.dtypes
df.info()


df.shape
df["master_id"].nunique()
           # 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Herbir müşterinin toplam
           # alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.

df["order_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["price_total"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

           # 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
df.dtypes

#1.yol:
date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
df.info()
#2.yol:
date_columns_2 = [col for col in df.columns if 'date' in col]

#3.yol:(?)
df[df.loc[:, df.columns.str.contains("date")]]


           # 5. Alışveriş kanallarındaki müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların dağılımına bakınız.

df["order_channel"].unique()

df.groupby("order_channel").agg({"master_id":"count",
                                 "order_total":"mean",
                                 "price_total":"mean"})

           # 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.

df.loc[:, ["master_id", "price_total"]].sort_values(by="price_total", ascending=False).head(10)


           # 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
df.sort_values("order_total", ascending=False)[:10]

           # 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.

def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

df[df["master_id"] == "00016786-2f5a-11ea-bb80-000d3a38a36f"]

df.loc[df["master_id"] == "00016786-2f5a-11ea-bb80-000d3a38a36f", "master_id"]



# GÖREV 2: RFM Metriklerinin Hesaplanması recency , frequency , monetary

df["last_order_date"].max() # 2021-05-30
df.info()
today_date = dt.datetime(2021,6,1)
df["last_order_date"].dtypes

rfm = df.groupby("master_id").agg({"last_order_date": lambda last_order_date: (today_date - last_order_date.max()).days,
                                   "order_total": lambda order_total: order_total.sum(),
                                   "price_total": lambda price_total: price_total.sum()})
rfm.head()
rfm.columns = ['recency', 'frequency', 'monetary']

# GÖREV 3: RF ve RFM Skorlarının Hesaplanması

rfm["recency_s"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_s"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_s"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])
rfm["RFM_S"] = (rfm['recency_s'].astype(str) + rfm['frequency_s'].astype(str))

# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}
rfm['segment'] = rfm['RFM_S'].replace(seg_map, regex=True)

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

rfm[rfm["segment"] == "cant_loose"].head()

rfm.to_csv("rfm.csv")

# GÖREV 5: Aksiyon zamanı!
           # 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
#1.yol:
rfm.groupby("segment").agg({
    "recency": "mean",
    "frequency": "mean",
    "monetary": "mean"
})
#2.yol:
rfm.groupby("segment")[["recency", "frequency", "monetary"]].mean()

#3.yol:
rfm[["segment","recency","frequency","monetary"]].groupby("segment").apply(lambda col: col.mean())

# 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv ye kaydediniz.


# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
# tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Sadık müşterilerinden(champions,loyal_customers),
# ortalama 250 TL üzeri ve kadın kategorisinden alışveriş yapan kişiler özel olarak iletişim kuralacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına
# yeni_marka_hedef_müşteri_id.cvs olarak kaydediniz.

#1.yol
rfm = pd.merge(rfm, df[["master_id", "interested_in_categories_12"]], on="master_id", how="left")

rfm["category"] = rfm["interested_in_categories_12"] #1.yol

#rfm = rfm.rename(columns={"interested_in_categories_12": "category"}) #2.yol

yeni_marka_hedef_musteri_id = rfm.loc[(rfm["monetary"] > 250) & (rfm["category"].str.contains("KADIN")) & ((rfm["segment"] == "champions") | (rfm["segment"] == "loyal_customers")), ["master_id", "monetary", "category", "segment"]]
yeni_marka_hedef_musteri_id.head(10)

yeni_marka_hedef_musteri_id.to_csv("yeni_marka_hedef_müşteri_id.csv")

#del rfm["interested_in_categories_12"]

rfm.head()



#2.yol
rfm[(rfm['monetary'] > 250) & (rfm['category'] == 'KADIN') & (rfm['segment'].isin(['champions', 'loyal_customers']))]

#3.yol:
rfm.query('monetary > 250 and category == "KADIN" and segment in ["champions", "loyal_customers"]')


#4.yol:
rfm.groupby('segment').filter(lambda x: (x['monetary'] > 250) & (x['category'] == 'KADIN').any())

rfm[(rfm["segment"] == "champions") | (rfm["segment"] == "loyal_customers")]








rfm.head()
# b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşteri olan ama uzun süredir
# alışveriş yapmayan kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor.
# Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
# olarak kaydediniz.

target_segments_customer_ids = rfm[rfm["segment"].isin(["cant_loose","hibernating","new_customers"])]["master_id"]
target_segments_customer_ids.head()
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) & ((df["interested_in_categories_12"].str.contains("ERKEK"))|(df["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]
cust_ids.head()
cust_ids.to_csv("indirim_hedef_müşteri_ids.csv", index=False)

# GÖREV 6: Tüm süreci fonksiyonlaştırınız.

def crm_fonk(dataframe, head=5):

    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

    dataframe["order_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["price_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]

    date_columns = dataframe[dataframe.columns[dataframe.columns.str.contains("date")]].apply(pd.to_datetime)

    # GÖREV 2: RFM Metriklerinin Hesaplanması recency , frequency , monetary

    dataframe["last_order_date"].max()# 2021-05-30

    today_date = dt.datetime(2021,6,1)

    rfm = dataframe.groupby("master_id").agg({"last_order_date": lambda date: (today_date - date.max()).days,
                                       "order_total": lambda order_total: order_total.sum(),
                                       "price_total": lambda price_total: price_total.sum()})
    rfm.head()
    rfm.columns = ['recency', 'frequency', 'monetary']

    # GÖREV 3: RF ve RFM Skorlarının Hesaplanması

    rfm["recency_s"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_s"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_s"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])
    rfm["RFM_S"] = (rfm['recency_s'].astype(str) + rfm['frequency_s'].astype(str))

    # GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması

    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }
    rfm['segment'] = rfm['RFM_S'].replace(seg_map, regex=True)

    rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

    rfm[rfm["segment"] == "cant_loose"].head()

    rfm.to_csv("rfm.csv")


crm_fonk(df)
###############################################################
# GÖREV 1: Veriyi  Hazırlama ve Anlama (Data Understanding)
###############################################################


# 2. Veri setinde
        # a. İlk 10 gözlem,
        # b. Değişken isimleri,
        # c. Boyut,
        # d. Betimsel istatistik,
        # e. Boş değer,
        # f. Değişken tipleri, incelemesi yapınız.



# 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir.
# Herbir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.



# 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.


# df["last_order_date"] = df["last_order_date"].apply(pd.to_datetime)



# 5. Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısı ve toplam harcamaların dağılımına bakınız. 



# 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.




# 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.




# 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.


###############################################################
# GÖREV 2: RFM Metriklerinin Hesaplanması
###############################################################

# Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi



# customer_id, recency, frequnecy ve monetary değerlerinin yer aldığı yeni bir rfm dataframe


###############################################################
# GÖREV 3: RF ve RFM Skorlarının Hesaplanması (Calculating RF and RFM Scores)
###############################################################

#  Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çevrilmesi ve
# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydedilmesi




# recency_score ve frequency_score’u tek bir değişken olarak ifade edilmesi ve RF_SCORE olarak kaydedilmesi


###############################################################
# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması
###############################################################

# Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlama ve  tanımlanan seg_map yardımı ile RF_SCORE'u segmentlere çevirme


###############################################################
# GÖREV 5: Aksiyon zamanı!
###############################################################

# 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.



# 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulunuz ve müşteri id'lerini csv ye kaydediniz.

# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
# tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Bu müşterilerin sadık  ve
# kadın kategorisinden alışveriş yapan kişiler olması planlandı. Müşterilerin id numaralarını csv dosyasına yeni_marka_hedef_müşteri_id.cvs
# olarak kaydediniz.



# b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşterilerden olan ama uzun süredir
# alışveriş yapmayan ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
# olarak kaydediniz.
