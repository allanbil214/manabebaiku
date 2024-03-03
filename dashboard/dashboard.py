import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Get yo Data ova here
urls = [
    'https://raw.githubusercontent.com/allanbangkit/manabebaiku/main/dataset/day.csv',
    'https://raw.githubusercontent.com/allanbangkit/manabebaiku/main/dataset/hour.csv'
]

dfs = [pd.read_csv(url) for url in urls]
df_day, df_hour = dfs


df_baiku = pd.merge(df_hour, df_day, on='dteday', how='inner', suffixes=('_hour', '_day'))

weather_labels = {1: 'Cerah', 2: 'Berawan', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}
df_baiku['weather_label'] = df_baiku['weathersit_day'].replace(weather_labels)

#Get yo Interface ova here

datetime_columns = ["dteday"]

for column in datetime_columns:
    df_baiku[column] = pd.to_datetime(df_baiku[column])

min_date = df_baiku["dteday"].min()
max_date = df_baiku["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://animevortexblog.files.wordpress.com/2017/02/bql4rep.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df_baiku[(df_baiku["dteday"] >= str(start_date)) & 
                (df_baiku["dteday"] <= str(end_date))]

st.header('Manabe Baiku :bike:')

# Get yo Graphic 1 ova here
st.subheader("Hari Kerja vs Hari Libur?!")

grouped_by_workingday = df_baiku.groupby('workingday_hour')['cnt_hour'].mean()
grouped_by_workingday.plot(kind='bar', rot=0)
plt.xlabel('Hari Libur (0) / Hari Kerja (1)')
plt.ylabel('Jumlah Pengguna Sepeda (Rata-rata)')
plt.title('Perbandingan Penggunaan Sepeda pada Hari Kerja dan Hari Libur')

st.pyplot(plt)
plt.clf() 
# End of Graphic 1 ova here

# Get yo Graphic 2 ova here
st.subheader("Korelasi Cuaca dan Penyepeda?!")

correlation_weather = df_baiku['weathersit_hour'].corr(df_baiku['cnt_hour'])

avg_cnt_by_weather = df_baiku.groupby('weathersit_hour')['cnt_hour'].mean()
avg_cnt_by_weather.plot(kind='bar', color='skyblue')
plt.xlabel('Kondisi Cuaca (weathersit_hour)')
plt.ylabel('Jumlah Pengguna Sepeda (cnt_hour)')
plt.title(f'Hubungan Antara Kondisi Cuaca dan Jumlah Pengguna Sepeda\nKorelasi: {correlation_weather}')
plt.xticks(rotation=0)

st.pyplot(plt)
plt.clf() 
# End of Graphic 2 ova here

# Get yo Graphic 3 ova here
st.subheader("Korelasi Kelembaban dengan Penyepeda?!")

correlation_humidity = df_baiku['hum_day'].corr(df_baiku['cnt_day'])

plt.scatter(df_baiku['hum_day'], df_baiku['cnt_day'])
plt.xlabel('Kelembaban Udara (hum_day)')
plt.ylabel('Jumlah Pengguna Sepeda (cnt_day)')
plt.title(f'Hubungan Antara Kelembaban Udara dan Jumlah Pengguna Sepeda\nKorelasi: {correlation_humidity}')

st.pyplot(plt)
plt.clf() 
# End of Graphic 3 ova here

# Get yo Graphic 4 ova here
st.subheader("Rata-rata Penyewaan Sepeda pada Hari Libur")

df_baiku['season'] = pd.to_datetime(df_baiku['dteday']).dt.month.map({1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring', 
                                                           6: 'Summer', 7: 'Summer', 8: 'Summer', 9: 'Fall', 10: 'Fall', 
                                                           11: 'Fall', 12: 'Winter'})

# Grouping data berdasarkan musim
grouped_by_season = df_baiku.groupby('season')['cnt_day'].mean()

grouped_by_season.plot(kind='bar', rot=0, color=['blue', 'red', 'green', 'orange'])
plt.xlabel('Musim')
plt.ylabel('Jumlah Pengguna Sepeda (Rata-rata)')
plt.title('Perbandingan Penggunaan Sepeda Antara Musim')

st.pyplot(plt)
plt.clf() 
# End of Graphic 4 ova here