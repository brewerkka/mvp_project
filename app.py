import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Анализ зарплат в России", layout="wide")


@st.cache_data
def load_data():
    return pd.read_csv("data/zarplaty_realnye.csv")


df = load_data()

st.title("Анализ зарплат в России (2000–2024)")
st.markdown(
    "Данные по секторам: **транспорт**, **образование**, **здравоохранение**. Реальная зарплата рассчитывается с учетом инфляции (CPI)."
)

sectors = st.multiselect(
    "Выберите сектор(ы)", options=df["Сектор"].unique(), default=df["Сектор"].unique()
)

df_filtered = df[df["Сектор"].isin(sectors)]

st.subheader("Номинальная зарплата по секторам")
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df_filtered, x="Год", y="Зарплата", hue="Сектор", marker="o", ax=ax1)
ax1.set_title("Номинальная зарплата (₽)")
ax1.set_ylabel("Зарплата")
st.pyplot(fig1)

st.subheader("Реальная зарплата (с учетом инфляции)")
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=df_filtered, x="Год", y="Реальная зарплата", hue="Сектор", marker="o", ax=ax2
)
ax2.set_title("Реальная зарплата (₽)")
ax2.set_ylabel("Реальная зарплата")
st.pyplot(fig2)

st.subheader("Изменение реальной зарплаты по годам")
df_sorted = df_filtered.sort_values(["Сектор", "Год"])
df_sorted["Δ Реальная зарплата"] = df_sorted.groupby("Сектор")[
    "Реальная зарплата"
].diff()

fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.barplot(data=df_sorted, x="Год", y="Δ Реальная зарплата", hue="Сектор", ax=ax3)
ax3.axhline(0, color="gray", linestyle="--")
ax3.set_title("Годовое изменение реальной зарплаты")
ax3.set_ylabel("Изменение, ₽")
st.pyplot(fig3)
