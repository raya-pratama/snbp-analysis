import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==============================================
# KONFIGURASI HALAMAN
# ==============================================
st.set_page_config(
    page_title="Dashboard Analisis SNBP Jawa Timur",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================
# LOAD DATA
# ==============================================
@st.cache_data  # agar data di-cache tidak di-load berulang
def load_data():
    df = pd.read_csv("data/cleaned/snbp_data_cleaned.csv")
    # Hitung metrik keketatan
    df["rasio_keketatan"] = round(df["peminat"] / df["daya_tampung"], 2)
    df["persentase_kelulusan"] = round(df["diterima"] / df["peminat"] * 100, 2)
    # Untuk tahun 2026, yang belum ada data lulus, tampilkan prediksi berdasarkan 2025
    return df

df = load_data()

# ==============================================
# SIDEBAR FILTER
# ==============================================
with st.sidebar:
    st.header("🔍 Filter Data")
    pilih_tahun = st.multiselect(
        "Pilih Tahun",
        options=sorted(df["tahun"].unique()),
        default=sorted(df["tahun"].unique())
    )
    pilih_ptn = st.multiselect(
        "Pilih PTN",
        options=sorted(df["nama_ptn"].unique()),
        default=sorted(df["nama_ptn"].unique())
    )
    pilih_asal_sekolah = st.radio(
        "Asal Sekolah",
        options=[
            "Semua",
            "SMA IPA",
            "SMA IPS",
            "SMK Semua Jurusan",
            "SMK Teknik/Informatika",
            "SMK Kesehatan",
            "SMK Bisnis/Pariwisata"
        ],
        index=0,
        help="Filter prodi yang sesuai dengan asal sekolahmu"
    )
    pilih_jenjang = st.multiselect(
        "Jenjang Pendidikan",
        options=sorted(df["jenjang"].unique()),
        default=sorted(df["jenjang"].unique())
    )

# Filter data sesuai pilihan pengguna
df_filtered = df[df["tahun"].isin(pilih_tahun)]
df_filtered = df_filtered[df_filtered["nama_ptn"].isin(pilih_ptn)]
df_filtered = df_filtered[df_filtered["jenjang"].isin(pilih_jenjang)]

# Filter berdasarkan asal sekolah
if pilih_asal_sekolah == "SMA IPA":
    df_filtered = df_filtered[df_filtered["kelompok_prodi"].str.contains("IPA|SMK|IPA_IPS")]
elif pilih_asal_sekolah == "SMA IPS":
    df_filtered = df_filtered[df_filtered["kelompok_prodi"].str.contains("IPS|IPA_IPS|SMK_Bisnis|SMK_Pariwisata")]
elif pilih_asal_sekolah == "SMK Semua Jurusan":
    df_filtered = df_filtered[df_filtered["kelompok_prodi"].str.contains("SMK")]
elif pilih_asal_sekolah == "SMK Teknik/Informatika":
    df_filtered = df_filtered[df_filtered["kelompok_prodi"].str.contains("SMK_Teknik|IPA_SMK")]
elif pilih_asal_sekolah == "SMK Kesehatan":
    df_filtered = df_filtered[df_filtered["kelompok_prodi"].str.contains("SMK_Kesehatan")]
elif pilih_asal_sekolah == "SMK Bisnis/Pariwisata":
    df_filtered = df_filtered[df_filtered["kelompok_prodi"].str.contains("SMK_Bisnis|SMK_Pariwisata|IPS_SMK")]

# ==============================================
# HALAMAN UTAMA
# ==============================================
st.title("🎓 Dashboard Analisis Kelulusan SNBP Jawa Timur 2024-2026")
st.markdown("Dashboard interaktif untuk melihat peta persaingan masuk PTN di Jawa Timur berdasarkan data SNBP 3 tahun terakhir. Proyek portofolio Data Analyst.")
st.divider()

# ==============================================
# KARTU RINGKASAN UTAMA
# ==============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_kuota = int(df_filtered[df_filtered["tahun"] != 2026]["daya_tampung"].sum())
    st.metric(
        label="Total Kuota SNBP (data riil 2024-2025)",
        value=f"{total_kuota:,}"
    )

with col2:
    total_peminat = int(df_filtered[df_filtered["tahun"] != 2026]["peminat"].sum())
    st.metric(
        label="Total Peminat (2024-2025)",
        value=f"{total_peminat:,}"
    )

with col3:
    rata_rata_keketatan = round(df_filtered[df_filtered["tahun"] != 2026]["rasio_keketatan"].mean(), 2)
    st.metric(
        label="Rata-rata Rasio Keketatan",
        value=f"1 : {rata_rata_keketatan}"
    )

with col4:
    jumlah_prodi = len(df_filtered["nama_prodi"].unique())
    st.metric(
        label="Jumlah Program Studi",
        value=f"{jumlah_prodi}"
    )

st.divider()

# ==============================================
# GRAFIK 1: 10 Prodi Paling Ketat
# ==============================================
st.subheader("🚨 10 Program Studi Paling Ketat Persaingannya")
st.caption("Diurutkan berdasarkan rasio peminat per 1 kursi, data tahun 2025")
df_paling_ketat = df_filtered[df_filtered["tahun"] == 2025].sort_values(by="rasio_keketatan", ascending=False).head(10)
fig_ketat = px.bar(
    df_paling_ketat,
    y="nama_prodi",
    x="rasio_keketatan",
    color="nama_ptn",
    orientation="h",
    labels={
        "rasio_keketatan": "Rasio Keketatan (1 kursi : X peminat)",
        "nama_prodi": "Program Studi",
        "nama_ptn": "Perguruan Tinggi"
    },
    hover_data=["daya_tampung", "peminat"]
)
fig_ketat.update_layout(yaxis=dict(autorange="reversed"))
st.plotly_chart(fig_ketat, use_container_width=True)

# ==============================================
# GRAFIK KHUSUS SMK (jika filter SMK dipilih)
# ==============================================
if "SMK" in pilih_asal_sekolah:
    st.divider()
    st.subheader("🔧 Prodi Khusus/Ramai Diisi Anak SMK (Data 2025)")
    st.info("✅ Semua prodi di daftar ini menerima siswa SMK sesuai jurusan yang relevan", icon="ℹ️")
    df_smk = df_filtered[df_filtered["tahun"] == 2025].sort_values(by="rasio_keketatan", ascending=False).head(15)
    fig_smk = px.bar(
        df_smk,
        y="nama_prodi",
        x="rasio_keketatan",
        color="jenjang",
        orientation="h",
        labels={
            "rasio_keketatan": "Rasio Keketatan (1 : X peminat)",
            "nama_prodi": "Program Studi",
            "jenjang": "Jenjang"
        },
        hover_data=["daya_tampung", "peminat", "nama_ptn"]
    )
    fig_smk.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_smk, use_container_width=True)

