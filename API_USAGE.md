# API Usage Guide

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Health Check
**GET** `/health`

Cek apakah aplikasi berjalan dan model sudah ter-load.

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": true
}
```

---

### 2. Model Status
**GET** `/api/models/status`

Cek status detail dari semua model dan daftar features yang diperlukan.

**Response:**
```json
{
  "models_loaded": true,
  "models": {
    "final_result_model": true,
    "dropout_model": true
  },
  "label_encoders": {
    "final_result": true,
    "dropout": true
  },
  "features": {
    "final_result": [
      "gender",
      "highest_education",
      "imd_band",
      "age_band",
      "num_of_prev_attempts",
      "studied_credits",
      "disability",
      "avg_assessment_score",
      "total_clicks"
    ],
    "dropout": [
      "code_module",
      "code_presentation",
      "gender",
      "region",
      "highest_education",
      "imd_band",
      "age_band",
      "num_of_prev_attempts",
      "studied_credits",
      "disability"
    ]
  }
}
```

---

### 3. Predict Final Result
**POST** `/api/predict/final-result`

Prediksi hasil akhir (final_result) mahasiswa.

**Required Features:**
- `gender`: Gender mahasiswa
- `highest_education`: Pendidikan tertinggi
- `imd_band`: Index of Multiple Deprivation band
- `age_band`: Kelompok umur
- `num_of_prev_attempts`: Jumlah percobaan sebelumnya
- `studied_credits`: Jumlah kredit yang dipelajari
- `disability`: Status disabilitas
- `avg_assessment_score`: Rata-rata skor assessment
- `total_clicks`: Total klik di VLE

**Request Body:**
```json
{
  "features": {
    "gender": "M",
    "highest_education": "HE Qualification",
    "imd_band": "50-75%",
    "age_band": "35-55",
    "num_of_prev_attempts": 0,
    "studied_credits": 120,
    "disability": "N",
    "avg_assessment_score": 75.5,
    "total_clicks": 1500
  }
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "final_result": "Pass",
    "confidence": 0.85,
    "confidence_scores": {
      "Pass": 0.85,
      "Fail": 0.10,
      "Distinction": 0.05
    }
  }
}
```

---

### 4. Predict Dropout
**POST** `/api/predict/dropout`

Prediksi apakah mahasiswa akan dropout (is_dropout).

**Required Features:**
- `code_module`: Kode modul
- `code_presentation`: Kode presentasi
- `gender`: Gender mahasiswa
- `region`: Region mahasiswa
- `highest_education`: Pendidikan tertinggi
- `imd_band`: Index of Multiple Deprivation band
- `age_band`: Kelompok umur
- `num_of_prev_attempts`: Jumlah percobaan sebelumnya
- `studied_credits`: Jumlah kredit yang dipelajari
- `disability`: Status disabilitas

**Request Body:**
```json
{
  "features": {
    "code_module": "AAA",
    "code_presentation": "2013J",
    "gender": "F",
    "region": "East Anglian Region",
    "highest_education": "A Level or Equivalent",
    "imd_band": "30-40%",
    "age_band": "0-35",
    "num_of_prev_attempts": 0,
    "studied_credits": 60,
    "disability": "N"
  }
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "is_dropout": "No",
    "confidence": 0.92,
    "confidence_scores": {
      "No": 0.92,
      "Yes": 0.08
    },
    "dropout_probability": 0.08
  }
}
```

---

## Error Responses

### Missing Features (400)
```json
{
  "detail": "Missing required features: ['avg_assessment_score', 'total_clicks']"
}
```

### Models Not Loaded (503)
```json
{
  "detail": "Models not loaded"
}
```

### Internal Error (500)
```json
{
  "detail": "Prediction failed: [error message]"
}
```

---

## Cara Menjalankan

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Jalankan aplikasi:**
   ```bash
   cd src
   python app.py
   ```
   
   Atau dengan uvicorn:
   ```bash
   cd src
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Akses API:**
   - API Docs (Swagger): http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

---

## Testing dengan cURL

### Health Check
```bash
curl http://localhost:8000/health
```

### Model Status
```bash
curl http://localhost:8000/api/models/status
```

### Predict Final Result
```bash
curl -X POST http://localhost:8000/api/predict/final-result \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "gender": "M",
      "highest_education": "HE Qualification",
      "imd_band": "50-75%",
      "age_band": "35-55",
      "num_of_prev_attempts": 0,
      "studied_credits": 120,
      "disability": "N",
      "avg_assessment_score": 75.5,
      "total_clicks": 1500
    }
  }'
```

### Predict Dropout
```bash
curl -X POST http://localhost:8000/api/predict/dropout \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "code_module": "AAA",
      "code_presentation": "2013J",
      "gender": "F",
      "region": "East Anglian Region",
      "highest_education": "A Level or Equivalent",
      "imd_band": "30-40%",
      "age_band": "0-35",
      "num_of_prev_attempts": 0,
      "studied_credits": 60,
      "disability": "N"
    }
  }'
```

---

## Testing dengan Python

```python
import requests

# Base URL
base_url = "http://localhost:8000"

# 1. Health check
response = requests.get(f"{base_url}/health")
print("Health:", response.json())

# 2. Predict Final Result
final_result_data = {
    "features": {
        "gender": "M",
        "highest_education": "HE Qualification",
        "imd_band": "50-75%",
        "age_band": "35-55",
        "num_of_prev_attempts": 0,
        "studied_credits": 120,
        "disability": "N",
        "avg_assessment_score": 75.5,
        "total_clicks": 1500
    }
}

response = requests.post(
    f"{base_url}/api/predict/final-result",
    json=final_result_data
)
print("Final Result:", response.json())

# 3. Predict Dropout
dropout_data = {
    "features": {
        "code_module": "AAA",
        "code_presentation": "2013J",
        "gender": "F",
        "region": "East Anglian Region",
        "highest_education": "A Level or Equivalent",
        "imd_band": "30-40%",
        "age_band": "0-35",
        "num_of_prev_attempts": 0,
        "studied_credits": 60,
        "disability": "N"
    }
}

response = requests.post(
    f"{base_url}/api/predict/dropout",
    json=dropout_data
)
print("Dropout:", response.json())
```

---

## Testing dengan JavaScript/Fetch

```javascript
const baseUrl = "http://localhost:8000";

// 1. Health check
fetch(`${baseUrl}/health`)
  .then(res => res.json())
  .then(data => console.log("Health:", data));

// 2. Predict Final Result
fetch(`${baseUrl}/api/predict/final-result`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    features: {
      gender: "M",
      highest_education: "HE Qualification",
      imd_band: "50-75%",
      age_band: "35-55",
      num_of_prev_attempts: 0,
      studied_credits: 120,
      disability: "N",
      avg_assessment_score: 75.5,
      total_clicks: 1500
    }
  })
})
  .then(res => res.json())
  .then(data => console.log("Final Result:", data));

// 3. Predict Dropout
fetch(`${baseUrl}/api/predict/dropout`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    features: {
      code_module: "AAA",
      code_presentation: "2013J",
      gender: "F",
      region: "East Anglian Region",
      highest_education: "A Level or Equivalent",
      imd_band: "30-40%",
      age_band: "0-35",
      num_of_prev_attempts: 0,
      studied_credits: 60,
      disability: "N"
    }
  })
})
  .then(res => res.json())
  .then(data => console.log("Dropout:", data));
```
