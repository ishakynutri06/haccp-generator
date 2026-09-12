import streamlit as st
import pandas as pd
import requests
import json
import io
import re
from datetime import datetime
from urllib.parse import quote

from openai import OpenAI

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image
)


# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="Generator HACCP Per Bahan",
    page_icon="🧪",
    layout="wide"
)


# =========================================================
# FUNGSI DASAR
# =========================================================

def clean_filename(text):
    """
    Mengubah nama bahan menjadi nama file yang aman.
    """
    text = str(text).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def get_openai_client():
    """
    Mengambil API Key dari Streamlit Secrets atau input pengguna.
    """
    api_key = None

    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        api_key = None

    if not api_key:
        api_key = st.session_state.get("api_key")

    if not api_key:
        return None

    return OpenAI(api_key=api_key)


# =========================================================
# PENCARIAN WIKIPEDIA INDONESIA
# =========================================================

def search_wikipedia_image(ingredient):
    """
    Mencari gambar dan ringkasan bahan melalui Wikipedia Bahasa Indonesia.
    Menggunakan REST API Wikipedia.
    """

    try:
        title = quote(ingredient.replace(" ", "_"))

        url = (
            "https://id.wikipedia.org/api/rest_v1/page/summary/"
            + title
        )

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "HACCP-SPPG-Generator/1.0"
            }
        )

        if response.status_code != 200:
            return {
                "title": ingredient,
                "description": "",
                "image": None,
                "wikipedia_url": (
                    "https://id.wikipedia.org/wiki/"
                    + title
                )
            }

        data = response.json()

        image_url = None

        if data.get("thumbnail"):
            image_url = data["thumbnail"].get("source")

        return {
            "title": data.get("title", ingredient),
            "description": data.get("extract", ""),
            "image": image_url,
            "wikipedia_url": data.get(
                "content_urls",
                {}
            ).get(
                "desktop",
                {}
            ).get(
                "page",
                "https://id.wikipedia.org/wiki/" + title
            )
        }

    except Exception as error:
        return {
            "title": ingredient,
            "description": "",
            "image": None,
            "wikipedia_url": (
                "https://id.wikipedia.org/wiki/"
                + quote(ingredient.replace(" ", "_"))
            ),
            "error": str(error)
        }


# =========================================================
# PROMPT AI HACCP
# =========================================================

