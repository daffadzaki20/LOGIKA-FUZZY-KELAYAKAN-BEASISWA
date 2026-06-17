import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set halaman Streamlit
st.set_page_config(page_title="Fuzzy Beasiswa - Kasus 2", layout="wide")

st.title("🎛️ Aplikasi Logika Fuzzy - Kelayakan Beasiswa (Kasus 2)")
st.markdown("Aplikasi ini menghitung tingkat kelayakan beasiswa mahasiswa berdasarkan input **IPK** menggunakan prinsip Logika Fuzzy.")

# Tampilan dibagi menjadi 2 kolom
col1, col2 = st.columns([1, 1.2])

with col1:
    st.header("1. Input Data & Perhitungan")
    # Input IPK via Slider
    ipk = st.slider("Masukkan IPK Mahasiswa:", min_value=0.00, max_value=4.00, value=2.50, step=0.01)

    # --- FUZZIFIKASI (Menghitung Derajat Keanggotaan) ---
    # 1. Tidak Layak
    if ipk <= 1.5:
        mu_tidak_layak = 1.0
    elif 1.5 < ipk < 2.5:
        mu_tidak_layak = (2.5 - ipk) / (2.5 - 1.5)
    else:
        mu_tidak_layak = 0.0

    # 2. Dipertimbangkan
    if 1.5 <= ipk <= 2.5:
        mu_dipertimbangkan = (ipk - 1.5) / (2.5 - 1.5)
    elif 2.5 < ipk <= 3.5:
        mu_dipertimbangkan = (3.5 - ipk) / (3.5 - 2.5)
    else:
        mu_dipertimbangkan = 0.0

    # 3. Layak
    if ipk <= 2.5:
        mu_layak = 0.0
    elif 2.5 < ipk < 3.5:
        mu_layak = (ipk - 2.5) / (3.5 - 2.5)
    else:
        mu_layak = 1.0

    st.subheader("Hasil Nilai Keanggotaan (μ):")
    st.write(f"- **μ Tidak Layak**: {mu_tidak_layak:.2f}")
    st.write(f"- **μ Dipertimbangkan**: {mu_dipertimbangkan:.2f}")
    st.write(f"- **μ Layak**: {mu_layak:.2f}")

    # --- INFERENSI & DEFUZZIFIKASI ---
    st.subheader("2. Kesimpulan Output")
    
    nilai_maks = max(mu_tidak_layak, mu_dipertimbangkan, mu_layak)
    
    if nilai_maks == 0:
        st.error("Status: Tidak Terdefinisi")
    elif nilai_maks == mu_layak:
        st.success("🎉 REKOMENDASI: LAYAK MENERIMA BEASISWA")
    elif nilai_maks == mu_dipertimbangkan:
        st.warning("⚠️ REKOMENDASI: DIPERTIMBANGKAN (Perlu Seleksi Berkas Lanjutan)")
    else:
        st.error("❌ REKOMENDASI: TIDAK LAYAK MENERIMA BEASISWA")

with col2:
    st.header("2. Visualisasi Grafik Keanggotaan")
    
    x = np.linspace(0, 4, 500)
    
    # Pola grafik sesuai gambar Kasus 2 Tugas Praktikum
    y_tidak_layak = np.piecewise(x, [x <= 1.5, (x > 1.5) & (x < 2.5), x >= 2.5], [1, lambda x: (2.5 - x)/(2.5 - 1.5), 0])
    y_dipertimbangkan = np.piecewise(x, [(x >= 1.5) & (x <= 2.5), (x > 2.5) & (x <= 3.5)], [lambda x: (x - 1.5)/(2.5 - 1.5), lambda x: (3.5 - x)/(3.5 - 2.5), 0])
    y_layak = np.piecewise(x, [x <= 2.5, (x > 2.5) & (x < 3.5), x >= 3.5], [0, lambda x: (x - 2.5)/(3.5 - 2.5), 1])

    fig, ax = plt.subplots(figsize=(6, 4))
    
    ax.plot(x, y_tidak_layak, 'b-', label='Tidak Layak', linewidth=2)
    ax.plot(x, y_dipertimbangkan, 'g-', label='Dipertimbangkan', linewidth=2)
    ax.plot(x, y_layak, 'r-', label='Layak', linewidth=2)
    
    ax.axvline(x=ipk, color='purple', linestyle='--', label=f'IPK Anda ({ipk:.2f})')
    ax.scatter([ipk], [nilai_maks], color='purple', s=50, zorder=5)

    ax.set_title("Fungsi Keanggotaan IPK (Domain: 0.00 - 4.00)")
    ax.set_xlabel("IPK")
    ax.set_ylabel("μ(x)")
    ax.set_xlim(0, 4.1)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc='upper left')
    ax.grid(True, linestyle=':', alpha=0.6)
    
    st.pyplot(fig)
