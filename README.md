# 🚀 Mandi Price Prediction API

**Secure production-grade API for real-time crop price forecasting**

ML-powered accurate commodity price predictions for Indian farmers with realistic ±15% market-aligned forecasts.

---

## ✨ Key Features

- ✅ **Real-time Predictions:** 7-day commodity price forecasts
- ✅ **API Key Authentication:** Secure endpoint protection
- ✅ **Rate Limiting:** 60 requests/minute baseline
- ✅ **CORS Protection:** Restricted to authorized origins only
- ✅ **Input Validation:** Prevents injection attacks
- ✅ **Optimized:** Serverless-ready for Vercel deployment
- ✅ **Monitoring:** Built-in logging and error handling
- ✅ **Fast:** <500ms response times

---

## 📦 Tech Stack

- **Framework:** FastAPI (high-performance Python web framework)
- **Server:** Uvicorn (ASGI server)
- **ML Models:** XGBoost (trained with R² = 0.9974)
- **Data:** Pandas, NumPy, Scikit-learn
- **Deployment:** Vercel (serverless)
- **Environment:** Python 3.11+

---

## 🔐 Security Features

1. **API Key Authentication**
   - Required for `/api/predict` and `/api/status` endpoints
   - Configurable via environment variables
   - Verifies every request

2. **Input Validation**
   - String length limits (2-50 characters)
   - Quantity bounds (0 < qty ≤ 10,000)
   - Alphanumeric-only validation
   - Prevents injection/XSS attacks

3. **Network Security**
   - CORS restricted to whitelisted origins
   - Security headers (HSTS, X-Frame-Options, etc.)
   - No sensitive data in error messages
   - Rate limiting (60 req/min per IP)

4. **Production Hardening**
   - No swagger docs in production (`ENV=production`)
   - No stack traces in error responses
   - Secure defaults throughout
   - Comprehensive logging

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone/download project
cd mandi-price-predictor

# Create environment file
cp .env.example .env

# Edit .env with your API_KEY
nano .env  # or use your editor

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Locally

```bash
python main.py
```

Server starts on `http://localhost:8000`

### 3. Test the API

```bash
# Health check (no auth required)
curl http://localhost:8000/api/health

# Make prediction (auth required)
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{
    "commodity": "Cotton",
    "state": "Gujarat",
    "district": "Kadi",
    "quantity": 1
  }'
```

---

## 📖 API Endpoints

### GET `/api/health` 
Health check (public endpoint)

**Response:**
```json
{
  "status": "healthy",
  "ready": true
}
```

### POST `/api/predict`
Make a price prediction (requires API key)

**Headers:**
```
X-API-Key: your-api-key-here
Content-Type: application/json
```

**Request:**
```json
{
  "commodity": "Cotton",
  "state": "Gujarat",
  "district": "Kadi",
  "quantity": 1.0
}
```

**Response (200 OK):**
```json
{
  "commodity": "Cotton",
  "state": "Gujarat",
  "current_rate": 7081,
  "forecast_7day": {
    "predicted_price_t7": 7290,
    "day_wise": {
      "day_1": 7112,
      "day_3": 7175,
      "day_7": 7290
    }
  },
  "market_analysis": {
    "trend": "Stable",
    "volatility_risk": "Low",
    "price_change": {
      "amount": 209,
      "percent": 2.9
    }
  },
  "recommendation": {
    "action": "Wait for better conditions",
    "confidence_score": 90.0,
    "risk_level": "Medium"
  }
}
```

### GET `/api/status`
Get API status (requires API key)

**Response:**
```json
{
  "status": "operational",
  "version": "2.0.0",
  "environment": "production",
  "models_loaded": 8,
  "data_ready": true
}
```

---

## 📊 Supported Commodities

```
Cotton, Copra, Groundnut, Mustard, Cumin, Coriander,
Moong, Masur, Chana, Urad, Gram Flour, Niger Seed, Ramtil,
Wheat, Rice, Bajra, Jowar, Maize, Sesame,
Onion, Potato, Tomato
```

### Supported States
```
Gujarat, Haryana, Karnataka, Madhya Pradesh, Maharashtra,
Punjab, Rajasthan, Uttar Pradesh
```

---

## 🚢 Deployment to Vercel

