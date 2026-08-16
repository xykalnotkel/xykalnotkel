# XySpace GitHub Profile — Setup Guide

Paket ini dibuat untuk akun GitHub **xykalnotkel**.

## 1. Buat repository profil

1. Masuk ke GitHub.
2. Buat repository public baru.
3. Nama repository harus persis: `xykalnotkel`.
4. Jangan ubah struktur folder paket ini.
5. Unggah seluruh isi folder `xyspace-github` ke root repository tersebut.

Struktur akhirnya:

```text
xykalnotkel/
├── .github/
│   └── workflows/
│       └── snake.yml
├── assets/
│   ├── xyspace-avatar.png
│   ├── xyspace-header.gif
│   ├── xyspace-header.png
│   ├── xyspace-orbit-divider.svg
│   ├── xyspace-typing.svg
│   └── ...
└── README.md
```

File `build_assets.py` hanya diperlukan jika ingin membangun ulang banner. File tersebut boleh dihapus setelah semua aset selesai diunggah.

## 2. Aktifkan contribution snake

1. Buka repository `xykalnotkel/xykalnotkel`.
2. Masuk ke **Settings → Actions → General**.
3. Pada **Workflow permissions**, pilih **Read and write permissions**.
4. Simpan pengaturan.
5. Buka tab **Actions**.
6. Pilih workflow **Generate contribution snake**.
7. Tekan **Run workflow**.
8. Setelah berhasil, workflow membuat branch `output` dan animasi akan muncul di README.

Workflow juga berjalan otomatis setiap hari.

## 3. Gunakan avatar XySpace

Gunakan file berikut sebagai foto profil GitHub:

```text
assets/xyspace-avatar.png
```

File sudah berukuran 1024 × 1024 px dan memiliki ruang aman untuk crop lingkaran.

## 4. Atur social preview repository

Untuk preview saat repository dibagikan:

1. Buka **Settings** repository.
2. Cari **Social preview**.
3. Unggah `assets/xyspace-social-preview.png`.

## 5. Tautan yang sudah dipasang

- GitHub: `https://github.com/xykalnotkel`
- TikTok: `https://www.tiktok.com/@xyy.k4l`
- WhatsApp: `https://wa.me/6283116632566`
- Email: `haekalsaputra01h@gmail.com`
- Portfolio: `https://portofolio.haekal.web.id`
- Bio: `https://bio.xykel.my.id`

> Catatan privasi: tombol WhatsApp mengarah ke nomor publik. Hapus badge dan tautannya dari `README.md` jika nomor tidak ingin tersedia secara terbuka.

## 6. Jika banner GIF terasa berat

Banner animasi berukuran sekitar 5 MB. Untuk versi yang lebih ringan, ganti:

```html
<img src="./assets/xyspace-header.gif" ... />
```

menjadi:

```html
<img src="./assets/xyspace-header.png" ... />
```

## 7. Mengubah isi profil

Semua teks utama berada di `README.md`. Bagian yang aman diubah:

- About Haekal
- Development Orbit
- Current Mission
- Areas I Work With & Explore
- XySpace Principles

Statistik sudah diarahkan ke username `xykalnotkel`.
