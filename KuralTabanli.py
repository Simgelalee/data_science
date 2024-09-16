import numpy as np
import pandas as pd
import seaborn as sns

#persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
df = pd.read_csv('persona.csv')
print(df.head())


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

# Kaç unique SOURCE vardır? Frekansları nedir?


df["SOURCE"].nunique()

df['SOURCE'].value_counts()


#Kaç unique PRICE vardır?

df["PRICE"].nunique()

df["PRICE"].unique()



# Hangi PRICE'dan kaçar tane satış gerçekleşmiş?

#1.yol
df['PRICE'].value_counts()
#2.yol
pd.pivot_table(df, index='PRICE', aggfunc='size') # Tüm Veriyi (df) veriyorum.
#3.yol
df.groupby('PRICE').size()


# Hangi ülkeden kaçar tane satış olmuş?

#1.yol
df['COUNTRY'].value_counts()
#2.yol
df.pivot_table(values="PRICE", index='COUNTRY', aggfunc='count')
#3.yol
df.groupby('COUNTRY').size()


# Ülkelere göre satışlardan toplam ne kadar kazanılmış?

df.groupby('COUNTRY')['PRICE'].sum()
df.groupby("COUNTRY").agg({'PRICE': "sum"})
df.groupby('COUNTRY')['PRICE'].agg(["sum"])
df.pivot_table(values="PRICE", index="COUNTRY", aggfunc="sum")

# SOURCE türlerine göre satış sayıları nedir?

df['SOURCE'].value_counts()
df.groupby("SOURCE")["PRICE"].count()

# Ülkelere göre PRICE ortalamaları nedir?

df.pivot_table("PRICE", "COUNTRY", aggfunc="mean")
df.groupby("COUNTRY").agg({"PRICE": "mean"})

# SOURCE'lara göre PRICE ortalamaları nedir?

df.groupby("SOURCE").agg({"PRICE": "mean"})

print("YOL 1:")
df.groupby("SOURCE")["PRICE"].mean()

print("YOL 2:")
df.groupby("SOURCE").agg({"PRICE": "mean"})

print("YOL 3:")
df.pivot_table(values="PRICE", index="SOURCE", aggfunc="mean")

# COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?


df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})

########## COUNTRY-SOURCE - SEX kırılımında PRICE ve  AGE ortalamaları nedir?

df.groupby(['COUNTRY', 'SOURCE', 'SEX']).agg({
    'PRICE': 'mean',
    'AGE': 'mean'
})


###### Görev 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?


df.groupby(['COUNTRY', 'SOURCE', 'SEX','AGE']).agg({'PRICE': 'mean'}).head()


##### Görev 3: Çıktıyı PRICE’a göre sıralayınız.

agg_df = df.groupby(['COUNTRY', 'SOURCE', 'SEX','AGE']).agg({'PRICE': 'mean'}).sort_values("PRICE", ascending = False)
agg_df.head()
##### Görev 4: Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir. Bu isimleri değişken isimlerine çeviriniz.
#1.yol
agg_df["COUNTRY"] = agg_df.index
agg_df.head()
agg_df.drop("COUNTRY", axis=1, inplace=True)


#2.yol
agg_df = agg_df.reset_index()


# Görev 5: Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz

# AGE degiskeni sınıf aralıgı
bins = [0, 18, 23, 30, 40, df["AGE"].max()]

# Sınıf aralıklarına denk gelen tanımlamalar:
labels = ['0_18', '19-23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]


agg_df["age_categorical"] = pd.cut(agg_df["AGE"], bins, labels=labels)
agg_df.head()



#2.Yol
age_bins = [0,18,23,30,40,70]
age_labels = ['0_18', '19_23', '24_30', '31_40', '41_70']
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins=age_bins, labels=age_labels)
agg_df.head()
agg_df["PRICE"].unique()



#Görev 6 : Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
print("YOL 1:")
agg_df["customers_level_based"] = agg_df[['COUNTRY', 'SOURCE', 'SEX', 'age_categorical']].agg(lambda x: '_'.join(x).upper(), axis=1)
agg_df.head()


#yol 2
agg_df["customers_level_based"] = (agg_df["COUNTRY"].astype(str)+"_" + agg_df["SOURCE"].astype(str)+"_" + agg_df["SEX"].astype(str) + "_" + agg_df["AGE"].astype(str) + "_" + agg_df["AGE_CAT"].astype(str)).str.upper()

agg_df.groupby(["customers_level_based"])["PRICE"].mean()
agg_df.head()

#görev 7 Yeni müşterileri (Örnek: USA_ANDROID_MALE_0_18) PRICE’a göre 4 segmente ayırınız

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])


segment_sum = agg_df.groupby("SEGMENT").agg(
    price_mean=("PRICE", "mean"),
    price_max=("PRICE", "max"),
    price_sum=("PRICE", "sum"))
agg_df.head()


#görev 8
#1
agg_df[agg_df["customers_level_based"] == "TUR_ANDROID_FEMALE_31_40"]["PRICE"].mean()
agg_df[agg_df["customers_level_based"] == "FRA_IOS_FEMALE_31_40"]["PRICE"].mean()
#2
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]
agg_df.groupby("SEGMENT").agg({"PRICE": ["mean","max","sum"]})


