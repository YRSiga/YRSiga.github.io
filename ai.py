import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import time

# Initialize Firebase Admin
cred = credentials.Certificate('cred.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://siddhi-project-67c6e-default-rtdb.firebaseio.com/'
})

# Function to fetch data from Firebase
def fetch_data():
    ref = db.reference('/realtime')
    data = ref.get()
    df = pd.DataFrame(data.values())
    # Ensure correct column name for timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')  # Convert to datetime format
    return df


# Preprocess data
def preprocess_data(df):
    df = df.dropna()
    return df

# Train Nutrient Deficiency Prediction model
def train_nutrient_model(X_train, y_train):
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model

# Function to predict nutrient deficiency
def predict_nutrient_deficiency(model, X_test):
    return model.predict(X_test)

# Generate user-friendly recommendations with parameter values
def generate_recommendations(df, nutrient_predictions):
    recommendations = []
    # Sort data by timestamp and select the latest 3 timestamps
    processed_data = df.sort_values(by='timestamp', ascending=False).head(3)
    for index, row in processed_data.iterrows():
        recommendation = f"Timestamp: {row['timestamp']}\n"
        recommendation += f"Potassium (K): {row['K']}\n"
        recommendation += f"Nitrogen (N): {row['N']}\n"
        recommendation += f"Phosphorus (P): {row['P']}\n"
        recommendation += f"Soil Moisture: {row['Soil Moisture']}\n"
        recommendation += f"EC (Electrical Conductivity): {row['ec']}\n"
        recommendation += f"Humidity: {row['humidity']}\n"
        recommendation += f"pH: {row['ph']}\n"
        
        # Add nutrient deficiency recommendation
        if nutrient_predictions[index] == 1:
            recommendation += "Your soil might need nutrients. Consider fertilizing your plants.\n"
        else:
            recommendation += "Your soil nutrient levels seem adequate.\n"
            
        # Add soil moisture recommendation
        if row['Soil Moisture'] < 40:
            recommendation += "Your soil is dry. Consider watering your plants.\n"
        elif row['Soil Moisture'] > 60:
            recommendation += "Your soil is moist. Avoid overwatering.\n"
        else:
            recommendation += "Your soil moisture levels seem balanced.\n"
        
        recommendations.append(recommendation)
    return recommendations

# Main function to run the analysis and generate recommendations
def run_analysis():
    # Fetch and preprocess data
    data = fetch_data()
    processed_data = preprocess_data(data)
    
    # Check if there is enough recent data available
    if len(processed_data) < 5:
        print("Insufficient recent data available for analysis. Unable to generate recommendations.")
        return
    
    # Split data for nutrient deficiency prediction
    X_nutrient = processed_data.drop(['timestamp', 'Soil Moisture'], axis=1)
    y_nutrient = [1 if moisture < 40 else 0 for moisture in processed_data['Soil Moisture']]
    X_train_nutrient, X_test_nutrient, y_train_nutrient, y_test_nutrient = train_test_split(X_nutrient, y_nutrient, test_size=0.2, random_state=42)
    
    # Train nutrient deficiency prediction model
    nutrient_model = train_nutrient_model(X_train_nutrient, y_train_nutrient)    
    # Predict nutrient deficiency
    nutrient_predictions = predict_nutrient_deficiency(nutrient_model, X_nutrient)    
    # Generate recommendations
    recommendations = generate_recommendations(processed_data, nutrient_predictions)
    
    return recommendations

# Run the analysis and generate recommendations
recommendations = run_analysis()
if recommendations:
    for idx, recommendation in enumerate(recommendations):
        print(f"Recommendation {idx+1}:\n{recommendation}")
        while True:
            recommendations = run_analysis()
            if recommendations:
                for idx, recommendation in enumerate(recommendations):
                    print(f"Recommendation {idx+1}:\n{recommendation}")
            time.sleep(30)


 