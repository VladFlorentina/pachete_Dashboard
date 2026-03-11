import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Spotify", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #121212 !important; color: #ffffff !important; }
    h1, h2, h3, h4 { color: #1DB954 !important; font-weight: 700 !important; }
    p, label { color: #b3b3b3 !important; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #282828; }
    [data-testid="stMetricValue"] { color: #1DB954 !important; }
</style>
""", unsafe_allow_html=True)

st.title("Top Melodii Spotify")  

st.info("Datele sunt incarcate automat din fisierul Spotify-2000.csv.")

try:
    df = pd.read_csv("Spotify-2000.csv")
    df.columns = df.columns.str.strip() 
except FileNotFoundError:
    st.error("Fisierul Spotify-2000.csv nu a fost gasit in acest folder.")
    st.stop()

coloana_categorica = "Top Genre" if "Top Genre" in df.columns else "Genre"
coloana_fericire = "Valence" 
coloana_ritm = "Beats Per Minute (BPM)"
coloana_popularitate = "Popularity" if "Popularity" in df.columns else df.columns[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Total inregistrari", len(df))
col2.metric("Piese foarte fericite (>70/100)", len(df[df[coloana_fericire] > 70]))
col3.metric("Ritm Mediu (BPM)", round(df[coloana_ritm].mean(), 1))

st.dataframe(df.head(10), use_container_width=True)

st.sidebar.header("Filtre")

optiuni_gen = df[coloana_categorica].dropna().unique().tolist()
selectie = st.sidebar.multiselect("Alege Genul Muzical", optiuni_gen, default=optiuni_gen[:4])

df_filtrat = df[df[coloana_categorica].isin(selectie)]

if len(df_filtrat) == 0:
    st.warning("Te rog selecteaza cel putin o optiune din filtre.")
    st.stop()


st.subheader("1. Fericirea in muzica")
st.write("Acest grafic arata cota de fericire (Valence: 0=Trist, 100=Fericit) in functie de genul muzical.")

fig = px.bar(
    df_filtrat.groupby(coloana_categorica)[coloana_fericire].mean().reset_index(),
    x=coloana_categorica,
    y=coloana_fericire,
    color=coloana_categorica,
    labels={coloana_categorica: "Gen Muzical", coloana_fericire: "Grad Mediu de Fericire (0-100)"},
    title="Ce genuri muzicale sunt cele mai vesele?",
    color_discrete_sequence=['#1DB954', '#1ed760', '#55f088', '#b3b3b3'] 
)
fig.update_layout(paper_bgcolor='#121212', plot_bgcolor='#121212', font=dict(color='#b3b3b3'), showlegend=False)
st.plotly_chart(fig, use_container_width=True)


st.subheader("2. Ritmul pieselor (BPM)")
st.write("Acest grafic arata cate piese sunt lente si cate sunt rapide in functie de ritm (Beats per Minute).")

fig2, ax = plt.subplots(figsize=(9, 4))
fig2.patch.set_facecolor('#121212')
ax.set_facecolor('#121212')
ax.tick_params(colors='#b3b3b3')

ax.hist(df_filtrat[coloana_ritm].dropna(), bins=15, color="#1DB954", edgecolor="white")
ax.set_title("Distributia ritmului (lentoare vs alert)", color='#1DB954')
ax.set_xlabel("Ritm (BPM - Batai pe Minut)", color='#b3b3b3')
ax.set_ylabel("Numar de piese", color='#b3b3b3')

for spine in ax.spines.values():
    spine.set_color('#282828')

st.pyplot(fig2)
plt.close(fig2)


st.write("---")
st.subheader("3. Preferintele publicului (Popularitate vs Fericire)")
st.write("Sunt piesele cele mai ascultate neaparat si cele mai vesele? Fiecare punct reprezinta o melodie.")

col_titlu = "Title" if "Title" in df.columns else df.columns[1]

fig3 = px.scatter(
    df_filtrat, 
    x=coloana_fericire, 
    y=coloana_popularitate, 
    color=coloana_categorica, 
    hover_name=col_titlu,
    labels={
        coloana_fericire: "Nivel Fericire (0-100)", 
        coloana_popularitate: "Popularitate pe Spotify (0-100)", 
        coloana_categorica: "Gen Muzical"
    },
    title="Corelatia dintre starea de spirit si popularitatea pe Spotify",
    color_discrete_sequence=px.colors.qualitative.Set1
)
fig3.update_layout(
    paper_bgcolor='#121212', 
    plot_bgcolor='#121212', 
    font=dict(color='#b3b3b3'),
    legend=dict(font=dict(size=12))
)
st.plotly_chart(fig3, use_container_width=True)
