

##################################################
# Pandas Alıştırmalar
##################################################

import numpy as np
import seaborn as sns
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

#########################################
# Görev 1: Seaborn kütüphanesi içerisinden Titanic veri setini tanımlayınız.
#########################################
df = sns.load_dataset("titanic")
df.head()
#########################################
# Görev 2: Yukarıda tanımlanan Titanic veri setindeki kadın ve erkek yolcuların sayısını bulunuz.
#########################################

df["sex"].value_counts()


#########################################
# Görev 3: Her bir sutuna ait unique değerlerin sayısını bulunuz.
#########################################

unique_counts = df.nunique()

#########################################
# Görev 4: pclass değişkeninin unique değerleri bulunuz.
#########################################

pclass_unique = df["pclass"].unique()


#########################################
# Görev 5:  pclass ve parch değişkenlerinin unique değerlerinin sayısını bulunuz.
#########################################

pclass_counts = df["pclass"].nunique()
parch_counts = df["parch"].nunique()

df[["pclass","parch"]].nunique()

["pclass", "parch"]
df[degisken].nunique()
#########################################
# Görev 6: embarked değişkeninin tipini kontrol ediniz. Tipini category olarak değiştiriniz. Tekrar tipini kontrol ediniz.
#########################################

df["embarked"].dtype
df['embarked'] = df['embarked'].astype('category')
df["embarked"].dtype
df.dtypes


#########################################
# Görev 7: embarked değeri C olanların tüm bilgilerini gösteriniz.
#########################################

df["embarked"].value_counts()

# 1. yol
embarked_c = df[df['embarked'] == 'C']

# 2. yol 'embarked' sütununda 'C' olan satırları liste
filtered_embarked = [row for index, row in df.iterrows() if row['embarked'] == 'C']

# Listeyi bir DataFrame'e dönüştür
filtered_df = pd.DataFrame(filtered_embarked)
#
#df.loc[df["embarked"] == "C", ].head()

#########################################
# Görev 8: embarked değeri S olmayanların tüm bilgelerini gösteriniz.
#########################################

embarked_nots = df[df['embarked'] != 'S']
#
df[~(df["embarked"] == "S")]
#
df[~(df["embarked"] == "S")]["embarked"].unique()

#########################################
# Görev 9: Yaşı 30 dan küçük ve kadın olan yolcuların tüm bilgilerini gösteriniz.
#########################################

df[(df["age"] < 30) &  (df["sex"] == "female")]

#########################################
# Görev 10: Fare'i 500'den büyük veya yaşı 70 den büyük yolcuların bilgilerini gösteriniz.
#########################################

df[(df["fare"] > 500) | (df["age"] > 70)]

#########################################
# Görev 11: Her bir değişkendeki boş değerlerin toplamını bulunuz.
#########################################

missing_values1 = df.isnull().sum()
#
missing_values2 = df.isna().sum()


#########################################
# Görev 12: who değişkenini dataframe'den düşürün.
#########################################

drop_who = df.drop(columns=['who'])
df.head(10)
#
df.drop("who", axis=1).head()
#########################################
# Görev 13: deck değikenindeki boş değerleri deck değişkenin en çok tekrar eden değeri (mode) ile doldurunuz.
#########################################

df = sns.load_dataset("Titanic")
df.head(10)

# 'deck' sütunundaki mod
mode_deck = df['deck'].mode()[0]  # İlk elemanı alıyoruz çünkü birden fazla mode olabilir

# Boş değerleri en çok tekrar eden değer ile doldur
df['deck'] = df['deck'].fillna(mode_deck)

df['deck'].head(10)


#########################################
# Görev 14: age değikenindeki boş değerleri age değişkenin medyanı ile doldurun.
#########################################

df["age"].isnull().sum()

# 1.Yol 'age' sütunundaki medyan değeri hesapla
median_age = df['age'].median()

# 'age' sütunundaki boş değerleri doldur
df['age'].fillna(median_age)

#2.yol
filled_df = df.fillna(value={'age': df['age'].median()})
filled_df["age"].isnull().sum()

#########################################
# Görev 15: survived değişkeninin Pclass ve Cinsiyet değişkenleri kırılımınında sum, count, mean değerlerini bulunuz.
#########################################

result = df.groupby(['pclass', 'sex'])['survived'].agg(['sum', 'count', 'mean'])

df.groupby(["pclass" ,"sex"]).agg({"survived" : ["sum","count","mean"]})

#########################################
# Görev 16:  30 yaşın altında olanlar 1, 30'a eşit ve üstünde olanlara 0 vericek bir fonksiyon yazınız.
# Yazdığınız fonksiyonu kullanarak titanik veri setinde age_flag adında bir değişken oluşturunuz oluşturunuz. (apply ve lambda yapılarını kullanınız)
#########################################


df["age_flag"] = df["age"].apply(lambda age: 1 if age < 30 else 0)

print(df[['age', 'age_flag']].head())

#########################################
# Görev 17: Seaborn kütüphanesi içerisinden Tips veri setini tanımlayınız.
#########################################

df = sns.load_dataset("tips")
df.head()

#########################################
# Görev 18: Time değişkeninin kategorilerine (Dinner, Lunch) göre total_bill  değerlerinin toplamını, min, max ve ortalamasını bulunuz.
#########################################
#1.yol
df.groupby('time', observed=False)['total_bill'].agg(['sum', 'min', 'max', 'mean'])
#2.yol
df.groupby("time").agg({"total_bill": ["min", "max", "mean","sum"]})

#########################################
# Görev 19: Günlere ve time göre total_bill değerlerinin toplamını, min, max ve ortalamasını bulunuz.
#########################################
df.groupby(['day', 'time']).agg({'total_bill': ['sum', 'min', 'max', 'mean']})


#########################################
# Görev 20:Lunch zamanına ve kadın müşterilere ait total_bill ve tip  değerlerinin day'e göre toplamını, min, max ve ortalamasını bulunuz.
#########################################
df[(df["time"] == "Lunch") & (df["sex"] == "Female")].groupby("day").agg({"total_bill": ["sum", "min", "max", "mean"],
                                                                          "tip": ["sum", "min", "max", "mean"]})


#########################################
# Görev 21: size'i 3'ten küçük, total_bill'i 10'dan büyük olan siparişlerin ortalaması nedir?
#########################################

df.loc[(df["size"] < 3) & (df["total_bill"] > 10), "total_bill"].mean()


#########################################
# Görev 22: total_bill_tip_sum adında yeni bir değişken oluşturun. Her bir müşterinin ödediği totalbill ve tip in toplamını versin.
#########################################

df['total_bill_tip_sum'] = (df['total_bill'] + df['tip']).head()


#########################################
# Görev 23: total_bill_tip_sum değişkenine göre büyükten küçüğe sıralayınız ve ilk 30 kişiyi yeni bir dataframe'e atayınız.
#########################################

top_30 = df.sort_values(by='total_bill_tip_sum', ascending=False).head(30)