def build_haccp_prompt(
    ingredient,
    facility,
    responsible_person,
    intended_use,
    process_description,
    vulnerable_groups,
    wikipedia_description
):
    """
    Membuat instruksi detail kepada AI.
    """

    return f"""
Anda adalah konsultan HACCP dan keamanan pangan yang memahami:

- Codex Alimentarius HACCP;
- 5 tugas pendahuluan HACCP;
- 7 prinsip HACCP;
- Good Hygiene Practices/GHP;
- Good Manufacturing Practices/GMP;
- pendekatan PRP, OPRP dan CCP;
- proses produksi makanan skala besar;
- kondisi operasional dapur MBG/SPPG di Indonesia.

Buatkan DOKUMEN HACCP PER BAHAN secara rinci, jelas, praktis dan mudah diterapkan.

DATA INPUT:

Nama bahan:
{ingredient}

Nama dapur/SPPG:
{facility}

Penanggung jawab:
{responsible_person}

Tujuan penggunaan:
{intended_use}

Kelompok penerima manfaat:
{vulnerable_groups}

Gambaran proses:
{process_description}

Informasi tambahan dari Wikipedia:
{wikipedia_description}

PENTING:

1. Jangan mengarang seolah-olah semua batas kritis sudah resmi.
2. Bedakan antara:
   - batas kritis yang harus divalidasi;
   - target operasional;
   - rekomendasi pengendalian;
   - persyaratan yang harus mengikuti peraturan Indonesia.
3. Jangan langsung menyatakan semua tahapan sebagai CCP.
4. Gunakan pendekatan decision tree untuk menentukan:
   - PRP;
   - OPRP;
   - CCP kandidat.
5. Jika data suhu, pH, Aw, waktu, atau ukuran bahan tidak tersedia, tulis:
   "Harus diverifikasi/diukur di lapangan".
6. Jangan menetapkan nilai pH atau Aw tanpa data pengukuran.
7. Jelaskan bahaya biologis, kimia, fisik dan alergen.
8. Sesuaikan analisis dengan jenis bahan.
9. Jelaskan risiko untuk:
   - anak sekolah;
   - balita;
   - ibu hamil/menyusui;
   - kelompok rentan lainnya jika relevan.
10. Gunakan bahasa Indonesia yang mudah dipahami oleh tim dapur.

HASIL WAJIB DALAM FORMAT JSON VALID DENGAN STRUKTUR BERIKUT:

{{
  "identitas_bahan": {{
    "nama_bahan": "",
    "nama_lain": "",
    "kategori_bahan": "",
    "deskripsi": "",
    "asal_sumber": "",
    "karakteristik_penting": "",
    "potensi_alergen": "",
    "kelompok_rentan": "",
    "tujuan_penggunaan": ""
  }},

  "tugas_pendahuluan": {{
    "tim_haccp": [],
    "deskripsi_produk": "",
    "penggunaan_yang_dimaksud": "",
    "diagram_alir": [],
    "verifikasi_diagram_alir": []
  }},

  "analisis_bahaya": [
    {{
      "tahap": "",
      "bahaya_biologis": "",
      "bahaya_kimia": "",
      "bahaya_fisik": "",
      "bahaya_alergen": "",
      "penyebab": "",
      "tingkat_risiko": "",
      "tindakan_pengendalian": "",
      "kategori_pengendalian": "PRP/OPRP/CCP kandidat",
      "alasan": ""
    }}
  ],

  "penerimaan_bahan": {{
    "kondisi_kemasan": "",
    "kondisi_kendaraan": "",
    "kondisi_sensoris": "",
    "suhu_penerimaan": "",
    "dokumen_pemasok": "",
    "kriteria_ditolak": "",
    "tindakan_jika_tidak_sesuai": ""
  }},

  "penyimpanan": {{
    "jenis_penyimpanan": "",
    "suhu_target": "",
    "batas_waktu": "",
    "pemisahan_bahan": "",
    "fifo_fefo": "",
    "risiko_kontaminasi_silang": "",
    "monitoring": ""
  }},

  "persiapan_bahan": {{
    "sortasi": "",
    "pencucian": "",
    "sanitasi": "",
    "pemotongan": "",
    "alat_dan_apd": "",
    "pencegahan_kontaminasi_silang": ""
  }},

  "proses_pengolahan": {{
    "metode": "",
    "parameter_penting": "",
    "suhu_inti": "",
    "waktu_proses": "",
    "indikator_kematangan": "",
    "risiko_jika_tidak_sesuai": "",
    "tindakan_koreksi": ""
  }},

  "penentuan_ccp": [
    {{
      "tahap": "",
      "pertanyaan_decision_tree": "",
      "hasil": "",
      "status": "PRP/OPRP/CCP kandidat",
      "alasan": "",
      "validasi_yang_diperlukan": ""
    }}
  ],

  "rencana_ccp": [
    {{
      "nomor_ccp": "",
      "tahap": "",
      "bahaya_signifikan": "",
      "batas_kritis": "",
      "dasar_penentuan": "",
      "cara_monitoring": "",
      "frekuensi": "",
      "penanggung_jawab": "",
      "tindakan_koreksi": "",
      "verifikasi": "",
      "rekaman": ""
    }}
  ],

  "monitoring_dan_verifikasi": [
    {{
      "parameter": "",
      "metode_pemeriksaan": "",
      "frekuensi": "",
      "penanggung_jawab": "",
      "formulir_rekaman": "",
      "verifikasi": ""
    }}
  ],

  "tindakan_koreksi_umum": [
    {{
      "ketidaksesuaian": "",
      "tindakan_langsung": "",
      "penanganan_produk": "",
      "pencegahan_berulang": ""
    }}
  ],

  "dokumen_rekaman": [
    "",
    "",
    ""
  ],

  "catatan_validasi": [
    "",
    "",
    ""
  ],

  "kesimpulan": ""
}}

Hanya kembalikan JSON valid tanpa markdown dan tanpa penjelasan tambahan.
"""


# =========================================================
# PEMANGGILAN AI
# =========================================================

