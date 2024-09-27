
###################################################
# PROJE: Rating Product & Sorting Reviews in Amazon
###################################################

###################################################
# İş Problemi
###################################################

# E-ticaretteki en önemli problemlerden bir tanesi ürünlere satış sonrası verilen puanların doğru şekilde hesaplanmasıdır.
# Bu problemin çözümü e-ticaret sitesi için daha fazla müşteri memnuniyeti sağlamak, satıcılar için ürünün öne çıkması ve satın
# alanlar için sorunsuz bir alışveriş deneyimi demektir. Bir diğer problem ise ürünlere verilen yorumların doğru bir şekilde sıralanması
# olarak karşımıza çıkmaktadır. Yanıltıcı yorumların öne çıkması ürünün satışını doğrudan etkileyeceğinden dolayı hem maddi kayıp
# hem de müşteri kaybına neden olacaktır. Bu 2 temel problemin çözümünde e-ticaret sitesi ve satıcılar satışlarını arttırırken müşteriler
# ise satın alma yolculuğunu sorunsuz olarak tamamlayacaktır.

###################################################
# Veri Seti Hikayesi
###################################################

# Amazon ürün verilerini içeren bu veri seti ürün kategorileri ile çeşitli metadataları içermektedir.
# Elektronik kategorisindeki en fazla yorum alan ürünün kullanıcı puanları ve yorumları vardır.

# Değişkenler:
# reviewerID: Kullanıcı ID’si
# asin: Ürün ID’si
# reviewerName: Kullanıcı Adı
# helpful: Faydalı değerlendirme derecesi
# reviewText: Değerlendirme
# overall: Ürün rating’i
# summary: Değerlendirme özeti
# unixReviewTime: Değerlendirme zamanı
# reviewTime: Değerlendirme zamanı Raw
# day_diff: Değerlendirmeden itibaren geçen gün sayısı
# helpful_yes: Değerlendirmenin faydalı bulunma sayısı
# total_vote: Değerlendirmeye verilen oy sayısı

import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

###################################################
# GÖREV 1: Average Rating'i Güncel Yorumlara Göre Hesaplayınız ve Var Olan Average Rating ile Kıyaslayınız.
###################################################

# Paylaşılan veri setinde kullanıcılar bir ürüne puanlar vermiş ve yorumlar yapmıştır.
# Bu görevde amacımız verilen puanları tarihe göre ağırlıklandırarak değerlendirmek.
# İlk ortalama puan ile elde edilecek tarihe göre ağırlıklı puanın karşılaştırılması gerekmektedir.

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

###################################################
# Adım 1: Veri Setini Okutunuz ve Ürünün Ortalama Puanını Hesaplayınız.
###################################################
df = pd.read_csv(r"C:\Users\ASUS\Desktop\Miuul\Measurement hafta 4\ödev\RatingProductSortingReviewsinAmazon-221119-111357\Rating Product&SortingReviewsinAmazon\amazon_review.csv")
df.head()

df["overall"].mean() #4.587589013224822

###################################################
# Adım 2: Tarihe Göre Ağırlıklı Puan Ortalamasını Hesaplayınız.
###################################################
def time_based_weighted_average(df , w1=50 , w2=30 , w3=20): #4.663414280495112

   return   df.loc[df["day_diff"] <= 30, "overall"].mean() * w1/100 + \
            df.loc[(df["day_diff"]) > 30 & (df["day_diff"] <= 90), "overall"].mean() * w2/100 + \
            df.loc[df["day_diff"] > 90, "overall"].mean() * w3/100

time_based_weighted_average(df)

'''df.loc[df["day_diff"] <= 30, "overall"].mean() * 50/100 
Out[17]: 2.371212121212121
df.loc[(df["day_diff"]) > 30 & (df["day_diff"] <= 90), "overall"].mean() * 30/100 
Out[18]: 1.3762767039674464
df.loc[df["day_diff"] > 90, "overall"].mean() * 20/100
Out[19]: 0.9159254553155443
df.loc[df["day_diff"] <= 30, "overall"].mean()
Out[20]: 4.742424242424242
df.loc[(df["day_diff"]) > 30 & (df["day_diff"] <= 90), "overall"].mean()
Out[21]: 4.587589013224822
df.loc[df["day_diff"] > 90, "overall"].mean()
Out[22]: 4.579627276577721'''

df[["helpful"]]
###################################################
# Görev 2: Ürün için Ürün Detay Sayfasında Görüntülenecek 20 Review'i Belirleyiniz.
###################################################

