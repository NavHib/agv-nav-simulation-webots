<img width="1000" height="1000" alt="Presentation1" src="https://github.com/user-attachments/assets/baf6c7f6-dec0-405b-9fbb-48d10662c314" /># agv-nav-simulation-webots
AGV line follower simulation using Webots and Python. Implements robust PID control for multi-route navigation (Routes A, B, C)

# 🤖 Industrial AGV Line Follower - Webots Simulation

Projek ini adalah simulasi **Automated Guided Vehicle (AGV)** berbasis robot E-puck di Webots menggunakan bahasa pemrograman **Python**.
Projek ini mendemonstrasikan kendali presisi robot dalam melintasi multi-rute (Route A, B, C).

---

## 📸 Dokumentasi & Arsitektur Sistem
### 1. Robot & Custom 8-Sensor Array (infra-red)
Robot dikonfigurasi menggunakan 8-channel sensor inframerah (`PS0` - `PS7`) untuk membaca lintasan secara presisi dengan *output* berupa data biner 1-Byte `(0000 0000)`. dengan keterangan posisi seperti berikut:
* `(0011 1100)` = Robot berada tepat di tengah garis lurus.
* `(1110 0000)` = Robot berada di **tikungan kiri** (kondisi sensor kiri mendeteksi garis).
* `(0000 0111)` = Robot berada di **tikungan kanan** (kondisi sensor kanan mendeteksi garis).
* `(1111 1111)` = Robot berada di **pertigaan / persimpangan** (semua sensor membaca area hitam pekat).
* `(0000 0000)` = Robot berada di luar jalur / kehilangan garis (*Lost Line*).

### 2. Layout Sirkuit Lintasan (Line Track)
Sirkuit multi-rute tempat pengujian performa algoritma navigasi robot untuk Route A, B, dan C.
<img width="1000" height="1000" alt="Presentation1" src="https://github.com/user-attachments/assets/2a362737-ba7b-490c-98ef-a40cd625330c" />

---
## Link siimulasi 
1. line A: https://drive.google.com/file/d/1pwZipJ-K8FGP8rHXstIUKIdxK_hBBJkd/view?usp=drive_link 
2. Line B: https://drive.google.com/file/d/17WQtUp9F8tct37jq0HZi5_UY7qm8FVxj/view?usp=drive_link
3. Line C: https://drive.google.com/file/d/1YXB3EOKAeWyfwpm7457S8ZogKQ7ZuWyu/view?usp=drive_link