def generate_haccp_with_ai(
    ingredient,
    facility,
    responsible_person,
    intended_use,
    process_description,
    vulnerable_groups,
    wikipedia_description
):
    """
    Mengirim prompt ke AI dan membaca hasil JSON.
    """

    client = get_openai_client()

    if client is None:
        raise ValueError(
            "OPENAI_API_KEY belum dimasukkan."
        )

    prompt = build_haccp_prompt(
        ingredient=ingredient,
        facility=facility,
        responsible_person=responsible_person,
        intended_use=intended_use,
        process_description=process_description,
        vulnerable_groups=vulnerable_groups,
        wikipedia_description=wikipedia_description
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "system",
                "content": (
                    "Anda adalah ahli HACCP. "
                    "Jawab hanya dalam JSON valid."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    return json.loads(content)


# =========================================================
# KONVERSI DATA JSON KE DATAFRAME
# =========================================================

def list_to_dataframe(data):
    """
    Mengubah list dictionary menjadi DataFrame.
    """
    if not data:
        return pd.DataFrame()

    if isinstance(data[0], dict):
        return pd.DataFrame(data)

    return pd.DataFrame({
        "Keterangan": data
    })


def flatten_simple_dict(data):
    """
    Mengubah dictionary sederhana menjadi tabel.
    """
    rows = []

    for key, value in data.items():
        if isinstance(value, list):
            value = "\n".join(
                [str(item) for item in value]
            )

        elif isinstance(value, dict):
            value = json.dumps(
                value,
                ensure_ascii=False,
                indent=2
            )

        rows.append({
            "Parameter": key,
            "Keterangan": value
        })

    return pd.DataFrame(rows)


# =========================================================
# EXPORT EXCEL
# =========================================================

def create_excel_file(haccp_data, wiki_data, metadata):
    """
    Membuat file Excel dengan banyak sheet.
    """

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        # Sheet identitas
        identity_rows = []

        for key, value in metadata.items():
            identity_rows.append({
                "Parameter": key,
                "Keterangan": value
            })

        pd.DataFrame(identity_rows).to_excel(
            writer,
            sheet_name="Identitas",
            index=False
        )

        # Informasi Wikipedia
        wiki_rows = [
            {
                "Judul Wikipedia": wiki_data.get("title", ""),
                "Ringkasan": wiki_data.get("description", ""),
                "URL": wiki_data.get("wikipedia_url", "")
            }
        ]

        pd.DataFrame(wiki_rows).to_excel(
            writer,
            sheet_name="Wikipedia",
            index=False
        )

        # Semua bagian HACCP
        for section_name, section_data in haccp_data.items():

            sheet_name = section_name[:31]

            if isinstance(section_data, dict):
                df = flatten_simple_dict(
                    section_data
                )

            elif isinstance(section_data, list):
                df = list_to_dataframe(
                    section_data
                )

            else:
                df = pd.DataFrame({
                    "Keterangan": [section_data]
                })

            if df.empty:
                df = pd.DataFrame({
                    "Keterangan": [
                        "Tidak ada data"
                    ]
                })

            df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False
            )

    output.seek(0)

    return output


# =========================================================
# PDF HELPER
# =========================================================

def paragraph_text(value):
    """
    Membersihkan teks untuk ReportLab.
    """
    if value is None:
        return ""

    value = str(value)

    value = value.replace("&", "&amp;")
    value = value.replace("<", "&lt;")
    value = value.replace(">", "&gt;")
    value = value.replace("\n", "<br/>")

    return value


def dataframe_to_pdf_table(df, styles):
    """
    Mengubah DataFrame menjadi tabel PDF.
    """

    if df.empty:
        return Paragraph(
            "Tidak ada data.",
            styles["Normal"]
        )

    columns = list(df.columns)

    table_data = [
        [
            Paragraph(
                paragraph_text(column),
                styles["TableHeader"]
            )
            for column in columns
        ]
    ]

    for _, row in df.iterrows():
        table_data.append([
            Paragraph(
                paragraph_text(row[column]),
                styles["Small"]
            )
            for column in columns
        ])

    table = Table(
        table_data,
        repeatRows=1,
        colWidths=None
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#D9EAD3")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.black
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.grey
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                4
            )
        ])
    )

    return table


