# api.py - Fixed FastAPI Backend (SHAP for Single Sample + Insights - No Auth for Dev)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import uvicorn
from typing import Dict, List
import os
from datetime import datetime
import shap

app = FastAPI(title="FMCG Oracle API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models and features from outputs_final_model
models = {}
features_dict = {}
output_dir = "outputs_final_model"
if not os.path.exists(output_dir):
    raise ValueError(f"Directory '{output_dir}' not found. Ensure models are saved there.")

for file in os.listdir(output_dir):
    if file.endswith("_model.pkl"):
        cat = file.replace("_model.pkl", "")
        try:
            models[cat] = joblib.load(os.path.join(output_dir, f"{cat}_model.pkl"))
            features_dict[cat] = joblib.load(os.path.join(output_dir, f"{cat}_features.pkl"))
            print(f"Loaded model for {cat}")
        except Exception as e:
            print(f"Error loading {cat}: {e}")

# Load processed data for defaults and insights - Cross-platform path handling
data_path = os.path.join(output_dir, "processed_data.csv")
try:
    processed_df = pd.read_csv(data_path, parse_dates=["date"])
    print("Loaded processed_data.csv for defaults and insights")
except FileNotFoundError:
    print("Warning: processed_data.csv not found. Using empty DF.")
    processed_df = pd.DataFrame()

class PredictRequest(BaseModel):
    category: str
    sku: str
    date: str
    price_unit: float = 105.0
    promotion_flag: int = 0
    stock_available: int = 275
    delivery_days: int = 3

@app.post("/predict")
async def predict_single(req: PredictRequest):
    cat = req.category
    if cat not in models:
        raise HTTPException(status_code=404, detail=f"Model for category '{cat}' not found in {output_dir}")
    
    model = models[cat]
    feats = features_dict[cat]
    
    # Date features
    pred_date = pd.to_datetime(req.date)
    dayofweek = pred_date.dayofweek
    month = pred_date.month
    day = pred_date.day
    
    # Basic input
    input_data = {
        "price_unit": req.price_unit,
        "promotion_flag": req.promotion_flag,
        "stock_available": req.stock_available,
        "delivery_days": req.delivery_days,
        "dayofweek": dayofweek,
        "month": month,
        "day": day
    }
    
    # Fill missing with category means
    if not processed_df.empty:
        cat_df = processed_df[processed_df["category"] == cat]
        if not cat_df.empty:
            cat_means = cat_df[feats].mean().to_dict()
            for f in feats:
                if f not in input_data:
                    input_data[f] = cat_means.get(f, 0)
        else:
            global_means = processed_df[feats].mean().to_dict()
            for f in feats:
                if f not in input_data:
                    input_data[f] = global_means.get(f, 0)
    else:
        for f in feats:
            if f not in input_data:
                input_data[f] = 0
    
    # Predict
    input_df = pd.DataFrame([input_data])[feats]
    pred = max(0, model.predict(input_df)[0])
    
    # SHAP (Fixed for single sample: 1D array)
    explainer = shap.TreeExplainer(model)
    shap_vals = explainer.shap_values(input_df.iloc[0:1])[0]  # Ensure single row; [0] for 1D
    shap_summary = dict(zip(feats, np.abs(shap_vals)))  # Direct abs for single sample
    
    return {
        "prediction": float(pred),
        "confidence_interval": [float(pred - 20), float(pred + 20)],
        "shap_importance": shap_summary
    }

# Insights endpoint - Avg SHAP across sample data
@app.get("/insights/{category}")
async def get_insights(category: str, sample_size: int = 100):
    if category not in models:
        raise HTTPException(status_code=404, detail=f"No model for '{category}'")
    
    model = models[category]
    feats = features_dict[category]
    
    if processed_df.empty:
        raise HTTPException(status_code=404, detail="No data for insights")
    
    cat_df = processed_df[processed_df["category"] == category]
    if cat_df.empty:
        raise HTTPException(status_code=404, detail=f"No data for category '{category}'")
    
    # Sample rows (with date features if needed)
    sample_df = cat_df.sample(min(sample_size, len(cat_df)))[feats]
    
    # Compute SHAP for sample
    explainer = shap.TreeExplainer(model)
    shap_vals_sample = explainer.shap_values(sample_df)
    avg_shap = np.mean(np.abs(shap_vals_sample), axis=0)  # Avg abs per feature
    
    insights = dict(zip(feats, avg_shap))
    top_driver = max(insights, key=lambda k: insights[k])
    top_impact = insights[top_driver]
    
    top_impact_pct = f"{(top_impact / np.sum(avg_shap) * 100):.1f}%"

    return {
    "category": category,
    "top_driver": top_driver,
    "top_impact_pct": top_impact_pct,
    "avg_shap_importance": insights,
    "key_takeaway": f"{top_driver} explains ~{top_impact_pct} of demand variance—optimize it first!"
}

@app.get("/health")
def health():
    return {"status": "healthy", "loaded_models": len(models), "total_features_avg": np.mean([len(f) for f in features_dict.values()]) if features_dict else 0}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)