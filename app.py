
import streamlit as st
import pandas as pd
import io
import requests
import re
from urllib.parse import quote

# =========================================================
# GENERATOR HACCP V2
# Codex HACCP / ISO 22000 - Rancangan untuk Validasi Tim
# =========================================================

st.set_page_config(
    page_title="Generator HACCP Otomatis",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Generator Dokumen HACCP Otomatis")
st.caption(
    "Codex HACCP / SNI ISO 22000 | "
    "Rancangan keamanan pangan untuk validasi Tim HACCP"
)

# =========================================================
# DATABASE BAHAN
# =========================================================

BAHAN_DB = {

    "bayam": {
        "nama": "Bayam",
        "nama_produk": "Sayur Bayam Matang",
        "nama_inggris": "Spinach",
        "kategori": "Sayuran Daun",
        "alergen": "Tidak termasuk alergen utama yang umum diakui Codex",
        "penyimpanan": "Bahan segar sesuai spesifikasi dan pengendalian suhu",
        "karakteristik": "Sayuran daun segar, mudah rusak, siap dimasak",
        "bahaya": [
            {
                "kategori": "Biologi",
                "bahaya": "Mikroorganisme patogen dari tanah dan air",
                "sumber": "Tanah, air, pekerja, peralatan",
                "keparahan": 3,
                "kemungkinan": 3,
                "pengendalian": "Pemasok disetujui, air layak, sortasi, pencucian, pemasakan"
            },
            {
                "kategori": "Kimia",
                "bahaya": "Residu pestisida",
                "sumber": "Budidaya dan bahan baku",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Pemasok disetujui dan pemeriksaan bahan"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Tanah, pasir, ulat, dan benda asing",
                "sumber": "Bahan baku",
                "keparahan": 2,
                "kemungkinan": 3,
                "pengendalian": "Sortasi dan pencucian"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan bahan segar",
            "Sortasi",
            "Pencucian",
            "Pemotongan",
            "Pemasakan",
            "Holding",
            "Pemorsian",
            "Distribusi"
        ]
    },

    "kangkung": {
        "nama": "Kangkung",
        "nama_produk": "Olahan Kangkung Matang",
        "nama_inggris": "Water spinach",
        "kategori": "Sayuran Daun",
        "alergen": "Tidak termasuk alergen utama yang umum diakui Codex",
        "penyimpanan": "Bahan segar sesuai spesifikasi",
        "karakteristik": "Sayuran daun segar, mudah rusak",
        "bahaya": [
            {
                "kategori": "Biologi",
                "bahaya": "Mikroorganisme patogen dari tanah dan air",
                "sumber": "Tanah, air, pekerja, peralatan",
                "keparahan": 3,
                "kemungkinan": 3,
                "pengendalian": "Pemasok disetujui, air layak, pencucian, pemasakan"
            },
            {
                "kategori": "Kimia",
                "bahaya": "Residu pestisida",
                "sumber": "Budidaya",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Pemasok disetujui dan pemeriksaan bahan"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Tanah, pasir, ulat, dan benda asing",
                "sumber": "Bahan baku",
                "keparahan": 2,
                "kemungkinan": 3,
                "pengendalian": "Sortasi dan pencucian"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan bahan segar",
            "Sortasi",
            "Pencucian",
            "Pemotongan",
            "Pemasakan",
            "Holding",
            "Pemorsian",
            "Distribusi"
        ]
    },

    "wortel": {
        "nama": "Wortel",
        "nama_produk": "Olahan Wortel Matang",
        "nama_inggris": "Carrot",
        "kategori": "Sayuran Umbi",
        "alergen": "Tidak termasuk alergen utama yang umum diakui Codex",
        "penyimpanan": "Bahan segar sesuai spesifikasi",
        "karakteristik": "Sayuran umbi segar",
        "bahaya": [
            {
                "kategori": "Biologi",
                "bahaya": "Mikroorganisme patogen dari tanah dan air",
                "sumber": "Tanah, air, bahan baku",
                "keparahan": 3,
                "kemungkinan": 3,
                "pengendalian": "Pemasok disetujui, sortasi, pencucian, pemasakan"
            },
            {
                "kategori": "Kimia",
                "bahaya": "Residu pestisida",
                "sumber": "Budidaya",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Pemasok disetujui dan pemeriksaan bahan"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Tanah, pasir, dan benda asing",
                "sumber": "Bahan baku",
                "keparahan": 2,
                "kemungkinan": 3,
                "pengendalian": "Sortasi dan pencucian"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan bahan segar",
            "Sortasi",
            "Pencucian",
            "Pengupasan",
            "Pemotongan",
            "Pemasakan",
            "Holding",
            "Pemorsian",
            "Distribusi"
        ]
    },

    "ayam": {
        "nama": "Ayam",
        "nama_produk": "Olahan Ayam Matang",
        "nama_inggris": "Chicken",
        "kategori": "Daging Unggas",
        "alergen": "Tidak termasuk alergen utama apabila tidak ada bahan tambahan alergen",
        "penyimpanan": "Chiller/freezer sesuai spesifikasi dan SOP",
        "karakteristik": "Daging unggas mentah, mudah rusak",
        "bahaya": [
            {
                "kategori": "Biologi",
                "bahaya": "Salmonella spp. dan Campylobacter spp.",
                "sumber": "Daging ayam mentah",
                "keparahan": 3,
                "kemungkinan": 3,
                "pengendalian": "Rantai dingin, pencegahan kontaminasi silang, pemasakan tervalidasi"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Tulang atau serpihan tulang",
                "sumber": "Daging ayam",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Pemeriksaan bahan dan proses"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan chiller/freezer",
            "Persiapan",
            "Pemotongan",
            "Pencucian sesuai SOP",
            "Pemasakan",
            "Holding",
            "Pemorsian",
            "Distribusi"
        ]
    },

    "telur": {
        "nama": "Telur",
        "nama_produk": "Olahan Telur Matang",
        "nama_inggris": "Egg",
        "kategori": "Telur",
        "alergen": "MENGANDUNG ALERGEN TELUR",
        "penyimpanan": "Sesuai spesifikasi penerimaan dan SOP penyimpanan",
        "karakteristik": "Telur mentah, mudah rusak",
        "bahaya": [
            {
                "kategori": "Biologi",
                "bahaya": "Salmonella spp.",
                "sumber": "Telur mentah dan cangkang",
                "keparahan": 3,
                "kemungkinan": 3,
                "pengendalian": "Penerimaan baik, pencegahan kontaminasi silang, pemasakan tervalidasi"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Serpihan cangkang",
                "sumber": "Pemecahan telur",
                "keparahan": 2,
                "kemungkinan": 2,
                "pengendalian": "Pemeriksaan telur dan pemecahan higienis"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan",
            "Persiapan",
            "Pemecahan",
            "Pengolahan",
            "Pemasakan",
            "Holding",
            "Pemorsian",
            "Distribusi"
        ]
    },

    "udang": {
        "nama": "Udang",
        "nama_produk": "Olahan Udang Matang",
        "nama_inggris": "Shrimp",
        "kategori": "Seafood",
        "alergen": "MENGANDUNG ALERGEN KRUSTASEA",
        "penyimpanan": "Chiller/freezer sesuai spesifikasi",
        "karakteristik": "Seafood mentah, mudah rusak",
        "bahaya": [
            {
                "kategori": "Biologi",
                "bahaya": "Mikroorganisme patogen dari seafood",
                "sumber": "Udang mentah",
                "keparahan": 3,
                "kemungkinan": 3,
                "pengendalian": "Rantai dingin, pemasok disetujui, pemasakan tervalidasi"
            },
            {
                "kategori": "Kimia",
                "bahaya": "Residu bahan kimia yang tidak sesuai",
                "sumber": "Bahan baku dan proses",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Spesifikasi pemasok dan pemeriksaan"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Sisa cangkang atau benda asing",
                "sumber": "Pengupasan dan bahan baku",
                "keparahan": 2,
                "kemungkinan": 3,
                "pengendalian": "Pemeriksaan dan pengupasan sesuai SOP"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan dingin",
            "Pengupasan",
            "Pencucian",
            "Penimbangan",
            "Pemasakan",
            "Holding",
            "Pemorsian",
            "Distribusi"
        ]
    },

    "sapi": {
        "nama": "Daging Sapi",
        "nama_produk": "Olahan Daging Sapi Matang",
        "nama_inggris": "Beef",
        "kategori": "Daging",
        "alergen": "Tidak termasuk alergen utama apabila tidak ada bahan tambahan alergen",
        "penyimpanan": "Chiller/freezer sesuai spesifikasi",
        "karakteristik": "Daging mentah, mudah rusak",
        "bahaya": [
            {
                "kategori": "Biologi",
                "bahaya": "E. coli patogen dan Salmonella spp.",
                "sumber": "Daging sapi mentah",
                "keparahan": 3,
                "kemungkinan": 3,
                "pengendalian": "Rantai dingin, pencegahan kontaminasi silang, pemasakan tervalidasi"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Tulang atau benda asing",
                "sumber": "Bahan baku",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Pemeriksaan bahan dan proses"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan dingin",
            "Persiapan",
            "Pemotongan",
            "Pemasakan",
            "Holding",
            "Pemorsian",
            "Distribusi"
        ]
    },

    "beras": {
        "nama": "Beras",
        "nama_produk": "Nasi Putih Matang",
        "nama_inggris": "Rice",
        "kategori": "Serealia",
        "alergen": "Tidak termasuk alergen utama yang umum diakui Codex",
        "penyimpanan": "Gudang kering bersih dan sesuai SOP",
        "karakteristik": "Bahan kering yang diolah dengan air dan panas",
        "bahaya": [
            {
                "kategori": "Biologi",
                "bahaya": "Bacillus cereus dan spora",
                "sumber": "Bahan baku dan penyimpanan nasi matang",
                "keparahan": 3,
                "kemungkinan": 3,
                "pengendalian": "Pemasok baik, penyimpanan kering, pemasakan, kontrol waktu-suhu"
            },
            {
                "kategori": "Kimia",
                "bahaya": "Kontaminan kimia sesuai risiko bahan",
                "sumber": "Bahan baku",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Pemasok disetujui dan spesifikasi bahan"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Batu, sekam, benda asing",
                "sumber": "Bahan baku",
                "keparahan": 2,
                "kemungkinan": 3,
                "pengendalian": "Sortasi dan pemeriksaan bahan"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan gudang kering",
            "Sortasi",
            "Pencucian",
            "Penimbangan",
            "Pemasakan",
            "Holding",
            "Pemorsian",
            "Distribusi"
        ]
    },

    "kentang": {
        "nama": "Kentang",
        "nama_produk": "Olahan Kentang Matang",
        "nama_inggris": "Potato",
        "kategori": "Umbi",
        "alergen": "Tidak termasuk alergen utama yang umum diakui Codex",
        "penyimpanan": "Sesuai spesifikasi bahan",
        "karakteristik": "Umbi segar",
        "bahaya": [
            {
                "kategori": "Biologi",
                "bahaya": "Mikroorganisme dari tanah dan air",
                "sumber": "Bahan baku",
                "keparahan": 3,
                "kemungkinan": 3,
                "pengendalian": "Sortasi, pencucian, pemasakan"
            },
            {
                "kategori": "Kimia",
                "bahaya": "Glikoalkaloid pada kentang yang rusak atau menghijau",
                "sumber": "Bahan baku",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Tolak kentang hijau, busuk, atau tidak sesuai"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Tanah dan benda asing",
                "sumber": "Bahan baku",
                "keparahan": 2,
                "kemungkinan": 3,
                "pengendalian": "Sortasi dan pencucian"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan",
            "Sortasi",
            "Pencucian",
            "Pengupasan",
            "Pemotongan",
            "Pemasakan",
            "Holding",
            "Pemorsian",
            "Distribusi"
        ]
    },

    "tempe": {
        "nama": "Tempe",
        "nama_produk": "Olahan Tempe Matang",
        "nama_inggris": "Tempeh",
        "kategori": "Nabati",
        "alergen": "MENGANDUNG KEDELAI",
        "penyimpanan": "Sesuai spesifikasi bahan dan SOP",
        "karakteristik": "Produk kedelai fermentasi",
        "bahaya": [
            {
                "kategori": "Biologi",
                "bahaya": "Mikroorganisme patogen akibat kontaminasi bahan atau proses",
                "sumber": "Bahan baku, air, pekerja, alat",
                "keparahan": 3,
                "kemungkinan": 3,
                "pengendalian": "Pemasok disetujui, higiene, pemasakan"
            },
            {
                "kategori": "Kimia",
                "bahaya": "Kontaminan kimia sesuai risiko bahan",
                "sumber": "Bahan baku",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Spesifikasi pemasok"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Benda asing",
                "sumber": "Bahan baku dan proses",
                "keparahan": 2,
                "kemungkinan": 2,
                "pengendalian": "Pemeriksaan bahan dan alat"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan",
            "Persiapan",
            "Pemotongan",
            "Pemasakan",
            "Holding",
            "Pemorsian",
            "Distribusi"
        ]
    },

    "tahu": {
        "nama": "Tahu",
        "nama_produk": "Olahan Tahu Matang",
        "nama_inggris": "Tofu",
        "kategori": "Nabati",
        "alergen": "MENGANDUNG KEDELAI",
        "penyimpanan": "Sesuai spesifikasi bahan dan SOP",
        "karakteristik": "Produk kedelai dengan kadar air tinggi",
        "bahaya": [
            {
                "kategori": "Biologi",
                "bahaya": "Mikroorganisme patogen akibat kontaminasi bahan atau proses",
                "sumber": "Bahan baku, air, pekerja, alat",
                "keparahan": 3,
                "kemungkinan": 3,
                "pengendalian": "Pemasok disetujui, higiene, pemasakan"
            },
            {
                "kategori": "Kimia",
                "bahaya": "Kontaminan kimia dari bahan atau proses",
                "sumber": "Bahan baku",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Spesifikasi pemasok dan pemeriksaan"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Benda asing",
                "sumber": "Bahan baku dan proses",
                "keparahan": 2,
                "kemungkinan": 2,
                "pengendalian": "Pemeriksaan bahan dan alat"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan",
            "Persiapan",
            "Pemotongan",
            "Pemasakan",
            "Holding",
            "Pemorsian",
            "Distribusi"
        ]
    },

    "apel": {
        "nama": "Apel",
        "nama_produk": "Apel Potong / Buah Segar",
        "nama_inggris": "Apple",
        "kategori": "Buah",
        "alergen": "Tidak termasuk alergen utama yang umum diakui Codex",
        "penyimpanan": "Sesuai spesifikasi dan pengendalian suhu",
        "karakteristik": "Buah segar siap santap",
        "bahaya": [
            {
                "kategori": "Biologi",
                "bahaya": "Mikroorganisme patogen pada permukaan buah",
                "sumber": "Tanah, air, pekerja, alat",
                "keparahan": 3,
                "kemungkinan": 3,
                "pengendalian": "Pemasok disetujui, pencucian, higiene, kontrol suhu/waktu"
            },
            {
                "kategori": "Kimia",
                "bahaya": "Residu pestisida",
                "sumber": "Budidaya",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Pemasok disetujui dan pemeriksaan"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Biji, tangkai, benda asing",
                "sumber": "Bahan baku",
                "keparahan": 2,
                "kemungkinan": 2,
                "pengendalian": "Sortasi dan pemeriksaan"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan",
            "Sortasi",
            "Pencucian",
            "Pemotongan bila diperlukan",
            "Pemorsian",
            "Distribusi"
        ]
    },

    "semangka": {
        "nama": "Semangka",
        "nama_produk": "Semangka Potong / Buah Segar",
        "nama_inggris": "Watermelon",
        "kategori": "Buah",
        "alergen": "Tidak termasuk alergen utama yang umum diakui Codex",
        "penyimpanan": "Sesuai spesifikasi dan pengendalian suhu",
        "karakteristik": "Buah segar siap santap",
        "bahaya": [
            {
                "kategori": "Biologi",
                "bahaya": "Mikroorganisme patogen pada permukaan dan daging buah",
                "sumber": "Tanah, air, pekerja, alat",
                "keparahan": 3,
                "kemungkinan": 3,
                "pengendalian": "Pemasok disetujui, pencucian, higiene, kontrol suhu/waktu"
            },
            {
                "kategori": "Kimia",
                "bahaya": "Residu pestisida",
                "sumber": "Budidaya",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Pemasok disetujui dan pemeriksaan"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Biji, kulit, dan benda asing",
                "sumber": "Bahan baku",
                "keparahan": 2,
                "kemungkinan": 2,
                "pengendalian": "Sortasi dan pemeriksaan"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan",
            "Sortasi",
            "Pencucian",
            "Pemotongan",
            "Pemorsian",
            "Distribusi"
        ]
    },

    "minyak": {
        "nama": "Minyak Goreng",
        "nama_produk": "Minyak Goreng",
        "nama_inggris": "Cooking oil",
        "kategori": "Bahan Tambahan",
        "alergen": "Periksa jenis minyak dan spesifikasi pemasok",
        "penyimpanan": "Gudang kering, tertutup, sesuai spesifikasi",
        "karakteristik": "Bahan cair untuk pengolahan makanan",
        "bahaya": [
            {
                "kategori": "Kimia",
                "bahaya": "Kontaminan kimia atau minyak rusak",
                "sumber": "Bahan baku dan penggunaan",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Pemasok disetujui, spesifikasi, kontrol penggunaan minyak"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Benda asing",
                "sumber": "Kemasan dan proses",
                "keparahan": 2,
                "kemungkinan": 2,
                "pengendalian": "Pemeriksaan kemasan dan penyaringan sesuai SOP"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan",
            "Penimbangan",
            "Pengolahan",
            "Pemorsian"
        ]
    },

    "bumbu": {
        "nama": "Bumbu Dapur",
        "nama_produk": "Bumbu Masakan",
        "nama_inggris": "Cooking spices",
        "kategori": "Bumbu",
        "alergen": "Periksa komposisi dan label pemasok",
        "penyimpanan": "Gudang kering sesuai spesifikasi",
        "karakteristik": "Bahan tambahan untuk pengolahan makanan",
        "bahaya": [
            {
                "kategori": "Biologi",
                "bahaya": "Kontaminasi mikroba pada bahan bumbu",
                "sumber": "Bahan baku dan penyimpanan",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Pemasok disetujui, penyimpanan baik, pengolahan higienis"
            },
            {
                "kategori": "Kimia",
                "bahaya": "Kontaminan kimia atau bahan tambahan tidak sesuai",
                "sumber": "Bahan baku",
                "keparahan": 3,
                "kemungkinan": 2,
                "pengendalian": "Spesifikasi pemasok dan pemeriksaan label"
            },
            {
                "kategori": "Fisik",
                "bahaya": "Benda asing",
                "sumber": "Bahan baku dan kemasan",
                "keparahan": 2,
                "kemungkinan": 2,
                "pengendalian": "Pemeriksaan bahan dan kemasan"
            }
        ],
        "proses": [
            "Penerimaan",
            "Penyimpanan",
            "Penimbangan",
            "Pengolahan",
            "Pemasakan"
        ]
    }
}

# =========================================================
# FUNGSI DETEKSI BAHAN
# =========================================================

def deteksi_bahan(nama_menu):

    m = nama_menu.lower().strip()

    prioritas = [
        ("udang", ["udang", "shrimp"]),
        ("telur", ["telur", "egg"]),
        ("ayam", ["ayam", "chicken"]),
        ("sapi", ["sapi", "daging sapi", "beef"]),
        ("kangkung", ["kangkung"]),
        ("bayam", ["bayam", "spinach"]),
        ("wortel", ["wortel", "carrot"]),
        ("kentang", ["kentang", "potato"]),
        ("semangka", ["semangka", "watermelon"]),
        ("apel", ["apel", "apple"]),
        ("beras", ["beras", "nasi", "rice"]),
        ("tempe", ["tempe", "tempeh"]),
        ("tahu", ["tahu", "tofu"]),
        ("minyak", ["minyak goreng", "cooking oil"]),
        ("bumbu", ["bumbu", "spices"])
    ]

    for bahan, kata_kunci in prioritas:
        if any(k in m for k in kata_kunci):
            return bahan

    return "bayam"


def cari_semua_bahan(teks):

    m = teks.lower()

    hasil = []

    for bahan, info in BAHAN_DB.items():

        kata = [
            bahan,
            info["nama"].lower(),
            info["nama_inggris"].lower()
        ]

        if any(k in m for k in kata):
            hasil.append(bahan)

    return list(dict.fromkeys(hasil))


# =========================================================
# GAMBAR OTOMATIS WIKIMEDIA
# =========================================================

@st.cache_data(ttl=86400)
def get_wikimedia_image(query):

    url = (
        "https://en.wikipedia.org/api/rest_v1/page/summary/"
        + quote(query.replace(" ", "_"))
    )

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "HACCP-Generator/2.0"
            }
        )

        if response.status_code == 200:

            data = response.json()

            if "thumbnail" in data:
                return data["thumbnail"]["source"]

    except Exception:
        return None

    return None


# =========================================================
# DATA UMUM HACCP
# =========================================================

def generate_tim_haccp(penanggung_jawab):

    return pd.DataFrame([
        {
            "Peran": "Ketua Tim HACCP",
            "Nama / Jabatan": penanggung_jawab,
            "Tanggung Jawab": "Koordinasi, validasi, verifikasi, persetujuan dokumen"
        },
        {
            "Peran": "Ahli Gizi",
            "Nama / Jabatan": "Tim HACCP",
            "Tanggung Jawab": "Spesifikasi bahan, menu, analisis bahaya, validasi gizi"
        },
        {
            "Peran": "Kepala Produksi",
            "Nama / Jabatan": "Tim Produksi",
            "Tanggung Jawab": "Pengawasan proses, suhu, waktu, higiene"
        },
        {
            "Peran": "Petugas Penerimaan",
            "Nama / Jabatan": "Tim Logistik",
            "Tanggung Jawab": "Pemeriksaan bahan, kondisi fisik, suhu, pemasok"
        },
        {
            "Peran": "Petugas Sanitasi",
            "Nama / Jabatan": "Tim Sanitasi",
            "Tanggung Jawab": "Sanitasi ruangan, alat, higiene personal"
        },
        {
            "Peran": "Petugas Pemorsian",
            "Nama / Jabatan": "Tim Pemorsian",
            "Tanggung Jawab": "Kontrol higiene, pemorsian, waktu, suhu"
        },
        {
            "Peran": "Petugas Distribusi",
            "Nama / Jabatan": "Tim Distribusi",
            "Tanggung Jawab": "Kontrol waktu, suhu, dan penyerahan makanan"
        }
    ])


def generate_deskripsi_produk(nama_menu, info, jumlah_porsi):

    return pd.DataFrame([
        ["Nama Produk", info["nama_produk"]],
        ["Bahan / Menu", nama_menu],
        ["Kategori", info["kategori"]],
        ["Bahan Utama", info["nama"]],
        ["Jumlah Produksi", jumlah_porsi],
        ["Tujuan Penggunaan", "Siap santap setelah pengolahan"],
        ["Konsumen Sasaran", "Penerima manfaat MBG sesuai kelompok usia"],
        ["Kelompok Rentan", "Balita, anak-anak, lansia, ibu hamil, dan individu rentan sesuai konteks"],
        ["Alergen", info["alergen"]],
        ["Karakteristik", info["karakteristik"]],
        ["Penyimpanan", info["penyimpanan"]],
        ["Kemasan", "Ompreng food grade / sesuai SOP distribusi"],
        ["Masa Simpan", "Mengikuti validasi waktu-suhu dan persyaratan distribusi"],
        ["Metode Pengolahan", "Sesuai diagram alir proses"],
        ["Status Dokumen", "Rancangan — wajib divalidasi Tim HACCP"]
    ], columns=["Parameter", "Keterangan"])


# =========================================================
# DIAGRAM ALIR
# =========================================================

def generate_diagram_alir(info, nama_menu):

    proses = info["proses"]

    return " → ".join(proses)


def generate_tahap_proses(info):

    return pd.DataFrame([
        {
            "No": i + 1,
            "Tahap Proses": tahap,
            "Keterangan": "Sesuai SOP dan observasi proses aktual"
        }
        for i, tahap in enumerate(info["proses"])
    ])


# =========================================================
# ANALISIS BAHAYA
# =========================================================

def generate_analisis_bahaya(info, nama_menu):

    rows = []

    for tahap in info["proses"]:

        for h in info["bahaya"]:

            rows.append({
                "Nama Menu": nama_menu,
                "Tahap Proses": tahap,
                "Kategori Bahaya": h["kategori"],
                "Bahaya Potensial": h["bahaya"],
                "Sumber Bahaya": h["sumber"],
                "Keparahan": h["keparahan"],
                "Kemungkinan": h["kemungkinan"],
                "Skor Risiko": h["keparahan"] * h["kemungkinan"],
                "Tindakan Pengendalian": h["pengendalian"],
                "Bahaya Signifikan": "Evaluasi Tim HACCP",
                "CCP": "Evaluasi Pohon Keputusan"
            })

    return pd.DataFrame(rows)


# =========================================================
# DATA CCP
# =========================================================

def generate_ccp(info, nama_menu):

    rows = []

    for tahap in info["proses"]:

        if "Pemasakan" in tahap or "Pengolahan" in tahap:

            rows.append({
                "Tahap Proses": tahap,
                "Bahaya Signifikan": "Bahaya biologis — evaluasi spesifik produk",
                "CCP": "Evaluasi pohon keputusan",
                "Batas Kritis": "Tetapkan berdasarkan validasi proses",
                "Monitoring": "Suhu inti / waktu sesuai SOP tervalidasi",
                "Frekuensi": "Setiap batch / sesuai SOP",
                "PIC": "Kepala Produksi",
                "Tindakan Koreksi": "Tahan produk dan lanjutkan tindakan sesuai SOP",
                "Verifikasi": "Review catatan dan validasi proses"
            })

        elif "Holding" in tahap:

            rows.append({
                "Tahap Proses": tahap,
                "Bahaya Signifikan": "Pertumbuhan mikroba dan rekontaminasi",
                "CCP": "Evaluasi pohon keputusan",
                "Batas Kritis": "Tetapkan batas waktu-suhu tervalidasi",
                "Monitoring": "Suhu dan waktu holding",
                "Frekuensi": "Berkala sesuai SOP",
                "PIC": "Kepala Produksi / Pemorsian",
                "Tindakan Koreksi": "Tahan produk, evaluasi waktu-suhu, tindak lanjuti SOP",
                "Verifikasi": "Review log suhu dan waktu"
            })

    return pd.DataFrame(rows)


# =========================================================
# POHON KEPUTUSAN CCP
# =========================================================

def pohon_keputusan_ccp():

    st.subheader("🌳 Pohon Keputusan CCP")

    st.warning(
        "Hasil ini adalah alat bantu evaluasi. "
        "Penetapan CCP harus disetujui Tim HACCP."
    )

    q1 = st.radio(
        "1. Apakah terdapat bahaya signifikan?",
        ["Ya", "Tidak"],
        key="ccp_q1"
    )

    if q1 == "Tidak":
        return "Bukan CCP — bahaya tidak signifikan"

    q2 = st.radio(
        "2. Apakah tersedia tindakan pengendalian?",
        ["Ya", "Tidak"],
        key="ccp_q2"
    )

    if q2 == "Tidak":
        return "Evaluasi perubahan proses atau tindakan pengendalian"

    q3 = st.radio(
        "3. Apakah tahap ini dirancang untuk menghilangkan "
        "atau mengurangi bahaya ke tingkat dapat diterima?",
        ["Ya", "Tidak"],
        key="ccp_q3"
    )

    if q3 == "Ya":
        return "Berpotensi CCP — validasi batas kritis diperlukan"

    q4 = st.radio(
        "4. Apakah bahaya dapat meningkat ke tingkat tidak dapat diterima?",
        ["Ya", "Tidak"],
        key="ccp_q4"
    )

    if q4 == "Tidak":
        return "Bukan CCP — evaluasi pengendalian lain"

    q5 = st.radio(
        "5. Apakah tahap berikutnya dapat menghilangkan "
        "atau mengurangi bahaya ke tingkat dapat diterima?",
        ["Ya", "Tidak"],
        key="ccp_q5"
    )

    if q5 == "Ya":
        return "Bukan CCP pada tahap ini — dikendalikan tahap berikutnya"

    return "CCP — tetapkan batas kritis, monitoring, koreksi, dan verifikasi"


# =========================================================
# FORM MONITORING
# =========================================================

def generate_form_monitoring():

    return pd.DataFrame([
        {
            "Tanggal": "",
            "Nama Menu": "",
            "Tahap Proses": "",
            "Jam": "",
            "Suhu (°C)": "",
            "Batas Kritis": "",
            "Hasil": "Sesuai / Tidak Sesuai",
            "PIC": "",
            "Paraf": ""
        }
        for _ in range(10)
    ])


def generate_form_koreksi():

    return pd.DataFrame([
        {
            "Tanggal": "",
            "Nama Menu": "",
            "Tahap Proses": "",
            "Penyimpangan": "",
            "Tindakan Koreksi": "",
            "Produk Ditahan / Dilepas": "",
            "PIC": "",
            "Verifikasi": "",
            "Paraf": ""
        }
        for _ in range(10)
    ])


# =========================================================
# INPUT SIDEBAR
# =========================================================

st.sidebar.header("⚙️ Pengaturan Operasional")

nama_menu = st.sidebar.text_input(
    "Nama Bahan / Menu",
    value="Bayam"
)

nama_dapur = st.sidebar.text_input(
    "Nama Fasilitas / Dapur",
    value="Dapur Satuan Pelayanan MBG"
)

penanggung_jawab = st.sidebar.text_input(
    "Penanggung Jawab / Ketua Tim",
    value="Ishak Yunus"
)

jumlah_porsi = st.sidebar.number_input(
    "Jumlah Porsi",
    min_value=1,
    value=1000,
    step=100
)

# Input bahan tambahan
bahan_tambahan = st.sidebar.text_input(
    "Bahan Tambahan / Bumbu",
    value=""
)

# Pilih bahan dari database
bahan = deteksi_bahan(nama_menu)

info_bahan = BAHAN_DB[bahan]

# Semua bahan yang terdeteksi
semua_bahan = cari_semua_bahan(
    nama_menu + " " + bahan_tambahan
)

if bahan not in semua_bahan:
    semua_bahan.insert(0, bahan)

semua_bahan = list(dict.fromkeys(semua_bahan))

# =========================================================
# GENERATE DATA
# =========================================================

df_tim = generate_tim_haccp(penanggung_jawab)

df_deskripsi = generate_deskripsi_produk(
    nama_menu,
    info_bahan,
    jumlah_porsi
)

diagram_alir = generate_diagram_alir(
    info_bahan,
    nama_menu
)

df_tahap = generate_tahap_proses(info_bahan)

df_bahaya = generate_analisis_bahaya(
    info_bahan,
    nama_menu
)

df_ccp = generate_ccp(
    info_bahan,
    nama_menu
)

df_monitoring = generate_form_monitoring()

df_koreksi = generate_form_koreksi()

# =========================================================
# HEADER
# =========================================================

st.header(f"📋 Rencana HACCP: {nama_menu}")

st.subheader(
    f"Fasilitas: {nama_dapur} | PJ: {penanggung_jawab}"
)

col1, col2 = st.columns([1, 2])

with col1:

    gambar = get_wikimedia_image(
        info_bahan["nama_inggris"]
    )

    if gambar:
        st.image(
            gambar,
            caption=info_bahan["nama_produk"],
            use_container_width=True
        )
    else:
        st.info("Gambar otomatis belum tersedia.")

with col2:

    st.markdown(f"### {info_bahan['nama_produk']}")

    st.write(
        f"**Kategori:** {info_bahan['kategori']}"
    )

    st.write(
        f"**Alergen:** {info_bahan['alergen']}"
    )

    st.write(
        f"**Jumlah Produksi:** {jumlah_porsi:,} porsi"
    )

    st.write(
        f"**Bahan Tambahan:** {bahan_tambahan or 'Tidak diisi'}"
    )

    st.info(
        "Dokumen ini merupakan rancangan HACCP "
        "yang wajib divalidasi oleh Tim HACCP."
    )

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "5 Langkah Persiapan",
    "7 Prinsip HACCP",
    "Pohon CCP",
    "Monitoring",
    "Dokumentasi",
    "Ekspor Excel"
])

# =========================================================
# TAB 1 — 5 LANGKAH PERSIAPAN
# =========================================================

with tab1:

    st.subheader("I. 5 Langkah Persiapan")

    st.markdown("### 1. Tim HACCP & Tanggung Jawab")

    st.dataframe(
        df_tim,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 2. Deskripsi Produk Lengkap")

    st.dataframe(
        df_deskripsi,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 3. Intended Use & Konsumen Sasaran")

    st.info(
        "Produk ditujukan untuk siap santap oleh penerima manfaat MBG "
        "sesuai kelompok usia. Kelompok rentan perlu diperhatikan "
        "dalam analisis bahaya dan pengendalian."
    )

    st.markdown("### 4. Diagram Alir Proses")

    st.code(
        diagram_alir,
        language="text"
    )

    st.markdown("### 5. Verifikasi Diagram Alir")

    st.write(
        "Tim HACCP wajib mengamati alur proses secara langsung "
        "di lapangan dan mencatat kesesuaian dengan operasional aktual."
    )

    st.checkbox(
        "Diagram alir sudah diverifikasi di lapangan",
        key="verifikasi_alir"
    )

    st.text_area(
        "Catatan Verifikasi",
        key="catatan_verifikasi"
    )

# =========================================================
# TAB 2 — 7 PRINSIP HACCP
# =========================================================

with tab2:

    st.subheader("II. 7 Prinsip HACCP")

    st.markdown("### Prinsip 1 — Analisis Bahaya")

    st.dataframe(
        df_bahaya,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Prinsip 2 — Penentuan CCP")

    st.dataframe(
        df_ccp,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Prinsip 3 — Batas Kritis")

    st.write(
        "Batas kritis harus ditetapkan dan divalidasi "
        "berdasarkan bahaya, proses, alat, waktu, suhu, "
        "dan persyaratan yang berlaku."
    )

    st.markdown("### Prinsip 4 — Monitoring")

    st.write(
        "Monitoring dilakukan sesuai SOP pada setiap tahap "
        "yang ditetapkan Tim HACCP."
    )

    st.markdown("### Prinsip 5 — Tindakan Koreksi")

    st.write(
        "Produk yang menyimpang harus ditahan dan dievaluasi. "
        "Tindakan koreksi mengikuti SOP yang disetujui."
    )

    st.markdown("### Prinsip 6 — Verifikasi")

    st.write(
        "Review catatan, pemeriksaan lapangan, evaluasi alat ukur, "
        "dan kegiatan verifikasi lain sesuai program HACCP."
    )

    st.markdown("### Prinsip 7 — Dokumentasi")

    st.write(
        "Semua monitoring, penyimpangan, koreksi, verifikasi, "
        "dan persetujuan harus didokumentasikan."
    )

# =========================================================
# TAB 3 — POHON KEPUTUSAN
# =========================================================

with tab3:

    hasil_ccp = pohon_keputusan_ccp()

    st.success(hasil_ccp)

# =========================================================
# TAB 4 — MONITORING
# =========================================================

with tab4:

    st.subheader("📝 Form Monitoring")

    st.dataframe(
        df_monitoring,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🛠️ Form Tindakan Koreksi")

    st.dataframe(
        df_koreksi,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# TAB 5 — DOKUMENTASI
# =========================================================

with tab5:

    st.subheader("📁 Dokumen Pendukung HACCP")

    st.markdown("""
    - Form Penerimaan Bahan
    - Log Suhu Pemasakan
    - Log Suhu Holding
    - Form Monitoring Pemorsian
    - Form Tindakan Koreksi
    - Form Verifikasi
    - Form Kalibrasi Termometer
    - Form Sanitasi Alat dan Ruangan
    - Form Higiene Personal
    - Form Evaluasi Pemasok
    """)

    st.warning(
        "Pastikan dokumen yang digunakan sudah disesuaikan "
        "dengan SOP dan persyaratan SPPG."
    )

# =========================================================
# TAB 6 — EKSPOR EXCEL
# =========================================================

with tab6:

    st.subheader("📤 Ekspor Dokumen HACCP")

    st.write(
        "Excel berisi data tim, deskripsi produk, "
        "diagram alir, analisis bahaya, CCP, monitoring, "
        "dan tindakan koreksi."
    )

    buffer = io.BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        df_tim.to_excel(
            writer,
            sheet_name="01 Tim HACCP",
            index=False
        )

        df_deskripsi.to_excel(
            writer,
            sheet_name="02 Deskripsi Produk",
            index=False
        )

        df_tahap.to_excel(
            writer,
            sheet_name="03 Diagram Alir",
            index=False
        )

        df_bahaya.to_excel(
            writer,
            sheet_name="04 Analisis Bahaya",
            index=False
        )

        df_ccp.to_excel(
            writer,
            sheet_name="05 CCP",
            index=False
        )

        df_monitoring.to_excel(
            writer,
            sheet_name="06 Monitoring",
            index=False
        )

        df_koreksi.to_excel(
            writer,
            sheet_name="07 Tindakan Koreksi",
            index=False
        )

        pd.DataFrame([
            {
                "Nama Menu": nama_menu,
                "Bahan Terdeteksi": bahan,
                "Nama Dapur": nama_dapur,
                "PJ": penanggung_jawab,
                "Jumlah Porsi": jumlah_porsi,
                "Bahan Tambahan": bahan_tambahan,
                "Status": "Rancangan — wajib validasi"
            }
        ]).to_excel(
            writer,
            sheet_name="08 Identitas Dokumen",
            index=False
        )

        pd.DataFrame([
            {
                "Nama Menu": nama_menu,
                "Nama Bahan": info_bahan["nama"],
                "Gambar URL": gambar or "Tidak tersedia"
            }
        ]).to_excel(
            writer,
            sheet_name="09 Gambar",
            index=False
        )

        for sheet in writer.sheets.values():

            for column_cells in sheet.columns:

                max_length = 0

                column_letter = column_cells[0].column_letter

                for cell in column_cells:

                    try:
                        if cell.value is not None:
                            max_length = max(
                                max_length,
                                len(str(cell.value))
                            )
                    except Exception:
                        pass

                sheet.column_dimensions[
                    column_letter
                ].width = min(max_length + 2, 60)

    st.download_button(
        label="📊 Unduh Excel HACCP",
        data=buffer.getvalue(),
        file_name=(
            "HACCP_"
            + re.sub(
                r"[^A-Za-z0-9_-]",
                "_",
                nama_menu
            )
            + ".xlsx"
        ),
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

st.divider()

st.caption(
    "Generator HACCP V2 | Rancangan untuk validasi Tim HACCP | "
    "Bukan sertifikat HACCP"
)