def create_pdf_file(
    haccp_data,
    wiki_data,
    metadata
):
    """
    Membuat laporan PDF HACCP.
    """

    output = io.BytesIO()

    doc = SimpleDocTemplate(
        output,
        pagesize=landscape(A4),
        rightMargin=1.2 * cm,
        leftMargin=1.2 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="TitleCenter",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=18,
            leading=22
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableHeader",
            parent=styles["Normal"],
            fontSize=7,
            leading=9,
            alignment=TA_CENTER
        )
    )

    styles.add(
        ParagraphStyle(
            name="Small",
            parent=styles["Normal"],
            fontSize=6.5,
            leading=8
        )
    )

    story = []

    ingredient = metadata.get(
        "Nama bahan",
        "Bahan"
    )

    story.append(
        Paragraph(
            "DOKUMEN HACCP PER BAHAN",
            styles["TitleCenter"]
        )
    )

    story.append(
        Paragraph(
            paragraph_text(
                f"Nama bahan: {ingredient}"
            ),
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            paragraph_text(
                f"Nama dapur/SPPG: "
                f"{metadata.get('Nama dapur/SPPG', '')}"
            ),
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            paragraph_text(
                f"Penanggung jawab: "
                f"{metadata.get('Penanggung jawab', '')}"
            ),
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            paragraph_text(
                f"Tanggal dokumen: "
                f"{metadata.get('Tanggal', '')}"
            ),
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 10))

    if wiki_data.get("description"):
        story.append(
            Paragraph(
                "<b>Ringkasan Wikipedia:</b><br/>"
                + paragraph_text(
                    wiki_data.get("description")
                ),
                styles["Normal"]
            )
        )

    story.append(
        Paragraph(
            "<b>Sumber gambar/informasi:</b> "
            + paragraph_text(
                wiki_data.get("wikipedia_url", "")
            ),
            styles["Small"]
        )
    )

    story.append(Spacer(1, 12))

    for section_name, section_data in haccp_data.items():

        story.append(
            Paragraph(
                paragraph_text(
                    section_name.replace("_", " ").upper()
                ),
                styles["Heading2"]
            )
        )

        if isinstance(section_data, dict):
            df = flatten_simple_dict(
                section_data
            )

        elif isinstance(section_data, list):
            df = list_to_dataframe(
                section_data
            )

        else:
            df = pd.DataFrame({
                "Keterangan": [section_data]
            })

        story.append(
            dataframe_to_pdf_table(
                df,
                styles
            )
        )

        story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>CATATAN PENTING:</b> "
            "Dokumen ini merupakan draft hasil bantuan AI. "
            "Semua bahaya, CCP, suhu, waktu, batas kritis, "
            "dan tindakan koreksi harus diverifikasi oleh "
            "tim HACCP berdasarkan proses nyata, alat ukur, "
            "pemasok, regulasi dan kondisi operasional SPPG.",
            styles["Normal"]
        )
    )

    doc.build(story)

    output.seek(0)

    return output


# =========================================================
# TAMPILKAN DATA JSON
# =========================================================

def show_section(section_title, section_data):
    """
    Menampilkan satu bagian hasil HACCP.
    """

    st.subheader(
        section_title.replace("_", " ").title()
    )

    if isinstance(section_data, dict):
        for key, value in section_data.items():

            st.markdown(
                f"**{key.replace('_', ' ').title()}**"
            )

            if isinstance(value, list):
                for item in value:
                    st.write(f"- {item}")

            elif isinstance(value, dict):
                st.json(value)

            else:
                st.write(value)

    elif isinstance(section_data, list):

        if section_data and isinstance(
            section_data[0],
            dict
        ):
            st.dataframe(
                pd.DataFrame(section_data),
                use_container_width=True
            )

        else:
            for item in section_data:
                st.write(f"- {item}")

    else:
        st.write(section_data)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Pengaturan")

st.sidebar.markdown(
    """
Masukkan API Key OpenAI agar sistem dapat
menganalisis bahan secara otomatis.
"""
)

api_key_input = st.sidebar.text_input(
    "OPENAI_API_KEY",
    type="password",
    help=(
        "Jangan tampilkan API Key di GitHub. "
        "Gunakan Streamlit Secrets."
    )
)