#1.yol:
def score_average_rating(helpful_yes, total_vote):

    if helpful_yes + total_vote == 0:
         return 0
    return helpful_yes / total_vote

df['helpfulness_score'] = df.apply(lambda row: score_average_rating(row['helpful_yes'], row['total_vote']), axis=1)

df.sort_values(by="helpfulness_score",ascending=False).head(20)

#2.yol:
df["helpful_no"] = df["total_vote"] - df["helpful_yes"]

def wilson_lower_bound(up, down, confidence=0.95):
    """
    Wilson Lower Bound Score hesapla

    - Bernoulli parametresi p için hesaplanacak güven aralığının alt sınırı WLB skoru olarak kabul edilir.
    - Hesaplanacak skor ürün sıralaması için kullanılır.
    - Not:
    Eğer skorlar 1-5 arasıdaysa 1-3 negatif, 4-5 pozitif olarak işaretlenir ve bernoulli'ye uygun hale getirilebilir.
    Bu beraberinde bazı problemleri de getirir. Bu sebeple bayesian average rating yapmak gerekir.

    Parameters
    ----------
    up: int
        up count
    down: int
        down count
    confidence: float
        confidence

    Returns
    -------
    wilson score: float

    """
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)

df['wlb_score'] = df.apply(lambda row: wilson_lower_bound(row['helpful_yes'], row['helpful_no']), axis=1)

df.sort_values(by="wlb_score",ascending=False).head(20)
#3.yol

def score_pos_neg_diff(helpful_yes, helpful_no):

    return helpful_yes - helpful_no

df['score_pos_neg_diff'] = df.apply(lambda row: score_pos_neg_diff(row['helpful_yes'], row['helpful_no']), axis=1)

df.sort_values(by="score_pos_neg_diff",ascending=False).head(20)

###################################################
# Adım 1. helpful_no Değişkenini Üretiniz
###################################################
df["helpful_no"] = df["total_vote"] - df["helpful_yes"]

# Not:
# total_vote bir yoruma verilen toplam up-down sayısıdır.
# up, helpful demektir.
# veri setinde helpful_no değişkeni yoktur, var olan değişkenler üzerinden üretilmesi gerekmektedir.


###################################################
# Adım 2. score_pos_neg_diff, score_average_rating ve wilson_lower_bound Skorlarını Hesaplayıp Veriye Ekleyiniz
###################################################

#1.yol:
def score_average_rating(helpful_yes, total_vote):

    if helpful_yes + total_vote == 0:
         return 0
    return helpful_yes / total_vote

df['helpfulness_score'] = df.apply(lambda row: score_average_rating(row['helpful_yes'], row['total_vote']), axis=1)

df.sort_values(by="helpfulness_score",ascending=False).head(20)

#2.yol:
df["helpful_no"] = df["total_vote"] - df["helpful_yes"]

def wilson_lower_bound(up, down, confidence=0.95):
    """
    Wilson Lower Bound Score hesapla

    - Bernoulli parametresi p için hesaplanacak güven aralığının alt sınırı WLB skoru olarak kabul edilir.
    - Hesaplanacak skor ürün sıralaması için kullanılır.
    - Not:
    Eğer skorlar 1-5 arasıdaysa 1-3 negatif, 4-5 pozitif olarak işaretlenir ve bernoulli'ye uygun hale getirilebilir.
    Bu beraberinde bazı problemleri de getirir. Bu sebeple bayesian average rating yapmak gerekir.

    Parameters
    ----------
    up: int
        up count
    down: int
        down count
    confidence: float
        confidence

    Returns
    -------
    wilson score: float

    """
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)

df['wlb_score'] = df.apply(lambda row: wilson_lower_bound(row['helpful_yes'], row['helpful_no']), axis=1)

df.sort_values(by="wlb_score",ascending=False).head(20)
#3.yol

def score_pos_neg_diff(helpful_yes, helpful_no):

    return helpful_yes - helpful_no

df['score_pos_neg_diff'] = df.apply(lambda row: score_pos_neg_diff(row['helpful_yes'], row['helpful_no']), axis=1)

df.sort_values(by="score_pos_neg_diff",ascending=False).head(20)


##################################################
# Adım 3. 20 Yorumu Belirleyiniz ve Sonuçları Yorumlayınız.
###################################################

df.sort_values(by="score_pos_neg_diff",ascending=False).head(20)
df.sort_values(by="wlb_score",ascending=False).head(20)
df.sort_values(by="helpfulness_score",ascending=False).head(20)