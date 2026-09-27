# Video Promosi Vertikal — AKH

`promo-akh-vertical.mp4`: 1080×1920 (9:16), 33 detik, 30 fps, H.264 + AAC.
Siap untuk Reels, TikTok, YouTube Shorts, dan Status WhatsApp.

| Waktu | Adegan |
|---|---|
| 0–5 dtk | Hook: "Sering merasa… cemas / sulit tidur / takut / dihantui masa lalu?" |
| 5–9 dtk | "Anda tidak sendiri" + tagline |
| 9–15,6 dtk | 6 layanan |
| 15,6–21,4 dtk | Profil terapis Abdulah Hubai (CHt, CCH, CI, NGH-USA) |
| 21,4–26,4 dtk | Terdaftar resmi, aman, privasi terjamin |
| 26,4–33 dtk | CTA: konsultasi awal gratis, WhatsApp, alamat, jam buka |

Musik latar disintesis sendiri oleh `music.py`, jadi bebas hak cipta.

## Render ulang

```bash
pip install numpy imageio-ffmpeg
python3 music.py                      # -> music.wav
FFMPEG=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())") \
NODE_PATH=$(npm root -g) node render.mjs   # -> promo-akh-vertical.mp4
```

Untuk mengubah teks atau waktu, sunting `promo.html` (atribut `data-in`/`data-out` dalam detik).
Buka `promo.html` langsung di browser untuk pratinjau langsung, atau `promo.html?t=12` untuk melihat satu frame.
