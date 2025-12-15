# KPI Dashboard - Dokumentasi

Dokumentasi ringkas 6 KPI untuk sistem dashboard analytics.

---

## Ringkasan KPI

| ID | Nama | Kategori | Sumber Data | Formula | ML? |
|----|------|----------|-------------|---------|-----|
| 1 | Forum Participation Score | Engagement | `studentvle.sum_click` | SUM(sum_click) | ❌ |
| 2 | Task Completion Ratio | Academic | `studentassessment.score` | COUNT(score > 50) / COUNT(*) × 100% | ❌ |
| 3 | Assignment Timeliness | Academic | `studentassessment.date_submitted`, `assessments.date` | COUNT(submitted ≤ deadline) / COUNT(*) × 100% | ❌ |
| 4 | Grade Performance Index | Academic | `studentassessment.score` | AVG(score) | ❌ |
| 5 | Low Activity Alert Index | Risk | `studentvle.sum_click` | COUNT(clicks < avg×0.5) / COUNT(*) × 100% | ❌ |
| 6 | Predicted Dropout Risk ⭐ | Risk | `studentinfo` + `studentvle` + `studentassessment` | ML Model Prediction | ✅ |

---

## Detail KPI

### KPI 1: Forum Participation Score
- **Definisi:** Total klik aktivitas diskusi mahasiswa
- **Tabel:** `studentvle`
- **Kolom:** `sum_click`, `id_student`
- **Output:** Total clicks, jumlah student aktif

### KPI 2: Task Completion Ratio
- **Definisi:** Persentase assessment dengan score > 50
- **Tabel:** `studentassessment`
- **Kolom:** `score`
- **Output:** Persentase completion, jumlah completed/total

### KPI 3: Assignment Timeliness
- **Definisi:** Persentase tugas dikumpulkan tepat waktu
- **Tabel:** `studentassessment` JOIN `assessments`
- **Kolom:** `date_submitted`, `date` (deadline)
- **Output:** Persentase on-time, jumlah on-time/total

### KPI 4: Grade Performance Index
- **Definisi:** Rata-rata nilai assessment
- **Tabel:** `studentassessment`
- **Kolom:** `score`
- **Output:** Avg, min, max score

### KPI 5: Low Activity Alert Index
- **Definisi:** Persentase mahasiswa dengan aktivitas < 50% rata-rata kelas
- **Tabel:** `studentvle`
- **Kolom:** `sum_click`
- **Output:** Persentase low activity, threshold

### KPI 6: Predicted Dropout Risk (ML) 
- **Definisi:** Prediksi risiko dropout dengan ML model
- **Tabel:** `studentinfo` + `studentvle` + `studentassessment`
- **Kolom:** `gender`, `age_band`, `studied_credits`, `num_of_prev_attempts`, `sum_click`, `score`
- **Proses:**
  1. Sample random 20% mahasiswa
  2. Ambil 6 features per student
  3. Encode features (gender/age_band → numeric)
  4. Predict dengan ML model (1=dropout, 0=tidak)
  5. Hitung persentase dropout
- **Output:** Persentase prediksi dropout, jumlah sample
- **Note:** Butuh model trained, proses 3-5s, hasil bervariasi (random sampling)

---

## Database Schema (Kolom Penting)

**studentvle:** `id_student`, `sum_click` (KPI 1, 5, 6)  
**studentassessment:** `id_student`, `id_assessment`, `score`, `date_submitted` (KPI 2, 3, 4, 6)  
**assessments:** `id_assessment`, `date` (KPI 3)  
**studentinfo:** `id_student`, `gender`, `age_band`, `studied_credits`, `num_of_prev_attempts` (KPI 6)

---

## API Endpoints

```bash
GET  /api/kpi/metrics                # Get all KPIs (cached)
GET  /api/kpi/metrics?refresh=true   # Force refresh
GET  /api/kpi/cache/info             # Cache status
POST /api/kpi/cache/clear            # Clear cache
```

---

## Configuration

```env
KPI_CACHE_TTL_SECONDS=300  # Cache duration (5 min default)
SAMPLE_SIZE=0.2            # KPI 6 sample size (20% default)
```

**Rekomendasi:**
- Cache: 5-10 menit untuk balance performa
- Sample: 0.2 (20%) untuk balance akurasi & kecepatan
