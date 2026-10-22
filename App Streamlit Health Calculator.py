import streamlit as st
from datetime import datetime

# =========================
# HEALTH & FITNESS CALCULATOR
# =========================

st.set_page_config(
    page_title="Health & Fitness Calculator",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Styling dashboard
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: linear-gradient(145deg, #eefaf8 0%, #f5fbfc 55%, #e7f5f4 100%);
        color: #24343a;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Memaksa semua label input berwarna gelap agar selalu terlihat */
    label, [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* Style untuk label kustom */
    .custom-label {
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 4px;
        font-size: 0.95rem;
    }
    .custom-sublabel {
        font-size: 0.8rem;
        color: #64748b;
        margin-bottom: 6px;
    }

    .topbar {
        background: linear-gradient(100deg, #168d8b, #35b1a9);
        color: white;
        padding: 18px 22px;
        border-radius: 16px;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(24, 125, 122, .14);
    }
    .topbar h1 {
        color: white;
        font-size: clamp(1.15rem, 3vw, 1.75rem);
        margin: 0;
        font-weight: 800;
    }
    .topbar p { margin: 5px 0 0; color: #e5ffff; font-size: .9rem; }
    .metric-card {
        background: rgba(255,255,255,.96);
        border: 1px solid #d9eeeb;
        border-radius: 16px;
        padding: 18px;
        min-height: 142px;
        box-shadow: 0 5px 18px rgba(40, 93, 92, .06);
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: .94rem;
        color: #177f7b;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .metric-value {
        font-size: clamp(1.45rem, 3vw, 2rem);
        color: #25363b;
        font-weight: 800;
        line-height: 1.2;
        overflow-wrap: anywhere;
    }
    .metric-caption { color: #667a7d; font-size: .86rem; margin-top: 8px; }
    .section-card {
        background: rgba(255,255,255,.96);
        border: 1px solid #d9eeeb;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 5px 18px rgba(40, 93, 92, .05);
        margin-bottom: 14px;
    }
    .section-card h3 { margin-top: 0; color: #263b40; font-size: 1.1rem; }
    .small-note { color: #64777a; font-size: .82rem; }
    div.stButton > button[kind="primary"] {
        background: #f19a4a;
        border: 0;
        color: white;
        font-weight: 700;
        border-radius: 10px;
        min-height: 44px;
    }
    div.stButton > button[kind="primary"]:hover { background: #dc8336; color: white; }
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #d9eeeb;
        padding: 12px;
        border-radius: 12px;
    }
    @media (max-width: 640px) {
        .topbar { padding: 15px; border-radius: 12px; }
        .metric-card { padding: 14px; min-height: 125px; }
        .section-card { padding: 14px; }
    }
</style>
""", unsafe_allow_html=True)


# -------------------------
# Fungsi perhitungan
# -------------------------
def hitung_bmi(berat, tinggi):
    tinggi_m = tinggi / 100
    return berat / (tinggi_m ** 2)


def evaluasi_bmi(bmi):
    if bmi < 18.5:
        return "Kurus (Underweight)"
    elif bmi < 25:
        return "Normal (Ideal)"
    elif bmi < 30:
        return "Gemuk (Overweight)"
    return "Obesitas"


def hitung_bmr(berat, tinggi, usia, jenis_kelamin):
    if jenis_kelamin == "Pria":
        return (10 * berat) + (6.25 * tinggi) - (5 * usia) + 5
    return (10 * berat) + (6.25 * tinggi) - (5 * usia) - 161


def rekomendasi_kesehatan(status_bmi):
    if status_bmi == "Kurus (Underweight)":
        aktivitas = [
            "Latihan kekuatan ringan hingga sedang secara bertahap.",
            "Jalan santai, bersepeda, atau aktivitas fisik ringan.",
            "Berikan waktu istirahat yang cukup agar tubuh dapat pulih.",
        ]
        makanan = [
            "Konsumsi makanan bergizi dan seimbang.",
            "Utamakan sumber protein, karbohidrat, sayur, dan buah.",
            "Jangan melewatkan waktu makan dan cukupi kebutuhan cairan.",
        ]
        pola = [
            "Makan secara teratur.",
            "Tidur cukup dan teratur.",
            "Tingkatkan aktivitas secara bertahap sesuai kemampuan tubuh.",
        ]
    elif status_bmi == "Normal (Ideal)":
        aktivitas = [
            "Lakukan olahraga secara rutin.",
            "Jalan kaki, bersepeda, berenang, atau olahraga yang disukai.",
            "Tambahkan latihan kekuatan beberapa kali dalam seminggu.",
        ]
        makanan = [
            "Pertahankan pola makan yang beragam dan bergizi seimbang.",
            "Konsumsi sayur, buah, protein, dan sumber karbohidrat secukupnya.",
            "Batasi makanan dan minuman yang tinggi gula, garam, dan lemak.",
        ]
        pola = [
            "Pertahankan aktivitas fisik secara rutin.",
            "Tidur cukup dan teratur.",
            "Seimbangkan waktu belajar, aktivitas, olahraga, dan istirahat.",
        ]
    elif status_bmi == "Gemuk (Overweight)":
        aktivitas = [
            "Perbanyak aktivitas fisik ringan hingga sedang.",
            "Jalan kaki, bersepeda, berenang, atau olahraga permainan.",
            "Tingkatkan aktivitas secara bertahap sesuai kemampuan.",
        ]
        makanan = [
            "Konsumsi makanan bergizi seimbang.",
            "Perbanyak sayur dan buah serta sumber protein.",
            "Batasi makanan dan minuman tinggi gula, garam, dan lemak.",
        ]
        pola = [
            "Kurangi terlalu banyak duduk dalam waktu lama.",
            "Lakukan aktivitas fisik secara rutin.",
            "Jaga pola tidur yang cukup dan teratur.",
        ]
    else:
        aktivitas = [
            "Mulai dari aktivitas ringan seperti berjalan santai.",
            "Tingkatkan durasi dan intensitas aktivitas secara bertahap.",
            "Pilih aktivitas yang nyaman dan dapat dilakukan secara rutin.",
        ]
        makanan = [
            "Fokus pada makanan bergizi dan seimbang.",
            "Perbanyak sayur, buah, protein, dan sumber karbohidrat bergizi.",
            "Batasi makanan dan minuman tinggi gula, garam, dan lemak.",
        ]
        pola = [
            "Kurangi waktu duduk terlalu lama dan lakukan jeda untuk bergerak.",
            "Bangun kebiasaan aktivitas fisik secara perlahan.",
            "Jaga tidur yang cukup dan teratur.",
            "Jika memiliki masalah kesehatan, konsultasikan dengan tenaga kesehatan.",
        ]
    return aktivitas, makanan, pola


def warna_status(status):
    if status == "Normal (Ideal)":
        return "#188568"
    if status == "Kurus (Underweight)":
        return "#277eae"
    if status == "Gemuk (Overweight)":
        return "#bd7b16"
    return "#c94b4b"


def tampilkan_list(items):
    for item in items:
        st.markdown(f"- {item}")


# -------------------------
# Header
# -------------------------
st.markdown("""
<div class="topbar">
  <h1>💚 HEALTH &amp; FITNESS CALCULATOR</h1>
  <p>Dashboard Kesehatan Sederhana</p>
</div>
""", unsafe_allow_html=True)

st.markdown("## Health Dashboard")
st.caption("Masukkan data kamu untuk menghitung BMI, BMR, kebutuhan kalori harian, dan melihat rekomendasi kesehatan.")

# State untuk riwayat
if "riwayat_kesehatan" not in st.session_state:
    st.session_state.riwayat_kesehatan = []

# Layout
form_col, result_col = st.columns([0.85, 1.35], gap="large")

with form_col:
    st.markdown('<div class="section-card"><h3>📝 Data Pengguna</h3></div>', unsafe_allow_html=True)
    with st.form("form_kesehatan", clear_on_submit=False):
        
        # Nama
        st.markdown('<div class="custom-label">👤 Nama Lengkap</div>', unsafe_allow_html=True)
        nama = st.text_input("Nama", placeholder="Masukkan nama kamu", label_visibility="collapsed")

        # Usia
        st.markdown('<div class="custom-label">📅 Usia (Tahun)</div>', unsafe_allow_html=True)
        usia = st.number_input("Usia", min_value=1, max_value=120, value=1, step=1, label_visibility="collapsed")

        # Berat
        st.markdown('<div class="custom-label">⚖️ Berat Badan (kg)</div>', unsafe_allow_html=True)
        berat = st.number_input("Berat", min_value=1.0, max_value=500.0, value=1.0, step=0.5, label_visibility="collapsed")

        # Tinggi
        st.markdown('<div class="custom-label">📏 Tinggi Badan (cm)</div>', unsafe_allow_html=True)
        tinggi = st.number_input("Tinggi", min_value=50.0, max_value=250.0, value=1.0, step=0.5, label_visibility="collapsed")

        # Jenis Kelamin
        st.markdown('<div class="custom-label">⚥ Jenis Kelamin</div>', unsafe_allow_html=True)
        jenis_kelamin = st.selectbox("Jenis Kelamin", ["Pria", "Wanita"], label_visibility="collapsed")

        # Aktivitas
        st.markdown('<div class="custom-label">⚡ Tingkat Aktivitas Fisik</div>', unsafe_allow_html=True)
        st.markdown('<div class="custom-sublabel">Pilih frekuensi olahraga mingguan kamu</div>', unsafe_allow_html=True)
        aktivitas_label = st.selectbox(
            "Aktivitas",
            [
                "Jarang olahraga",
                "Ringan (1–3 hari/minggu)",
                "Sedang (3–5 hari/minggu)",
                "Berat (6–7 hari/minggu)",
            ],
            index=2,
            label_visibility="collapsed"
        )
        
        submitted = st.form_submit_button("HITUNG KALKULASI", type="primary", use_container_width=True)

    reset_col, history_col = st.columns(2)
    with reset_col:
        if st.button("↻ Reset hasil", use_container_width=True):
            st.session_state.pop("hasil_kesehatan", None)
            st.rerun()
    with history_col:
        show_history = st.button("◷ Riwayat", use_container_width=True)

    if show_history:
        st.session_state["lihat_riwayat"] = not st.session_state.get("lihat_riwayat", False)

    if submitted:
        bmi = hitung_bmi(float(berat), float(tinggi))
        status = evaluasi_bmi(bmi)
        bmr = hitung_bmr(float(berat), float(tinggi), int(usia), jenis_kelamin)
        faktor = [1.2, 1.375, 1.55, 1.725]
        index_aktivitas = [
            "Jarang olahraga",
            "Ringan (1–3 hari/minggu)",
            "Sedang (3–5 hari/minggu)",
            "Berat (6–7 hari/minggu)",
        ].index(aktivitas_label)
        tdee = bmr * faktor[index_aktivitas]
        aktivitas_rec, makanan_rec, pola_rec = rekomendasi_kesehatan(status)

        hasil = {
            "nama": nama.strip() or "Pengguna",
            "usia": int(usia),
            "berat": float(berat),
            "tinggi": float(tinggi),
            "jenis_kelamin": jenis_kelamin,
            "aktivitas_label": aktivitas_label,
            "bmi": bmi,
            "status": status,
            "bmr": bmr,
            "tdee": tdee,
            "aktivitas_rec": aktivitas_rec,
            "makanan_rec": makanan_rec,
            "pola_rec": pola_rec,
            "waktu": datetime.now().strftime("%d-%m-%Y %H:%M"),
        }
        st.session_state.hasil_kesehatan = hasil
        st.session_state.riwayat_kesehatan.append(hasil)

with result_col:
    hasil = st.session_state.get("hasil_kesehatan")
    if hasil:
        st.markdown("### Hasil Perhitungan")
        bmi_col, bmr_col, tdee_col = st.columns(3, gap="small")
        with bmi_col:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-title">💚 BMI</div>
              <div class="metric-value">{hasil['bmi']:.1f}</div>
              <div class="metric-caption" style="color:{warna_status(hasil['status'])};font-weight:700">{hasil['status']}</div>
            </div>
            """, unsafe_allow_html=True)
        with bmr_col:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-title">🔥 BMR</div>
              <div class="metric-value">{hasil['bmr']:,.0f}</div>
              <div class="metric-caption">kkal/hari saat istirahat</div>
            </div>
            """, unsafe_allow_html=True)
        with tdee_col:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-title">⚡ TDEE</div>
              <div class="metric-value">{hasil['tdee']:,.0f}</div>
              <div class="metric-caption">kkal/hari perkiraan</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="section-card">
          <h3>🎯 Target Kalori Harian</h3>
          <div style="font-size:1.55rem;font-weight:800;color:#25363b">{hasil['tdee']:,.0f} kkal/hari</div>
          <div class="small-note">Estimasi untuk mempertahankan berat berdasarkan tingkat aktivitas yang dipilih.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Rekomendasi Kesehatan")
        tab1, tab2, tab3 = st.tabs(["🏃 Aktivitas", "🥗 Pola makan", "🌙 Istirahat"])
        with tab1:
            tampilkan_list(hasil["aktivitas_rec"])
        with tab2:
            tampilkan_list(hasil["makanan_rec"])
        with tab3:
            tampilkan_list(hasil["pola_rec"])
    else:
        st.markdown("""
        <div class="section-card">
          <h3>💚 Hasil Kesehatan</h3>
          <p>Hasil BMI, BMR, dan TDEE akan muncul di sini setelah kamu menekan tombol <b>HITUNG KALKULASI</b>.</p>
          <p class="small-note">Tip: gunakan data yang benar agar estimasi yang ditampilkan lebih relevan.</p>
        </div>
        """, unsafe_allow_html=True)

if st.session_state.get("lihat_riwayat", False):
    st.markdown("---")
    st.subheader("🕘 Riwayat Perhitungan")
    if st.session_state.riwayat_kesehatan:
        for idx, item in enumerate(reversed(st.session_state.riwayat_kesehatan), start=1):
            with st.expander(f"{item['waktu']} • {item['nama']}"):
                st.write(f"BMI: **{item['bmi']:.1f}** — {item['status']}")
                st.write(f"BMR: **{item['bmr']:,.0f} kkal/hari**")
                st.write(f"TDEE: **{item['tdee']:,.0f} kkal/hari**")
                st.caption(f"{item['usia']} tahun • {item['jenis_kelamin']} • {item['aktivitas_label']}")
    else:
        st.info("Belum ada riwayat. Lakukan perhitungan terlebih dahulu.")

st.markdown("---")
st.markdown(
    '<p class="small-note">Catatan: BMI adalah indikator umum dan bukan diagnosis kesehatan. '
    'Rumus BMR dan estimasi kalori memiliki keterbatasan, terutama pada remaja yang masih tumbuh. '
    'Gunakan hasil sebagai edukasi, bukan pengganti saran tenaga kesehatan.</p>',
    unsafe_allow_html=True,
)