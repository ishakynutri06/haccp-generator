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

# Sidebar Menu
st.sidebar.header("Pengaturan Operasional")
nama_menu = st.sidebar.text_input("Nama Bahan / Menu", value="Telur Dadar")
nama_dapur = st.sidebar.text_input("Nama Fasilitas / Dapur", value="Dapur Satuan Pelayanan MBG")
penanggung_jawab = st.sidebar.text_input("Penanggung Jawab / Ketua Tim", value="Ishak Yunus")

btn_generate = st.sidebar.button("🚀 Hasilkan Laporan HACCP", type="primary")

if btn_generate or nama_menu:
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
            st.markdown("**Komposisi Utama:** Telur Ayam Segar, Minyak Goreng, Garam, Bumbu")
            st.markdown("**Karakteristik Biokimia:** Aw > 0.95, pH 6.5 - 7.0 (Risiko tinggi mikroba)")
        with col2:
            st.markdown("**Metode Pengolahan:** Pengocokan adonan & Penggorengan")
            st.markdown("**Kemasan:** Insulated Stainless Container / Food Grade Box")
            st.markdown("**Masa Simpan:** Max 2 jam (Suhu Ruang), Max 4 jam (Hot Warmer >= 60°C)")

        st.markdown("### 3. Rencana Penggunaan (Intended Use) & Analisis Risiko Konsumen")
        st.info('''
        - **Target Konsumen:** Konsumen umum (Anak sekolah, pekerja, dewasa, lansia).
        - **Kelompok Rentan (Vulnerable Group):** Balita, lansia, ibu hamil wajib menerima produk matang sempurna (suhu inti >= 74°C) untuk mencegah *Salmonella enteritidis*.
        - **Status Alergen:** **MENGANDUNG ALERGEN UTAMA (TELUR)**. Dapat memicu reaksi alergi protein telur (ovalbumin).
        - **Cara Penyajian:** Siap santap (Ready-to-Eat / RTE).
        - **Potensi Penyalahgunaan:** Disimpan pada suhu ruang > 2 jam tanpa pemanasan ulang, atau dikonsumsi dingin setelah terkontaminasi lingkungan.
        ''')

        st.markdown("### 4. Diagram Alir Proses")
        st.code('''
[ Penerimaan Telur Utuh & Bahan ] -> [ Penyimpanan Cold Room / Sejuk ]
                                              │
                                              ▼
[ Pemorsian & Hot Holding >= 60°C ] <- [ Pemasakan / Penggorengan >= 74°C (CCP 1) ] <- [ Pemecahan & Pengocokan ]
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
                "Tahap Proses": "Penerimaan Telur Utuh",
                "Bahaya Potensial": "Biologi: Salmonella spp.\nFisik: Cangkang retak, kotoran",
                "Kategori CCP": "PRP / GHP",
                "Batas Kritis": "Cangkang utuh, bersih, bebas kotoran, tanggal segar",
                "Pemantauan (Monitoring)": "Visual inspeksi tiap lot oleh Tim Logistik",
                "Tindakan Koreksi": "Tolak pengiriman jika retak/kotor berat"
            },
            {
                "Tahap Proses": "Pemasakan / Penggorengan",
                "Bahaya Potensial": "Biologi: Kelangsungan hidup Salmonella spp.",
                "Kategori CCP": "CCP 1",
                "Batas Kritis": "Suhu inti dadar >= 74°C selama minimal 15 detik",
                "Pemantauan (Monitoring)": "Ukur suhu inti dengan probe thermometer tiap batch",
                "Tindakan Koreksi": "Lanjutkan pemasakan hingga mencapai suhu >= 74°C"
            },
            {
                "Tahap Proses": "Holding & Pemorsian",
                "Bahaya Potensial": "Biologi: Rekontaminasi & pertumbuhan Bacillus cereus",
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