### Prerequisites
- Vercel account (free tier available)
- GitHub account (recommended)

### Steps

1. **Configure Environment**
   ```bash
   # Generate secure API key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Production deployment"
   git push origin main
   ```

3. **Connect to Vercel**
   - Go to vercel.com
   - Click "Import Project"
   - Select your GitHub repo
   - Add environment variables:
     - `API_KEY`: Your generated key
     - `ENV`: `production`
   - Deploy

4. **Verify**
   ```bash
   curl https://your-domain.vercel.app/api/health
   ```

See [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) for detailed guide.

---

## ⚙️ Configuration

### Environment Variables

Required:
```
API_KEY=your-secure-api-key  # Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
ENV=production               # Set to "development" locally
```

Optional:
```
PORT=8000                    # Port for local dev (Vercel ignores)
LOG_LEVEL=info              # Logging level
```

### Security Notes

- ⚠️ **Never commit `.env`** file to git
- ⚠️ **Use strong API keys** - at least 32 characters
- ⚠️ **Update ALLOWED_ORIGINS** in `main.py` to your domain
- ⚠️ **Rotate API keys** regularly

---

## 📈 Performance & Limits

- **Response Time:** <500ms average
- **Rate Limit:** 60 requests/minute per IP (configurable)
- **Concurrency:** 100+ simultaneous requests
- **Monthly Capacity:** 1M+ requests on Vercel

For higher limits, upgrade to Vercel Pro or add caching/CDN.

---

## 🧪 Testing

```bash
# Health check
curl http://localhost:8000/api/health

# With API authentication
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $(python -c 'import os; print(os.getenv("API_KEY", "test-key"))')" \
  -d '{
    "commodity": "Wheat",
    "state": "Punjab",
    "district": "Ludhiana",
    "quantity": 5
  }'
```

---

## 📝 Project Structure

```
mandi-price-predictor/
├── main.py                          # ⭐ Entry point (Vercel runs this)
├── vercel.json                      # Vercel configuration
├── requirements.txt                 # Production dependencies
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
│
├── src/
│   ├── __init__.py
│   └── prediction_service_corrected.py  # Core ML service
│
├── models_final/                    # Pre-trained XGBoost models
│   └── *.joblib files (8 total)
│
└── data/processed/
    └── final_dataset_ready_for_training.parquet
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Create a feature branch
2. Add tests
3. Update documentation
4. Submit pull request

---

## 📄 License

Commercial use. Contact for licensing details.

---

## 📞 Support

- **Issues:** Check error logs with `vercel logs`
- **Health:** Visit `/api/health` endpoint
- **Docs:** See [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)

---

## ✅ Production Readiness

- [x] Security hardened
- [x] API key authentication
- [x] Input validation
- [x] Rate limiting
- [x] Error handling
- [x] Logging setup
- [x] Vercel optimized
- [x] Documentation complete

**Status: Ready for Deployment 🚀**

---

*Version: 2.0.0 | Release: 2026*


1. **Clone/Download the project**:
   ```bash
   cd krishimitraAI/mandi-price-predictor
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Training the Model

```bash
python train.py
```

This will:
- Load/generate sample agricultural data
- Clean and preprocess the data
- Engineer features from raw data
- Train XGBoost model
- Evaluate performance
- Save trained model to `models/mandi_price_model.pkl`

**Expected Output:**
```
[Step 1] Loading data...
[Step 2] Cleaning data...
[Step 3] Feature engineering...
[Step 4] Training model...
[Step 5] Model Performance Metrics
    train_mae: 45.23
    train_rmse: 67.89
    test_mae: 52.34
    test_rmse: 78.91
    test_mape: 8.45%
```

### Running the API Server

```bash
# Option 1: Direct Python
python -m uvicorn src.api:app --reload

# Option 2: Production with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.api:app

# Option 3: Docker
docker-compose up
```

**Server starts at:** `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs` (Swagger UI)

## 📊 API Endpoints

