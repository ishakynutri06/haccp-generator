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
nama_menu = st.sidebar.text_input("Nama Bahan / Menu", value="Ayam Goreng")
nama_dapur = st.sidebar.text_input("Nama Fasilitas / Dapur", value="Dapur Satuan Pelayanan MBG")
penanggung_jawab = st.sidebar.text_input("Penanggung Jawab / Ketua Tim", value="Ishak Yunus")

# Logic Generator Berdasarkan Katagori Bahan
def generate_haccp_data(menu):
    menu_lower = menu.lower()
    
    # Kategori: Daging / Ayam
    if any(k in menu_lower for k in ["ayam", "daging", "sapi", "kambing", "unggas"]):
        alergen = "Tidak mengandung alergen utama (kecuali ada tambahan bumbu/kemiri/kedelai)."
        rentan = "Balita, lansia, dan ibu hamil wajib menerima daging matang sempurna (suhu inti >= 74°C) untuk mencegah Salmonella spp. dan Campylobacter."
        tahap_ccp1 = "Pemasakan / Ungkep / Goreng"
        bahaya_ccp1 = "Biologi: Kelangsungan hidup Salmonella spp., E. coli, & Listeria monocytogenes"
        batas_ccp1 = "Suhu inti daging >= 74°C minimal 15 detik"
        koreksi_ccp1 = "Lanjutkan pemasakan hingga suhu inti mencapai >= 74°C"
        
    # Kategori: Ikan / Seafood
    elif any(k in menu_lower for k in ["ikan", "udang", "cumi", "seafood", "tongkol", "layang"]):
        alergen = "MENGANDUNG ALERGEN UTAMA (IKAN / SEAFOOD)."
        rentan = "Wajib dipastikan kesegarannya (bebas histamin) dan dimasak matang sempurna."
        tahap_ccp1 = "Pemasakan / Penggorengan / Perebusan"
        bahaya_ccp1 = "Biologi: Vibrio parahaemolyticus & Histamin (akibat pembusukan awal)"
        batas_ccp1 = "Suhu inti produk >= 74°C minimal 15 detik"
        koreksi_ccp1 = "Lanjutkan pemasakan hingga matang sempurna; tolak ikan jika bau busuk di awal penerimaan"

    # Kategori: Sayuran / Tahu / Tempe
    elif any(k in menu_lower for k in ["sayur", "tahu", "tempe", "tumis", "sop", "bayam", "kangkung"]):
        alergen = "Mengandung Kedelai (pada Tahu/Tempe). Bebas alergen untuk sayuran murni."
        rentan = "Sayuran harus dicuci bersih dengan air mengalir untuk menghilangkan residu pestisida & tanah."
        tahap_ccp1 = "Pencucian & Pemasakan"
        bahaya_ccp1 = "Kimia: Residu pestisida / Biologi: Bacillus cereus & kontaminasi tanah"
        batas_ccp1 = "Pencucian air mengalir & Pemasakan suhu inti >= 70°C"
        koreksi_ccp1 = "Cuci ulang dengan air mengalir / Lanjutkan pemanasan"

    # Default / Terigu / Telur / Lainnya
    else:
        alergen = "MENGANDUNG ALERGEN UTAMA (TELUR / PROTEIN)."
        rentan = "Balita dan lansia wajib menerima produk matang sempurna (suhu inti >= 74°C)."
        tahap_ccp1 = "Pemasakan / Pengolahan Utama"
        bahaya_ccp1 = "Biologi: Salmonella spp. & Staphylococcal enterotoxin"
        batas_ccp1 = "Suhu inti produk >= 74°C minimal 15 detik"
        koreksi_ccp1 = "Lanjutkan pemanasan hingga mencapai suhu >= 74°C"

    return alergen, rentan, tahap_ccp1, bahaya_ccp1, batas_ccp1, koreksi_ccp1

alergen_info, rentan_info, ccp1_tahap, ccp1_bahaya, ccp1_batas, ccp1_koreksi = generate_haccp_data(nama_menu)

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
        st.markdown(f"**Komposisi Utama:** {nama_menu}, Bumbu, Minyak Goreng, Garam")
        st.markdown("**Karakteristik Biokimia:** Aw > 0.92, pH 5.5 - 6.8 (Risiko tinggi mikroba)")
    with col2:
        st.markdown("**Metode Pengolahan:** Persiapan, Pemotongan/Pembersihan, & Pemasakan Termal")
        st.markdown("**Kemasan:** Insulated Stainless Container / Food Grade Box")
        st.markdown("**Masa Simpan:** Max 2 jam (Suhu Ruang), Max 4 jam (Hot Warmer >= 60°C)")

    st.markdown("### 3. Rencana Penggunaan (Intended Use) & Analisis Risiko Konsumen")
    st.info(f'''
    - **Target Konsumen:** Konsumen umum (Anak sekolah, pekerja, dewasa, lansia).
    - **Kelompok Rentan (Vulnerable Group):** {rentan_info}
    - **Status Alergen:** {alergen_info}
    - **Cara Penyajian:** Siap santap (Ready-to-Eat / RTE).
    - **Potensi Penyalahgunaan:** Disimpan pada suhu ruang > 2 jam tanpa pemanasan ulang, atau dikonsumsi dingin setelah terkontaminasi lingkungan.
    ''')

    st.markdown("### 4. Diagram Alir Proses")
    st.code(f'''
[ Penerimaan {nama_menu} ] -> [ Penyimpanan Cold Room / Chiller ]
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
            "Bahaya Potensial": "Biologi: Kontaminasi awal mikroba patogen\nFisik: Benda asing, fisik rusak/busuk",
            "Kategori CCP": "PRP / GHP",
            "Batas Kritis": "Karakteristik fisik segar, suhu penerimaan sesuai standar (Chiller <= 4°C)",
            "Pemantauan (Monitoring)": "Visual inspeksi & cek suhu penerimaan tiap lot",
            "Tindakan Koreksi": "Tolak pengiriman jika busuk/rusak/suhu tidak sesuai"
        },
        {
            "Tahap Proses": ccp1_tahap,
            "Bahaya Potensial": ccp1_bahaya,
            "Kategori CCP": "CCP 1",
            "Batas Kritis": ccp1_batas,
            "Pemantauan (Monitoring)": "Ukur suhu inti dengan probe thermometer tiap batch",
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