# ==============================================
# GRAFIK 2: Tren Kuota Per Tahun Per PTN
# ==============================================
st.subheader("📈 Tren Alokasi Kuota Per PTN 2024-2026")
tren_kuota = df_filtered.groupby(["tahun", "nama_ptn", "jenjang"])["daya_tampung"].sum().reset_index()
fig_tren = px.line(
    tren_kuota,
    x="tahun",
    y="daya_tampung",
    color="nama_ptn",
    line_dash="jenjang",
    markers=True,
    labels={
        "daya_tampung": "Total Daya Tampung",
        "tahun": "Tahun",
        "nama_ptn": "Perguruan Tinggi",
        "jenjang": "Jenjang"
    }
)
st.plotly_chart(fig_tren, use_container_width=True)

# ==============================================
# PERBANDINGAN KUOTA S1 VS VOKASI (D3/D4)
# ==============================================
st.subheader("⚖️ Perbandingan Kuota Prodi S1 vs Vokasi (D3/D4) 2025")
kuota_jenjang = df_filtered[df_filtered["tahun"] == 2025].groupby(["nama_ptn", "jenjang"])["daya_tampung"].sum().reset_index()
fig_jenjang = px.bar(
    kuota_jenjang,
    x="nama_ptn",
    y="daya_tampung",
    color="jenjang",
    barmode="group",
    labels={
        "daya_tampung": "Total Daya Tampung",
        "nama_ptn": "Perguruan Tinggi",
        "jenjang": "Jenjang"
    }
)
st.plotly_chart(fig_jenjang, use_container_width=True)

# ==============================================
# TABEL DATA LENGKAP
# ==============================================
st.divider()
st.subheader("📋 Tabel Data Lengkap Bisa Diurutkan")
st.caption("Kolom 'Bisa Diisi SMK' menunjukkan prodi yang menerima lulusan SMK")
df_tabel = df_filtered.copy()
df_tabel["bisa_smk"] = df_tabel["kelompok_prodi"].str.contains("SMK").map({True: "✅ Ya", False: "❌ Tidak"})
st.dataframe(
    df_tabel.sort_values(by="rasio_keketatan", ascending=False)[["tahun", "nama_ptn", "nama_prodi", "jenjang", "daya_tampung", "peminat", "rasio_keketatan", "bisa_smk", "akreditasi_prodi"]],
    use_container_width=True,
    hide_index=True,
    column_config={
        "rasio_keketatan": st.column_config.NumberColumn(
            "Rasio Keketatan",
            format="1 : %.2f"
        )
    }
)

# ==============================================
# FOOTER
# ==============================================
st.divider()
st.caption("Proyek portofolio Data Analysis | Sumber data: Resmi PMB masing-masing PTN Jawa Timur | Dibuat dengan Python, Pandas, Plotly, dan Streamlit")
