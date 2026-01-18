
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestRegressor
from model_utils import calculate_aqi

print("📥 Loading dataset...")

# ensure model folder exists
os.makedirs("model", exist_ok=True)

# load dataset (CSV only)
df = pd.read_csv("dataset/dataset.csv")

print("✅ Dataset loaded successfully")

# pivot table
pivot = df.pivot_table(
    index=["city", "last_update"],
    columns="pollutant_id",
    values="pollutant_avg",
    aggfunc="mean"
).fillna(0)

print("🔄 Pivot table created")

# ensure all required columns exist
for col in ["PM2.5", "PM10", "NO2", "SO2", "CO", "OZONE"]:
    if col not in pivot.columns:
        pivot[col] = 0

# calculate AQI
pivot["AQI"] = pivot.apply(lambda x: calculate_aqi({
    "PM2.5": x["PM2.5"],
    "PM10": x["PM10"],
    "NO2": x["NO2"],
    "SO2": x["SO2"],
    "CO": x["CO"],
    "O3": x["OZONE"]   # OZONE → O3 mapping
}), axis=1)

print("📊 AQI calculated")

# features & target
X = pivot[["PM2.5", "PM10", "NO2", "SO2", "CO", "OZONE"]]
y = pivot["AQI"]

# train model
model = RandomForestRegressor(random_state=42)
model.fit(X, y)

# save model
with open("model/aqi_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("🎉 SUCCESS: model/aqi_model.pkl generated")
