import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Fuzzy Beasiswa - Kasus 2", layout="wide", page_icon="🎓")

# Judul Utama Aplikasi
st.title("🎓 Aplikasi Sistem Cerdas Logika Fuzzy - Kelayakan Beasiswa")
st.markdown("### **Studi Kasus 2: Penentuan Kelayakan Berdasarkan IPK (Domain: 0.00 - 4.00)**")
st.write("Aplikasi ini dibuat untuk memenuhi Tugas Praktikum Logika Fuzzy dengan luaran parameter penilaian yang komprehensif.")

st.markdown("---")

# Layout Utama: 2 Kolom Besar
col1, col2 = st.columns([1.1, 0.9])

# ==========================================
# KOLOM 1: INPUT, PERHITUNGAN & INTERPRETASI
# ==========================================
with col1:
    st.header("🎛️ [1] Interface Streamlit & Input Data")
    # Slider Input IPK
    ipk = st.slider("Geser untuk memasukkan nilai IPK Mahasiswa:", min_value=0.00, max_value=4.00, value=2.50, step=0.01)
    
    st.markdown("---")
    
    st.header("🧮 [3] Perhitungan Derajat Keanggotaan")
    st.write("Berikut adalah proses kalkulasi matematika *fuzzifikasi* secara *real-time* berdasarkan nilai IPK yang dimasukkan:")

    # --- Logika Perhitungan & Langkah Rumus ---
    
    # 1. Menghitung Himpunan Tidak Layak
    rumus_tidak_layak = ""
    if ipk <= 1.5:
        mu_tidak_layak = 1.0
        rumus_tidak_layak = f"Karena IPK ({ipk}) ≤ 1.5, maka \\mu = 1.0"
    elif 1.5 < ipk < 2.5:
        mu_tidak_layak = (2.5 - ipk) / (2.5 - 1.5)
        rumus_tidak_layak = f"\\mu = \\frac{{2.5 - {ipk}}}{{2.5 - 1.5}} = \\frac{{{(2.5 - ipk):.2f}}}{{1.0}} = {mu_tidak_layak:.2f}"
    else:
        mu_tidak_layak = 0.0
        rumus_tidak_layak = f"Karena IPK ({ipk}) ≥ 2.5, maka \\mu = 0.0"

    # 2. Menghitung Himpunan Dipertimbangkan
    rumus_dipertimbangkan = ""
    if 1.5 <= ipk <= 2.5:
        mu_dipertimbangkan = (ipk - 1.5) / (2.5 - 1.5)
        rumus_dipertimbangkan = f"\\mu = \\frac{{{ipk} - 1.5}}{{2.5 - 1.5}} = \\frac{{{(ipk - 1.5):.2f}}}{{1.0}} = {mu_dipertimbangkan:.2f}"
    elif 2.5 < ipk <= 3.5:
        mu_dipertimbangkan = (3.5 - ipk) / (3.5 - 2.5)
        rumus_dipertimbangkan = f"\\mu = \\frac{{3.5 - {ipk}}}{{3.5 - 2.5}} = \\frac{{{(3.5 - ipk):.2f}}}{{1.0}} = {mu_dipertimbangkan:.2f}"
    else:
        mu_dipertimbangkan = 0.0
        rumus_dipertimbangkan = f"Karena IPK ({ipk}) diluar domain [1.5 - 3.5], maka \\mu = 0.0"

    # 3. Menghitung Himpunan Layak
    rumus_layak = ""
    if ipk <= 2.5:
        mu_layak = 0.0
        rumus_layak = f"Karena IPK ({ipk}) ≤ 2.5, maka \\mu = 0.0"
    elif 2.5 < ipk < 3.5:
        mu_layak = (ipk - 2.5) / (3.5 - 2.5)
        rumus_layak = f"\\mu = \\frac{{{ipk} - 2.5}}{{3.5 - 2.5}} = \\frac{{{(ipk - 2.5):.2f}}}{{1.0}} = {mu_layak:.2f}"
    else:
        mu_layak = 1.0
        rumus_layak = f"Karena IPK ({ipk}) ≥ 3.5, maka \\mu = 1.0"

    # Tampilan box perhitungan matematika di UI
    with st.expander("Lihat Detail Jalannya Rumus Matematika", expanded=True):
        st.markdown(f"**• Nilai Keanggotaan Himpunan Tidak Layak:**")
        st.latex(rumus_tidak_layak)
        st.markdown(f"**• Nilai Keanggotaan Himpunan Dipertimbangkan:**")
        st.latex(rumus_dipertimbangkan)
        st.markdown(f"**• Nilai Keanggotaan Himpunan Layak:**")
        st.latex(rumus_layak)

    st.markdown("---")

    # --- INTERPRETASI HASIL ---
    st.header("📝 [5] Interpretasi Hasil Akhir")
    nilai_maks = max(mu_tidak_layak, mu_dipertimbangkan, mu_layak)
    
    if nilai_maks == 0:
        st.error("**STATUS KEPUTUSAN: TIDAK TERDEFINISI**")
        st.write("Interpretasi: Nilai input berada di luar jangkauan logika sistem.")
    elif nilai_maks == mu_layak:
        st.success("🎉 **STATUS KEPUTUSAN: REKOMENDASI LAYAK MENERIMA BEASISWA**")
        st.info(f"**Interpretasi Analisis:** Mahasiswa memiliki track record akademik yang sangat unggul dengan nilai IPK **{ipk:.2f}**. Dalam grafik himpunan fuzzy, nilai tersebut dominan masuk ke dalam kategori **Layak** dengan derajat keanggotaan tertinggi sebesar **{mu_layak:.2f}**. Mahasiswa ini diprioritaskan utama untuk lolos pendanaan beasiswa.")
    elif nilai_maks == mu_dipertimbangkan:
        st.warning("⚠️ **STATUS KEPUTUSAN: REKOMENDASI DIPERTIMBANGKAN**")
        st.info(f"**Interpretasi Analisis:** Mahasiswa memiliki nilai IPK sebesar **{ipk:.2f}**, yang menempatkannya pada posisi menengah (tengah grafik). Kategori keanggotaan tertingginya berada di himpunan **Dipertimbangkan** sebesar **{mu_dipertimbangkan:.2f}**. Sistem menyarankan agar mahasiswa ini dievaluasi lebih lanjut menggunakan berkas pendukung tambahan seperti piagam prestasi atau surat keterangan kurang mampu.")
    else:
        st.error("❌ **STATUS KEPUTUSAN: REKOMENDASI TIDAK LAYAK MENERIMA BEASISWA**")
        st.info(f"**Interpretasi Analisis:** Berdasarkan hasil pemetaan, mahasiswa dengan IPK **{ipk:.2f}** memiliki tingkat keanggotaan dominan pada himpunan **Tidak Layak** sebesar **{mu_tidak_layak:.2f}**. Nilai akademik belum memenuhi batas ambang standar minimum kelayakan program kualifikasi beasiswa saat ini.")