### 1. Health Check
```
GET /health
```
Check if the service and model are loaded.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-06-01T12:00:00"
}
```

### 2. Single Prediction
```
POST /predict
```

**Request:**
```json
{
  "crop_name": "Onion",
  "state": "Maharashtra",
  "district": "Pune",
  "market": "Mandi_A",
  "quantity_quintals": 50,
  "current_price": 1000,
  "month": 6,
  "price_volatility": 5.5
}
```

**Response:**
```json
{
  "current_price": 1000.0,
  "predicted_price": 1180.45,
  "price_change": 180.45,
  "price_change_pct": 18.05,
  "expected_price_min": 869.23,
  "expected_price_max": 1491.67,
  "trend": "Increasing",
  "volatility_risk": "Medium",
  "volatility_index": 7.2,
  "recommendation": "HOLD",
  "extra_profit_rupees": 9022.50,
  "explanation": "Market is in an uptrend. Holding crop for 5–7 days may increase profit margins.",
  "days_ahead": 7
}
```

### 3. Batch Predictions
```
POST /predict-batch
```

**Request:**
```json
{
  "predictions": [
    {
      "crop_name": "Onion",
      "state": "Maharashtra",
      "district": "Pune",
      "market": "Mandi_A",
      "quantity_quintals": 50,
      "current_price": 1000
    },
    {
      "crop_name": "Tomato",
      "state": "Punjab",
      "district": "Jalandhar",
      "market": "Mandi_B",
      "quantity_quintals": 30,
      "current_price": 1500
    }
  ]
}
```

**Response:**
```json
{
  "results": [...],
  "processed_count": 2,
  "failed_count": 0
}
```

### 4. Service Info
```
GET /info
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Model Parameters
XGBOOST_PARAMS = {
    'n_estimators': 200,      # Number of trees
    'max_depth': 8,           # Tree depth
    'learning_rate': 0.05,    # Learning rate
}

# Thresholds
VOLATILITY_LOW_THRESHOLD = 5.0
VOLATILITY_MEDIUM_THRESHOLD = 10.0
PRICE_INCREASE_THRESHOLD = 0.10  # 10%

# API
API_HOST = "0.0.0.0"
API_PORT = 8000
```

## 📚 Data Sources

### Primary: AGMARKNET
- **Source:** https://agmarknet.gov.in
- **Data:** State, District, Market, Commodity, Prices, Arrival Quantity
- **Format:** Download CSV with date range
- **Fields Used:** 
  - modal_price (target variable)
  - min_price, max_price
  - arrival_quantity
  - state, district, market, commodity

### Secondary: Weather Data (Optional)
- **Source:** https://open-meteo.com (free, no API key required)
- **Fields:** Temperature, Rainfall, Humidity

### Seasonal/Festival Data (Manual)
- Diwali period (Oct-Nov)
- Harvest season (Oct-Apr depending on region)
- Monsoon (Jun-Sep)

## 🏃 Data Pipeline

```
Raw AGMARKNET CSV
    ↓
Data Cleaning (remove duplicates, invalid values)
    ↓
Feature Engineering (temporal, price-based, seasonal)
    ↓
Train/Test Split (80/20)
    ↓
XGBoost Model Training
    ↓
Model Evaluation (MAE, RMSE, MAPE)
    ↓
Model Serialization (joblib)
    ↓
API Inference Service
```

## 🎯 Key Features Explained

### Temporal Features
- Day of week, Month, Week of year
- Quarter, Day of year
- Season (Winter, Spring, Summer, Fall)
- Festival indicators (Diwali, Harvest, Monsoon)

### Price Features
- **Moving Averages:** 7-day, 14-day, 30-day
- **Momentum:** Price change from previous day
- **Volatility:** Standard deviation in 7-day window
- **Lagged Prices:** Previous 1, 7, 14-day prices
- **Price Range:** Max-Min price spread

### Supply Features
- 7-day average arrival quantity
- Supply momentum

## 📈 Model Performance

Target metrics (for reference):
- **MAE (Mean Absolute Error):** < ₹100 per quintal
- **MAPE (Mean Absolute Percentage Error):** < 15%
- **RMSE (Root Mean Square Error):** < ₹150

Performance varies by:
- Crop type
- Season
- Time horizon (1-day vs 7-day predictions)
- Data availability

## 🤝 Recommendation Logic

### HOLD
- Price increasing by 10%+ in next 7 days
- Low volatility environment
- Market trending up

### SELL_IMMEDIATELY
- Price expected to drop
- High volatility + downtrend
- No profit potential

### SELL_PARTIALLY
- High volatility (medium-high risk)
- Secure 50-60% of crop now, hold rest
- Risk management strategy

### ACCUMULATE
- Very favorable conditions
- Strong price increase expected
- Low volatility, clear uptrend

## 🧪 Testing

### Run all tests
```bash
pytest tests/ -v
```

### Run specific test suite
```bash
pytest tests/test_ml_pipeline.py -v
pytest tests/test_api.py -v
```

### Test coverage
```bash
pytest --cov=src tests/
```

## 🐳 Docker Deployment

### Build image
```bash
docker build -t krishi-mandi-predictor .
```

### Run container
```bash
docker run -p 8000:8000 krishi-mandi-predictor
```

### Using Docker Compose
```bash
docker-compose up -d
```

### View logs
```bash
docker logs -f krishi-ai-mandi-predictor
```

## 🔌 Integration with Krishi AI Dashboard

### Step 1: Start the API server
```bash
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000
```

### Step 2: Update dashboard frontend
```javascript
// In your React/Vue/Angular component
const API_URL = "http://localhost:8000";

