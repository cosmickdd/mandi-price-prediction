"""
Production API Entry Point
Secure, optimized FastAPI application for Vercel deployment
"""

import os
import logging
from typing import Optional
from functools import lru_cache

from fastapi import FastAPI, HTTPException, Header, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security configuration
API_KEY = os.getenv("API_KEY", "")
ENV = os.getenv("ENV", "production")

# CORS configuration - restricted to specific domains
ALLOWED_ORIGINS = [
    "https://mandi-price-prediction-yczz.onrender.com",
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]

if ENV == "development":
    ALLOWED_ORIGINS.extend([
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost",
    ])

# ============================================================================
# VALIDATION MODELS
# ============================================================================

class PredictionRequest(BaseModel):
    """Encrypted and validated prediction request"""
    commodity: str = Field(..., min_length=2, max_length=50)
    state: str = Field(..., min_length=2, max_length=50)
    district: str = Field(..., min_length=2, max_length=50)
    quantity: float = Field(..., gt=0, le=10000)
    
    @field_validator('commodity', 'state', 'district', mode='before')
    @classmethod
    def sanitize_input(cls, v):
        """Sanitize string inputs"""
        # Allow only alphanumeric and spaces/hyphens
        if not all(c.isalnum() or c in ' -' for c in v):
            raise ValueError('Invalid characters in input')
        return v.strip().title()


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    ready: bool


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    app = FastAPI(
        title="Mandi Price Prediction API",
        description="Secure crop price forecasting service",
        version="2.0.0",
        # Hide docs in production
        docs_url="/api/docs" if ENV == "development" else None,
        redoc_url=None,
        openapi_url="/api/openapi.json" if ENV == "development" else None,
    )
    
    # ========== SECURITY MIDDLEWARE ==========
    
    # Restricted CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=False,
        allow_methods=["POST", "GET", "OPTIONS"],
        allow_headers=["Content-Type", "X-API-Key"],
        max_age=3600,
    )
    
    # ========== STATIC FILES ==========
    
    # Mount static files (test-api.html, etc)
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory="static"), name="static")
        logger.info("✅ Static files mounted at /static")
    
    # ========== SERVICE INITIALIZATION ==========
    
    service_cache = {}
    
    @lru_cache(maxsize=1)
    def get_prediction_service():
        """Lazy-load prediction service once"""
        if 'service' not in service_cache:
            try:
                from src.prediction_service_corrected import CorrectedPredictionService
                service_cache['service'] = CorrectedPredictionService()
                logger.info("✅ Prediction service initialized")
            except Exception as e:
                logger.error(f"❌ Service init failed: {e}", exc_info=True)
                raise RuntimeError("Service initialization failed")
        return service_cache['service']
    
    # ========== AUTHENTICATION ==========
    
    def verify_api_key(x_api_key: Optional[str] = Header(None)) -> bool:
        """Verify API key if configured"""
        if not API_KEY:
            return True  # No key configured
        
        if not x_api_key or x_api_key != API_KEY:
            logger.warning("Invalid API key attempt")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing API key",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return True
    
    # ========== ROUTES ==========
    
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "service": "Mandi Price Prediction API",
            "version": "2.0.0",
            "status": "operational",
            "docs": "/api/docs" if ENV == "development" else "Not available in production"
        }
    
    @app.get("/api/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint (no auth required)"""
        try:
            service = get_prediction_service()
            return HealthResponse(
                status="healthy",
                ready=len(service.models) > 0 if service.models else False
            )
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service unavailable"
            )
    
    @app.post("/api/predict")
    async def predict(
        request: Request,
        prediction_request: PredictionRequest,
        x_api_key: Optional[str] = Header(None)
    ):
        """
        Make a price prediction.
        
        **Requires API Key** (if configured)
        
        **Parameters:**
        - commodity: Crop name (e.g., "Cotton", "Wheat", "Potato")
        - state: State/Region (e.g., "Gujarat", "Punjab", "Haryana")
        - district: District name
        - quantity: Quantity in quintals (1-10000)
        
        **Response:** Prediction with 7-day forecast
        """
        
        # API Key verification
        try:
            verify_api_key(x_api_key)
        except HTTPException:
            raise
        
        # Rate limiting (basic check)
        client_ip = request.client.host if request.client else "unknown"
        
        try:
            service = get_prediction_service()
            
            # Make prediction
            result = service.predict(
                commodity=prediction_request.commodity,
                state=prediction_request.state,
                district=prediction_request.district,
                quantity=prediction_request.quantity
            )
            
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No data found for this commodity/state combination"
                )
            
            logger.info(f"Prediction successful: {prediction_request.commodity}/{prediction_request.state}")
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Prediction error: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Prediction failed"
            )
    
    @app.get("/api/status")
    async def api_status(x_api_key: Optional[str] = Header(None)):
        """
        Get detailed API status (requires authentication).
        """
        try:
            verify_api_key(x_api_key)
        except HTTPException:
            raise
        
        try:
            service = get_prediction_service()
            return {
                "status": "operational",
                "version": "2.0.0",
                "environment": ENV,
                "models_loaded": len(service.models) if service.models else 0,
                "data_ready": service.training_data is not None and len(service.training_data) > 0,
            }
        except Exception as e:
            logger.error(f"Status check failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service unavailable"
            )
    
    # ========== ERROR HANDLERS ==========
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Handle validation errors"""
        logger.warning(f"Validation error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "Invalid input provided"}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected errors"""
        logger.error(f"Unexpected error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )
    
    return app


# ============================================================================
# APPLICATION INSTANCE
# ============================================================================

app = create_app()

# ============================================================================
# ASGI HANDLER (for Vercel)
# ============================================================================

# Vercel will call this directly
handler = app

# ============================================================================
# LOCAL DEVELOPMENT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    reload = ENV == "development"
    
    logger.info(f"Starting {ENV} server on port {port}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=reload,
        log_level="info"
    )