# ==========================================
# KOLOM 2: GRAFIK & DOKUMENTASI FUNGSI
# ==========================================
with col2:
    st.header("📊 [4] Grafik Himpunan Fuzzy")
    st.write("Posisi garis ungu putus-putus menunjukkan letak nilai IPK kamu saat ini:")
    
    # Generate data kurva untuk visualisasi plot
    x = np.linspace(0, 4, 500)
    y_tidak_layak = np.piecewise(x, [x <= 1.5, (x > 1.5) & (x < 2.5), x >= 2.5], [1, lambda x: (2.5 - x)/(2.5 - 1.5), 0])
    y_dipertimbangkan = np.piecewise(x, [(x >= 1.5) & (x <= 2.5), (x > 2.5) & (x <= 3.5)], [lambda x: (x - 1.5)/(2.5 - 1.5), lambda x: (3.5 - x)/(3.5 - 2.5), 0])
    y_layak = np.piecewise(x, [x <= 2.5, (x > 2.5) & (x < 3.5), x >= 3.5], [0, lambda x: (x - 2.5)/(3.5 - 2.5), 1])

    # Plotting Menggunakan Matplotlib
    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.plot(x, y_tidak_layak, 'b-', label='Tidak Layak', linewidth=2.5)
    ax.plot(x, y_dipertimbangkan, 'g-', label='Dipertimbangkan', linewidth=2.5)
    ax.plot(x, y_layak, 'r-', label='Layak', linewidth=2.5)
    
    # Garis indikator nilai IPK user saat ini
    ax.axvline(x=ipk, color='purple', linestyle='--', alpha=0.8, label=f'IPK Input ({ipk:.2f})')
    ax.scatter([ipk], [nilai_maks], color='purple', s=60, zorder=5)

    ax.set_title("Kurva Fungsi Keanggotaan Kasus 2 (IPK)", fontsize=11, fontweight='bold')
    ax.set_xlabel("Nilai IPK", fontsize=9)
    ax.set_ylabel("Derajat Keanggotaan \mu(x)", fontsize=9)
    ax.set_xlim(0, 4.1)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc='lower left', fontsize=8)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    st.pyplot(fig)

    st.markdown("---")

    st.header("📐 [2] Dokumentasi Fungsi Keanggotaan")
    st.write("Berdasarkan grafik praktikum, berikut adalah pemodelan matematika formal yang ditanamkan ke sistem:")
    
    # Menampilkan Rumus Piecewise Linear untuk masing-masing Himpunan (Kriteria Nilai Fungsi)
    with st.tabs(["📉 Tidak Layak", "📉 Dipertimbangkan", "📈 Layak"]):
        with st.tab("📉 Tidak Layak"):
            st.write("Menggunakan Fungsi Keanggotaan Bahu Turun (Linier Turun):")
            st.latex(r"""
            \mu_{\text{Tidak Layak}}(x) = \begin{cases} 
            1, & x \le 1.5 \\ 
            \frac{2.5 - x}{2.5 - 1.5}, & 1.5 < x < 2.5 \\ 
            0, & x \ge 2.5 
            \end{cases}
            """)
        with st.tab("📉 Dipertimbangkan"):
            st.write("Menggunakan Fungsi Keanggotaan Segitiga (*Triangular Mf*):")
            st.latex(r"""
            \mu_{\text{Dipertimbangkan}}(x) = \begin{cases} 
            0, & x \le 1.5 \text{ atau } x \ge 3.5 \\ 
            \frac{x - 1.5}{2.5 - 1.5}, & 1.5 \le x \le 2.5 \\ 
            \frac{3.5 - x}{3.5 - 2.5}, & 2.5 < x \le 3.5 
            \end{cases}
            """)
        with st.tab("📈 Layak"):
            st.write("Menggunakan Fungsi Keanggotaan Bahu Naik (Linier Naik):")
            st.latex(r"""
            \mu_{\text{Layak}}(x) = \begin{cases} 
            0, & x \le 2.5 \\ 
            \frac{x - 2.5}{3.5 - 2.5}, & 2.5 < x < 3.5 \\ 
            1, & x \ge 3.5 
            \end{cases}
            """)

st.markdown("---")
st.caption("Aplikasi Praktikum Logika Fuzzy Berbasis Streamlit | Pengembang: Daffa Dzaki")
