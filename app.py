import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="Generator HACCP Otomatis",
    page_icon="🍳",
    layout="wide"
)

st.title("🛡️ Generator Dokumen HACCP Otomatis (12 Langkah)")
st.caption("Standar Keamanan Pangan Codex Alimentarius / SNI ISO 22000")

# Sidebar Input
st.sidebar.header("Pengaturan Operasional")
nama_menu = st.sidebar.text_input("Nama Bahan / Menu", value="Bayam")
nama_dapur = st.sidebar.text_input("Nama Fasilitas / Dapur", value="Dapur Satuan Pelayanan MBG")
penanggung_jawab = st.sidebar.text_input("Penanggung Jawab / Ketua Tim", value="Ishak Yunus")

# Logic Generator Berdasarkan Kategori Bahan
def generate_haccp_data(menu):
    m = menu.lower()
    
    # 1. Kategori Sayuran & Nabati
    if any(k in m for k in ["bayam", "kangkung", "sayur", "sop", "tumis", "tahu", "tempe", "wortel", "buncis"]):
        alergen = "Bebas alergen utama (kecuali kedelai jika ada Tahu/Tempe)."
        rentan = "Anak-anak, balita, lansia, dan individu dengan sistem imun rendah (sensitif terhadap residu pestisida & bakteri tanah)."
        penerimaan_bahaya = "Biologi: Kontaminasi Bacillus cereus & parasit tanah\nKimia: Residu pestisida\nFisik: Daun busuk, ulat, & tanah/pasir"
        penerimaan_batas = "Segar, bebas hama/ulat, tidak ada bau pembusukan, kondisi fisik utuh"
        
        tahap_ccp1 = "Pencucian & Perebusan/Pemasakan Sayur"
        bahaya_ccp1 = "Biologi: Kelangsungan hidup Bacillus cereus & kontaminasi silang tanah\nKimia: Residu pestisida"
        batas_ccp1 = "Pencucian air mengalir bersih & Pemasakan suhu inti >= 70°C"
        koreksi_ccp1 = "Cuci ulang dengan air bersih mengalir; lanjutkan pemanasan hingga matang"

    # 2. Kategori Daging / Ayam / Unggas
    elif any(k in m for k in ["ayam", "daging", "sapi", "kambing", "unggas"]):
        alergen = "Tidak mengandung alergen utama."
        rentan = "Balita, lansia, ibu hamil, dan individu imunokompromais (risiko infeksi Salmonella & Listeria)."
        penerimaan_bahaya = "Biologi: Salmonella spp., E. coli, & Listeria monocytogenes\nFisik: Bau lendir, memar, atau tekstur lembek"
        penerimaan_batas = "Suhu penerimaan Chiller <= 4°C atau Freezer <= -18°C, tidak berbau busuk"
        
        tahap_ccp1 = "Pemasakan / Ungkep / Goreng"
        bahaya_ccp1 = "Biologi: Kelangsungan hidup Salmonella spp. & E. coli"
        batas_ccp1 = "Suhu inti daging >= 74°C minimal 15 detik"
        koreksi_ccp1 = "Lanjutkan pemasakan hingga suhu inti mencapai >= 74°C"

    # 3. Kategori Ikan / Seafood
    elif any(k in m for k in ["ikan", "udang", "cumi", "seafood", "tongkol", "layang", "gurame"]):
        alergen = "MENGANDUNG ALERGEN UTAMA (IKAN / SEAFOOD)."
        rentan = "Individu dengan alergi makanan laut, balita, dan lansia."
        penerimaan_bahaya = "Biologi: Vibrio parahaemolyticus\nKimia: Histamin & Logam berat\nFisik: Mata suram, insang pucat"
        penerimaan_batas = "Ikan segar (mata jernih, kenyal), suhu penerimaan <= 4°C dengan es"
        
        tahap_ccp1 = "Pemasakan / Penggorengan / Perebusan Ikan"
        bahaya_ccp1 = "Biologi: Vibrio parahaemolyticus & Histamin (akibat pembusukan)"
        batas_ccp1 = "Suhu inti produk >= 74°C minimal 15 detik"
        koreksi_ccp1 = "Lanjutkan pemanasan; tolak ikan sejak awal jika sudah ada indikasi busuk"

    # 4. Kategori Telur / Default
    else:
        alergen = "MENGANDUNG ALERGEN UTAMA (TELUR)."
        rentan = "Balita, anak-anak, lansia, dan ibu hamil."
        penerimaan_bahaya = "Biologi: Salmonella enteritidis pada cangkang\nFisik: Cangkang retak, kotoran menempel"
        penerimaan_batas = "Cangkang bersih, utuh, tidak retak, tidak berbau busuk"
        
        tahap_ccp1 = "Pemasakan / Pengolahan Telur"
        bahaya_ccp1 = "Biologi: Kelangsungan hidup Salmonella enteritidis"
        batas_ccp1 = "Suhu inti produk >= 74°C (putih & kuning telur memadat)"
        koreksi_ccp1 = "Lanjutkan pemanasan hingga telur matang sempurna"

    return alergen, rentan, penerimaan_bahaya, penerimaan_batas, tahap_ccp1, bahaya_ccp1, batas_ccp1, koreksi_ccp1

# Jalankan Logika Deteksi
alergen_info, rentan_info, pen_bahaya, pen_batas, ccp1_tahap, ccp1_bahaya, ccp1_batas, ccp1_koreksi = generate_haccp_data(nama_menu)

# Tampilan Utama
st.header(f"📋 Rencana HACCP: {nama_menu}")
st.subheader(f"Fasilitas: {nama_dapur} | PJ: {penanggung_jawab}")

tab1, tab2, tab3 = st.tabs(["5 Langkah Persiapan", "7 Prinsip HACCP", "Ekspor Dokumen"])