if api_key_input:
    st.session_state["api_key"] = api_key_input

facility = st.sidebar.text_input(
    "Nama Dapur/SPPG",
    value="SPPG Pangkajene dan Kepulauan Segeri"
)

responsible_person = st.sidebar.text_input(
    "Penanggung Jawab",
    value="Ahli Gizi"
)

intended_use = st.sidebar.text_area(
    "Tujuan Penggunaan Bahan",
    value=(
        "Digunakan sebagai bahan makanan "
        "dalam produksi MBG/SPPG."
    )
)

vulnerable_groups = st.sidebar.text_area(
    "Kelompok Penerima Manfaat",
    value=(
        "Anak sekolah, balita jika relevan, "
        "ibu hamil/menyusui jika relevan, "
        "dan kelompok rentan lainnya."
    )
)

process_description = st.sidebar.text_area(
    "Gambaran Proses",
    value=(
        "Penerimaan bahan → penyimpanan → "
        "sortasi → pencucian/persiapan → "
        "pengolahan → pemorsian → distribusi."
    )
)


# =========================================================
# HALAMAN UTAMA
# =========================================================

st.title("🧪 Generator HACCP Per Bahan")

st.write(
    """
Masukkan **satu nama bahan saja**. Sistem akan mencari
informasi umum melalui Wikipedia Indonesia dan meminta AI
menyusun analisis HACCP yang lebih rinci.
"""
)

ingredient = st.text_input(
    "Nama bahan yang ingin dianalisis",
    placeholder=(
        "Contoh: bayam, kangkung, ayam, udang, telur, "
        "daging sapi, tahu, tempe"
    )
)

generate_button = st.button(
    "🔍 Cari Informasi dan Buat HACCP",
    type="primary"
)


# =========================================================
# PROSES GENERATE
# =========================================================

if generate_button:

    if not ingredient.strip():
        st.warning(
            "Silakan masukkan nama bahan terlebih dahulu."
        )
        st.stop()

    if not get_openai_client():
        st.error(
            "OPENAI_API_KEY belum tersedia. "
            "Masukkan API Key di sidebar atau "
            "gunakan Streamlit Secrets."
        )
        st.stop()

    with st.spinner(
        "Mencari informasi Wikipedia Indonesia..."
    ):
        wiki_data = search_wikipedia_image(
            ingredient.strip()
        )

    if wiki_data.get("image"):
        st.image(
            wiki_data["image"],
            caption=(
                f"Gambar referensi Wikipedia: "
                f"{wiki_data.get('title', ingredient)}"
            ),
            width=280
        )
    else:
        st.info(
            "Gambar Wikipedia tidak ditemukan. "
            "Analisis tetap dapat dilanjutkan."
        )

    with st.spinner(
        "AI sedang menyusun analisis HACCP per bahan..."
    ):
        try:

            haccp_data = generate_haccp_with_ai(
                ingredient=ingredient.strip(),
                facility=facility,
                responsible_person=responsible_person,
                intended_use=intended_use,
                process_description=process_description,
                vulnerable_groups=vulnerable_groups,
                wikipedia_description=wiki_data.get(
                    "description",
                    ""
                )
            )

            st.session_state["haccp_data"] = haccp_data
            st.session_state["wiki_data"] = wiki_data
            st.session_state["ingredient"] = ingredient.strip()

            st.success(
                "Analisis HACCP berhasil dibuat."
            )

        except Exception as error:
            st.error(
                "Gagal membuat analisis HACCP."
            )
            st.exception(error)


# =========================================================
# TAMPILKAN HASIL
# =========================================================

