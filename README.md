# 🧘‍♀️ YogaFlow AI

YogaFlow AI adalah aplikasi berbasis AI yang mendeteksi pose yoga secara real-time melalui kamera dan memberikan feedback koreksi postur secara langsung.

---

## 📌 Prerequisites

Pastikan sudah terinstall:

- Node.js (direkomendasikan versi 18+) → https://nodejs.org  
- Python (versi 3.8+) → https://www.python.org  
- Webcam (wajib untuk deteksi pose)

---

## ⚙️ Installation

### 1. Backend Setup

Buka terminal di root project, lalu jalankan:

```bash
cd backend
pip install -r requirements.txt
````

> Pastikan kamu berada di folder `backend`

---

### 2. Frontend Setup

Buka terminal baru, lalu jalankan:

```bash
cd frontend
npm install
```

---

## ▶️ Running the Application

Kamu bisa menjalankan aplikasi dengan dua cara:

### Option 1 — Start Script (Windows Recommended)

Jalankan file berikut dari root project:

```bash
start_app.cmd
```

Script ini akan menjalankan backend dan frontend secara otomatis.

---

### Option 2 — Manual Run

#### Start Backend

```bash
cd backend
python main.py
```

Server akan berjalan di:
[http://localhost:8000](http://localhost:8000)

---

#### Start Frontend

```bash
cd frontend
npm run dev
```

Aplikasi akan berjalan di:
[http://localhost:3000](http://localhost:3000)

---

## 🧪 How to Use

1. Buka browser dan akses:
   [http://localhost:3000](http://localhost:3000)
2. Izinkan akses kamera saat diminta
3. Pastikan seluruh tubuh terlihat di kamera
4. AI akan:

   * Mendeteksi pose yoga
   * Mengidentifikasi pose
   * Memberikan koreksi postur secara real-time