with tab1:
    st.subheader("I. 5 Langkah Persiapan (Preliminary Steps)")
    
    st.markdown("### 1. Tim HACCP & Tanggung Jawab")
    df_tim = pd.DataFrame([
        {"Peran": "Ketua Tim HACCP", "Nama / Jabatan": penanggung_jawab, "Tanggung Jawab": "Validasi dokumen, verifikasi sistem, koordinasi audit."},
        {"Peran": "Kepala Masak (Head Chef)", "Nama / Jabatan": "Tim Produksi", "Tanggung Jawab": "Pengawasan CCP prapemasakan & pemasakan."},
        {"Peran": "Koordinator Logistik", "Nama / Jabatan": "Tim Penerimaan", "Tanggung Jawab": "Inspeksi visual & penerimaan bahan baku."},
        {"Peran": "Petugas Hygiene & Sanitasi", "Nama / Jabatan": "Tim Sanitasi", "Tanggung Jawab": "Sanitasi peralatan, ruangan, dan hygiene personal."}
    ])
    st.table(df_tim)

    st.markdown("### 2. Deskripsi Produk Lengkap")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Nama Produk:** {nama_menu}")
        st.markdown(f"**Komposisi Utama:** {nama_menu} (100% Bahan Tunggal)")
        st.markdown("**Karakteristik Biokimia:** Aw > 0.92, pH 5.5 - 6.8 (Risiko tinggi mikroba)")
    with col2:
        st.markdown("**Metode Pengolahan:** Persiapan, Pemotongan/Pencucian, & Pemasakan Termal")
        st.markdown("**Kemasan:** Ompreng (Food Grade)")
        st.markdown("**Masa Simpan:** Max 2 jam (Suhu Ruang), Max 4 jam (Hot Warmer >= 60°C)")

    st.markdown("### 3. Rencana Penggunaan (Intended Use) & Analisis Risiko Konsumen")
    st.info(f'''
    - **Target Konsumen:** Konsumen umum (Anak sekolah, pekerja, dewasa, lansia).
    - **Kelompok Rentan (Vulnerable Group):** {rentan_info}
    - **Status Alergen:** {alergen_info}
    - **Cara Penyajian:** Siap santap (Ready-to-Eat / RTE).
    - **Potensi Penyalahgunaan:** Disimpan pada suhu ruang > 2 jam tanpa pemanasan ulang.
    ''')

    st.markdown("### 4. Diagram Alir Proses")
    st.code(f'''
[ Penerimaan {nama_menu} ] -> [ Penyimpanan Segar / Chiller ]
                                     │
                                     ▼
[ Pemorsian & Hot Holding >= 60°C ] <- [ {ccp1_tahap} (CCP 1) ] <- [ Persiapan / Pencucian / Penimbangan ]
         │
         ▼
[ Pendistribusian & Penyajian (CCP 2) ]
    ''')

    st.markdown("### 5. Verifikasi Diagram Alir")
    st.write("Tim HACCP telah melakukan pengamatan alur proses secara langsung di lapangan untuk memastikan diagram alir sesuai dengan operasional riil dapur.")

with tab2:
    st.subheader("II. 7 Prinsip HACCP (Analisis Utama)")

    df_haccp = pd.DataFrame([
        {
            "Tahap Proses": f"Penerimaan {nama_menu}",
            "Bahaya Potensial": pen_bahaya,
            "Kategori CCP": "PRP / GHP",
            "Batas Kritis": pen_batas,
            "Pemantauan (Monitoring)": "Inspeksi visual & cek kondisi fisik tiap penerimaan",
            "Tindakan Koreksi": "Tolak bahan baku jika rusak, kotor, atau tidak sesuai standar"
        },
        {
            "Tahap Proses": ccp1_tahap,
            "Bahaya Potensial": ccp1_bahaya,
            "Kategori CCP": "CCP 1",
            "Batas Kritis": ccp1_batas,
            "Pemantauan (Monitoring)": "Ukur suhu inti pemanasan & pantau waktu pencucian/pemasakan",
            "Tindakan Koreksi": ccp1_koreksi
        },
        {
            "Tahap Proses": "Holding & Pemorsian",
            "Bahaya Potensial": "Biologi: Rekontaminasi & pertumbuhan Bacillus cereus/Staphylococcus",
            "Kategori CCP": "CCP 2",
            "Batas Kritis": "Suhu warmer >= 60°C atau max 2 jam di suhu ruang",
            "Pemantauan (Monitoring)": "Cek display suhu warmer & catat jam selesai masak",
            "Tindakan Koreksi": "Panaskan ulang ke 74°C jika < 60°C; buang jika > 2 jam suhu ruang"
        }
    ])
    st.table(df_haccp)

    st.markdown("### Prosedur Verifikasi & Dokumentasi")
    st.markdown("- **Verifikasi:** Pemeriksaan log harian oleh Supervisor, kalibrasi termometer mingguan, uji sampel lab mikrobiologi bulanan.")
    st.markdown("- **Dokumentasi Wajib:** Form Penerimaan Bahan, Log Suhu Pemasakan (CCP 1), Log Suhu Holding (CCP 2), & Form Tindakan Korektif.")

with tab3:
    st.subheader("📤 Ekspor Dokumen HACCP")
    st.write("Unduh dokumen ini untuk arsip operasional dan keperluan audit resmi.")
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_tim.to_excel(writer, sheet_name='5 Langkah - Tim', index=False)
        df_haccp.to_excel(writer, sheet_name='7 Prinsip HACCP', index=False)
    
    st.download_button(
        label="📊 Unduh Format Excel (.xlsx)",
        data=buffer.getvalue(),
        file_name=f"HACCP_Plan_{nama_menu.replace(' ', '_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