if "haccp_data" in st.session_state:

    haccp_data = st.session_state["haccp_data"]
    wiki_data = st.session_state["wiki_data"]
    saved_ingredient = st.session_state["ingredient"]

    metadata = {
        "Nama bahan": saved_ingredient,
        "Nama dapur/SPPG": facility,
        "Penanggung jawab": responsible_person,
        "Tanggal": datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        ),
        "Tujuan penggunaan": intended_use,
        "Kelompok penerima manfaat": vulnerable_groups,
        "Gambaran proses": process_description
    }

    st.divider()

    st.header(
        f"📋 Hasil HACCP: {saved_ingredient}"
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Ringkasan Bahan",
        "Analisis Bahaya",
        "CCP dan Monitoring",
        "Catatan Validasi",
        "Export"
    ])

    with tab1:

        show_section(
            "identitas_bahan",
            haccp_data.get(
                "identitas_bahan",
                {}
            )
        )

        st.subheader(
            "Informasi Wikipedia Indonesia"
        )

        st.write(
            wiki_data.get(
                "description",
                "Tidak tersedia."
            )
        )

        st.markdown(
            f"[Buka Wikipedia Indonesia]("
            f"{wiki_data.get('wikipedia_url', '')}"
            f")"
        )

        show_section(
            "tugas_pendahuluan",
            haccp_data.get(
                "tugas_pendahuluan",
                {}
            )
        )

    with tab2:

        show_section(
            "analisis_bahaya",
            haccp_data.get(
                "analisis_bahaya",
                []
            )
        )

        show_section(
            "penerimaan_bahan",
            haccp_data.get(
                "penerimaan_bahan",
                {}
            )
        )

        show_section(
            "penyimpanan",
            haccp_data.get(
                "penyimpanan",
                {}
            )
        )

        show_section(
            "persiapan_bahan",
            haccp_data.get(
                "persiapan_bahan",
                {}
            )
        )

        show_section(
            "proses_pengolahan",
            haccp_data.get(
                "proses_pengolahan",
                {}
            )
        )

    with tab3:

        show_section(
            "penentuan_ccp",
            haccp_data.get(
                "penentuan_ccp",
                []
            )
        )

        show_section(
            "rencana_ccp",
            haccp_data.get(
                "rencana_ccp",
                []
            )
        )

        show_section(
            "monitoring_dan_verifikasi",
            haccp_data.get(
                "monitoring_dan_verifikasi",
                []
            )
        )

        show_section(
            "tindakan_koreksi_umum",
            haccp_data.get(
                "tindakan_koreksi_umum",
                []
            )
        )

    with tab4:

        show_section(
            "dokumen_rekaman",
            haccp_data.get(
                "dokumen_rekaman",
                []
            )
        )

        show_section(
            "catatan_validasi",
            haccp_data.get(
                "catatan_validasi",
                []
            )
        )

        st.subheader("Kesimpulan")

        st.write(
            haccp_data.get(
                "kesimpulan",
                ""
            )
        )

        st.warning(
            """
            Periksa kembali seluruh suhu, waktu, batas kritis,
            metode sanitasi, alur produksi, dan status CCP.
            Jangan langsung menjadikan hasil AI sebagai SOP final
            sebelum divalidasi oleh tim HACCP.
            """
        )

    with tab5:

        st.subheader(
            "📊 Export Dokumen"
        )

        st.write(
            """
            Pilih format dokumen yang ingin disimpan.
            """
        )

        excel_file = create_excel_file(
            haccp_data=haccp_data,
            wiki_data=wiki_data,
            metadata=metadata
        )

        pdf_file = create_pdf_file(
            haccp_data=haccp_data,
            wiki_data=wiki_data,
            metadata=metadata
        )

        json_file = json.dumps(
            {
                "metadata": metadata,
                "wikipedia": wiki_data,
                "haccp": haccp_data
            },
            ensure_ascii=False,
            indent=2
        ).encode("utf-8")

        file_base = clean_filename(
            saved_ingredient
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.download_button(
                label="⬇️ Download Excel",
                data=excel_file,
                file_name=(
                    f"HACCP_{file_base}.xlsx"
                ),
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.spreadsheetml.sheet"
                )
            )

        with col2:

            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_file,
                file_name=(
                    f"HACCP_{file_base}.pdf"
                ),
                mime="application/pdf"
            )

        with col3:

            st.download_button(
                label="⬇️ Download JSON",
                data=json_file,
                file_name=(
                    f"HACCP_{file_base}.json"
                ),
                mime="application/json"
            )

        st.info(
            """
            File Excel berisi beberapa sheet seperti:
            identitas, Wikipedia, analisis bahaya,
            penerimaan, penyimpanan, persiapan,
            proses pengolahan, CCP, monitoring,
            tindakan koreksi, dan validasi.
            """
        )
