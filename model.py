import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score, mean_absolute_error
import pickle
import os

def calculate_sustainability_score(row):
    """Calculate sustainability score using the formula if not provided."""
    recyclability = row.get('Recyclability', 50)
    lifespan = min(row.get('Lifespan', 365), 3650)
    co2 = row.get('CO2_kg', 10)
    energy = row.get('Energy_MJ', 100)
    water = row.get('Water_L', 100)

    # Normalize components to 0-100 scale
    recyclability_norm = recyclability  # already 0-100
    lifespan_norm = min((lifespan / 3650) * 100, 100)
    co2_norm = min((co2 / 200) * 100, 100)
    energy_norm = min((energy / 500) * 100, 100)
    water_norm = min((water / 3000) * 100, 100)

    score = (
        (0.30 * recyclability_norm) +
        (0.20 * lifespan_norm) -
        (0.20 * co2_norm) -
        (0.15 * energy_norm) -
        (0.15 * water_norm)
    )
    return score

def train_model():
    """Train the RandomForest model and save it."""
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'dataset.csv'))

    # Calculate scores if not already valid
    if 'Sustainability_Score' not in df.columns:
        df['Sustainability_Score'] = df.apply(calculate_sustainability_score, axis=1)

    features = ['Energy_MJ', 'Water_L', 'CO2_kg']
    target = 'Sustainability_Score'

    X = df[features].values
    y = df[target].values

    # Scale features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # Train RandomForest
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Model trained successfully!")
    print(f"R² Score: {r2:.4f}")
    print(f"MAE: {mae:.4f}")

    # Save model and scaler
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')

    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)

    print(f"Model saved to {model_path}")
    return model, scaler

def load_model():
    """Load the trained model and scaler."""
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')

    if not os.path.exists(model_path):
        print("Model not found, training now...")
        return train_model()

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    return model, scaler

def predict_sustainability(energy, water, co2):
    """Predict sustainability score for given inputs."""
    model, scaler = load_model()

    input_data = np.array([[energy, water, co2]])
    input_scaled = scaler.transform(input_data)
    raw_score = model.predict(input_scaled)[0]

    # Clamp to 0-100
    score = float(np.clip(raw_score, 0, 100))

    # Classify
    if score > 70:
        category = "Eco-Friendly"
    elif score > 40:
        category = "Moderate"
    else:
        category = "Harmful"

    # Generate recommendation
    recommendation = generate_recommendation(score, category, energy, water, co2)

    return {
        "predicted_score": round(score, 2),
        "category": category,
        "recommendation": recommendation
    }

def generate_recommendation(score, category, energy, water, co2):
    """Generate detailed recommendation based on score and inputs."""
    if category == "Harmful":
        recs = []
        if co2 > 50:
            recs.append("⚠️ High CO₂ emissions detected. Consider switching to low-carbon alternatives or renewable energy sources.")
        if energy > 100:
            recs.append("⚡ Energy consumption is critically high. Look for energy-efficient versions (e.g., LED bulbs, Energy Star-certified appliances).")
        if water > 500:
            recs.append("💧 Water footprint is excessive. Choose products with lower water usage or opt for sustainable materials like bamboo or recycled fabrics.")
        recs.append("♻️ Switch to reusable alternatives where possible — replace single-use plastics with glass, metal, or cloth options.")
        recs.append("🌱 Prioritize products from companies with verified sustainability certifications (ISO 14001, Fair Trade, etc.).")
        return " | ".join(recs) if recs else "This product has high environmental impact. Consider eco-friendly alternatives and sustainable practices."

    elif category == "Moderate":
        recs = []
        if co2 > 20:
            recs.append("📉 Moderate CO₂ levels — consider carbon offset programs or choosing local/organic alternatives.")
        if energy > 50:
            recs.append("⚡ Reduce energy usage by choosing more efficient products or using them less frequently.")
        if water > 200:
            recs.append("💧 Water usage can be improved. Look for water-efficient production certifications.")
        recs.append("✅ You're on the right track! Small improvements in product choice can push this into the eco-friendly zone.")
        recs.append("🔄 Extend product lifespan through repair and maintenance instead of replacing.")
        return " | ".join(recs) if recs else "This product has moderate environmental impact. Small improvements can make a big difference."

    else:  # Eco-Friendly
        return (
            "🌟 Excellent sustainability score! This product demonstrates strong environmental responsibility. "
            "✅ Continue supporting products with similar impact profiles. "
            "📢 Share this data to raise awareness and encourage others to make sustainable choices. "
            "🌍 Consider advocating for industry-wide adoption of these standards."
        )

if __name__ == "__main__":
    train_model()
