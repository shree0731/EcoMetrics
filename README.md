# 🌿 EcoMetrics — Multi-Product Life Cycle Analysis & Environmental Dashboard

A professional-grade sustainability intelligence platform featuring interactive LCA dashboards, stakeholder survey analytics, environmental education, and an AI-powered sustainability score predictor.

---

## 📁 Project Structure

```
sustainability-platform/
├── backend/
│   ├── app.py              # Flask server (main API)
│   ├── model.py            # ML model (RandomForestRegressor)
│   ├── dataset.csv         # Training data (35 products)
│   └── requirements.txt    # Python dependencies
└── frontend/
    └── index.html          # Complete single-file frontend
```

---

## 🚀 Quick Start

### Step 1 — Install Python Dependencies

Make sure you have Python 3.8+ installed.

```bash
cd sustainability-platform/backend
pip install flask flask-cors pandas scikit-learn numpy
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### Step 2 — Start the Backend Server

```bash
cd backend
python app.py
```

You should see:
```
Loading ML model...
Training model for first time...
Model trained successfully!
R² Score: 0.9XXX
MAE: X.XXXX
Model ready!
 * Running on http://0.0.0.0:5000
```

### Step 3 — Open the Frontend

Open `frontend/index.html` directly in your browser:
- Double-click the file, OR
- Right-click → Open with → Browser

That's it! 🎉

---

## 🔌 API Reference

### Health Check
```
GET http://127.0.0.1:5000/health
```

### Predict Sustainability Score
```
POST http://127.0.0.1:5000/predict
Content-Type: application/json

{
  "energy": 350,
  "water": 1500,
  "co2": 200
}
```

**Response:**
```json
{
  "predicted_score": 18.5,
  "category": "Harmful",
  "recommendation": "⚠️ High CO₂ emissions detected..."
}
```

### Get All Product Data
```
GET http://127.0.0.1:5000/products
```

---

## 🤖 ML Model Details

- **Algorithm**: RandomForestRegressor (scikit-learn)
- **Features**: Energy_MJ, Water_L, CO2_kg
- **Target**: Sustainability_Score (0–100)
- **Training Data**: 35 products
- **Formula** (when score unavailable):
  ```
  score = (0.3 × Recyclability) + (0.2 × Lifespan) 
        - (0.2 × CO2) - (0.15 × Energy) - (0.15 × Water)
  ```

### Classification Logic
| Score Range | Category     |
|-------------|--------------|
| 70 – 100    | Eco-Friendly |
| 40 – 70     | Moderate     |
| 0 – 40      | Harmful      |

---

## 🎨 Features

| Page       | Features                                              |
|------------|-------------------------------------------------------|
| Home       | Hero section, animated stats, product impact bars     |
| Dashboard  | 4 interactive Chart.js charts (Energy/CO₂/Water/Waste)|
| Insights   | 6 insight cards (critical findings from LCA data)     |
| Survey     | 24-response stakeholder analytics, pie/bar charts     |
| Education  | 4 tabbed topics: CO₂, Water, E-Waste, Plastic         |
| Predict    | ML predictor with sliders, presets, ring score, recs  |
| About      | Platform overview, tech stack, stakeholder report     |

---

## 🛠️ Tech Stack

| Layer     | Technology                    |
|-----------|-------------------------------|
| Frontend  | HTML5, CSS3, Vanilla JS        |
| Charts    | Chart.js 4.4                  |
| Backend   | Python Flask                  |
| ML        | scikit-learn RandomForest     |
| Data      | Pandas, NumPy                 |
| Fonts     | Syne, DM Sans (Google Fonts)  |

---

## 💡 Offline Mode

If the Flask backend is not running, the frontend automatically falls back to a **client-side scoring model** that mirrors the server-side formula. A toast notification will indicate which mode is active.

---

## 📊 Data Sources

- Product LCA data: Based on published lifecycle assessment studies
- Survey data: 24 stakeholder responses (primary research)
- ML training: 35 diverse product profiles

---

*Built with 💚 for a sustainable future*