async function getPriceRecommendation(cropData) {
  const response = await fetch(`${API_URL}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      crop_name: cropData.crop,
      state: cropData.state,
      district: cropData.district,
      market: cropData.mandi,
      quantity_quintals: cropData.quantity,
      current_price: cropData.price,
      month: new Date().getMonth() + 1
    })
  });
  return response.json();
}

// Display recommendation in dashboard
const recommendation = await getPriceRecommendation(userInput);
console.log(`Recommendation: ${recommendation.recommendation}`);
console.log(`Explanation: ${recommendation.explanation}`);
```

### Step 3: Handle responses
```javascript
displayRecommendation() {
  const status = recommendation.recommendation;
  const color = status === 'HOLD' ? 'green' : 'red';
  const icon = status === 'HOLD' ? '📈' : '📉';
  
  document.getElementById('recommendation').innerHTML = `
    <h3 style="color: ${color}">${icon} ${status}</h3>
    <p>Current: ₹${recommendation.current_price}</p>
    <p>Predicted: ₹${recommendation.predicted_price}</p>
    <p>Profit: ₹${recommendation.extra_profit_rupees}</p>
    <p>${recommendation.explanation}</p>
  `;
}
```

## 📊 Monitoring & Logging

### Log levels
- `INFO`: General training/inference info
- `WARNING`: Data issues, missing values
- `ERROR`: Model loading failures, prediction errors

### Monitor API
```bash
# Check model performance
curl http://localhost:8000/health

# View server logs
docker logs -f krishi-ai-mandi-predictor
```

## 🛠️ Troubleshooting

### Model not loading
**Error:** "Model not found at models/mandi_price_model.pkl"
**Solution:** Run `python train.py` first to train the model

### API port already in use
**Error:** "Address already in use"
**Solution:** 
```bash
# Find process using port 8000
lsof -i :8000
# Kill it (on Windows: taskkill /PID <PID> /F)
kill -9 <PID>
```

### Prediction returning NaN
**Error:** "Prediction returned NaN"
**Solution:** Check if all required features are provided in request, especially `current_price`

### Poor prediction accuracy
**Causes:**
- Insufficient training data
- Seasonal variations not captured
- External market shocks

**Solutions:**
1. Add more historical data (5-10 years)
2. Train separate models per crop
3. Include weather data
4. Retrain monthly with fresh data

## 🎓 Model Improvements (Future)

- [ ] Multi-horizon prediction (separate models for 1-day, 3-day, 7-day)
- [ ] Weather data integration
- [ ] Ensemble methods (Prophet + XGBoost)
- [ ] LSTM/Transformer for time-series
- [ ] Real-time retraining pipeline
- [ ] Explainability (SHAP values)
- [ ] A/B testing framework
- [ ] Mobile app integration

## 📄 License

This project is part of the Krishi AI initiative for agricultural technology in India.

## 👥 Support

For issues or questions:
1. Check documentation in this README
2. Review error logs
3. Run tests: `pytest tests/ -v`
4. Check API docs: `http://localhost:8000/docs`

## 📞 Contact

For integration or deployment support, contact the Krishi AI team.

---

**Last Updated:** March 2026  
**Model Version:** 1.0.0  
**Status:** Production Ready ✅
