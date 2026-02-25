<div align="center">
  <h1>🎓 SIMAkademik</h1>
  <p><strong>Modern School Management System Built with Django</strong></p>
  
  <br>
  
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
</div>

<hr>

<h2>✨ About SIMAkademik</h2>
<p><strong>SIMAkademik</strong> adalah sistem manajemen akademik berbasis web yang dirancang untuk membantu sekolah dalam mengelola operasional harian secara efisien dan terstruktur. Dirancang dengan <strong>arsitektur modular</strong> agar mudah dikembangkan menjadi sistem skala besar atau SaaS.</p>

<h2>🚀 Features</h2>
<ul>
  <li><b>👥 User & Role Management:</b> Custom User Model, Role-Based Auth, Group & Permission Support.</li>
  <li><b>🎓 Academic Management:</b> Manajemen siswa, guru, kelas, dan mata pelajaran.</li>
  <li><b>📊 Attendance & Grades:</b> Sistem absensi, penilaian, dan struktur siap untuk raport digital.</li>
  <li><b>🛠 Admin Dashboard:</b> Modern UI (AdminLTE), Custom branding, & Clean layout.</li>
</ul>

<h2>🏗 Project Architecture</h2>
<pre>
SIMAkademik/
├── apps/
│   ├── accounts/, academics/, students/, teachers/
│   ├── attendance/, grades/, website/
└── config/
    └── settings/ (base, dev, prod)
</pre>

<h2>⚙️ Installation Guide</h2>
<ol>
  <li><b>Clone Repository</b><br><code>git clone https://github.com/username/SIMAkademik.git && cd SIMAkademik</code></li>
  <li><b>Setup Virtual Environment</b><br><code>python3 -m venv venv && source venv/bin/activate</code></li>
  <li><b>Install Dependencies</b><br><code>pip install -r requirements.txt</code></li>
  <li><b>Setup .env</b> (DEBUG, SECRET_KEY, DATABASE_URL, ALLOWED_HOSTS)</li>
  <li><b>Run Migration</b><br><code>python manage.py migrate</code></li>
  <li><b>Run Server</b><br><code>python manage.py runserver</code></li>
</ol>

<blockquote>
  <b>🔐 Authentication Note:</b> AUTH_USER_MODEL = "accounts.User" <br>
  ⚠️ <i>Jangan ubah setelah migration pertama.</i>
</blockquote>

<h2>🛣 Roadmap</h2>
<ul>
  <li>☐ Dashboard Statistik</li>
  <li>☐ Export Nilai ke PDF</li>
  <li>☐ REST API (DRF)</li>
  <li>☐ Multi-school (SaaS)</li>
  <li>☐ Deployment Guide (VPS / Docker)</li>
</ul>

<hr>

<div align="center">
  <p>Developed with ❤️ by <b>LapakNgoding</b></p>
  <p><em>License: MIT</em></p>
</div>
