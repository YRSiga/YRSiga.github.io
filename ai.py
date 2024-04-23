from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd

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

# Train Nutrient Deficiency Prediction model using kNN
def train_nutrient_model(X_train, y_train, n_neighbors=5):
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(X_train, y_train)
    return model

# Function to predict nutrient deficiency
def predict_nutrient_deficiency(model, X_test):
    return model.predict(X_test)

# Generate user-friendly recommendations with parameter values
def generate_recommendations(df, nutrient_predictions):
    recommendations = []
    # Sort data by timestamp and select the latest 2 timestamps
    processed_data = df.sort_values(by='timestamp', ascending=False).head(2)
    for index, row in processed_data.iterrows():
        recommendation = f"Timestamp: {row['timestamp']}<br>"
        recommendation += f"Potassium (K): {row['K']}<br>"
        recommendation += f"Nitrogen (N): {row['N']}<br>"
        recommendation += f"Phosphorus (P): {row['P']}<br>"
        recommendation += f"Soil Moisture: {row['Soil Moisture']}<br>"
        recommendation += f"EC (Electrical Conductivity): {row['ec']}<br>"
        recommendation += f"Humidity: {row['humidity']}<br>"
        recommendation += f"pH: {row['ph']}<br>"

        # Nutrient deficiency evaluation
        if nutrient_predictions[index] == 1:
            recommendation += "Your soil might need nutrients. Consider fertilizing your plants.<br>"
        else:
            recommendation += "Your soil nutrient levels seem adequate.<br>"
        
        # Moisture level recommendations
        if row['Soil Moisture'] < 40:
            recommendation += "Your soil is dry. Consider watering your plants.<br>"
        elif row['Soil Moisture'] > 60:
            recommendation += "Your soil is moist. Avoid overwatering.<br>"
        else:
            recommendation += "Your soil moisture levels seem balanced.<br>"

        # Crop suggestions based on N , P and K.
        if row['N'] < 200 or row['N'] > 250 and row['P'] < 50 or row['P'] > 100 and row['K'] < 150 or row['K'] > 200:
            recommendation += "--Suggested crops for given soil : <br>"
            recommendation += "-Red Gram (Pigeon Pea),Maize (Corn),Potato,Tomato,Carrot,Cabbage, due to suitable soil and high moisture.<br>"

        elif row['N'] < 150 or row['N'] > 200 and row['P'] < 40 or row['P'] > 80 and row['K'] < 100 or row['K'] > 150:
            recommendation += "--Suggested crops for given soil : <br>"
            recommendation += "-Cotton,Soybean,Groundnut (Peanut),Sorghum,Chickpea (Garbanzo Bean),Sunflower,Sugarcane, due to suitable soil and moderate moisture.<br>"
        else:
            recommendation += "--Suggested crops for given soil : <br>"
            recommendation += "-Wheat or Sorghum, which fit well with current soil conditions.<br>"






        # Fertilizer suggestions based on NPK values
        recommendation += "Fertilizer Suggestions:<br>"
        if (row['N'] < 200 or row['N'] > 250) or (row['P'] < 50 or row['P'] > 100) or (row['K'] < 150 or row['K'] > 200):
            recommendation += "-- Based on NPK values, Fertilizer suggestions are:<br>"
            recommendation += "- Add nitrogen-rich fertilizers like Urea, Diammonium Phosphate (DAP), or Ammonium Sulphate.<br>"
            recommendation += "- Boost phosphorus levels with Single Super Phosphate (SSP), Rock Phosphate, or Bone Meal.<br>"
            recommendation += "- Increase potassium with Muriate of Potash (MOP), Sulphate of Potash (SOP), or Potassium Magnesium Sulfate.<br>"
        elif (150 <= row['N'] <= 200) and (40 <= row['P'] <= 80) and (100 <= row['K'] <= 150):
            recommendation += "-- Based on NPK values, Fertilizer suggestions are:<br>"
            recommendation += "- Use balanced fertilizers like 15-15-15 or 10-20-10 to maintain optimal nutrient levels.<br>"
            recommendation += "- Additionally, consider applying micronutrient fertilizers such as zinc sulfate or boron to ensure comprehensive soil nutrition.<br>"
        elif (100 <= row['N'] <= 150) and (30 <= row['P'] <= 60) and (80 <= row['K'] <= 120):
            recommendation += "-- Based on NPK values, Fertilizer suggestions are:<br>"
            recommendation += "- Apply organic fertilizers like compost, manure, or biochar to improve soil structure and fertility.<br>"
            recommendation += "- Use slow-release fertilizers to provide nutrients gradually over time and reduce nutrient leaching.<br>"
        elif (50 <= row['N'] <= 100) and (20 <= row['P'] <= 50) and (50 <= row['K'] <= 100):
            recommendation += "-- Based on NPK values, Fertilizer suggestions are:<br>"
            recommendation += "- Utilize green manure crops to fix nitrogen and improve soil organic matter content.<br>"
            recommendation += "- Apply phosphorus-rich organic fertilizers such as bone meal or fish emulsion to boost root development.<br>"
        elif (20 <= row['N'] <= 50) and (10 <= row['P'] <= 30) and (30 <= row['K'] <= 70):
            recommendation += "-- Based on NPK values, Fertilizer suggestions are:<br>"
            recommendation += "- Implement crop rotation to naturally replenish soil nutrients and break pest cycles.<br>"
            recommendation += "- Use mulching techniques to conserve soil moisture and suppress weed growth.<br>"
        else:
            recommendation += "-- Based on NPK values, Fertilizer suggestions are:<br>"
            recommendation += "- No specific fertilizer recommendation needed based on current NPK levels.<br><br>"

        recommendations.append(recommendation)
    return recommendations
    
# Main function to run the analysis and generate recommendations
def run_analysis():
    data = fetch_data()
    processed_data = preprocess_data(data)
    
    if len(processed_data) < 5:
        print("Insufficient recent data available for analysis. Unable to generate recommendations.")
        return
    
    X_nutrient = processed_data.drop(['timestamp', 'Soil Moisture'], axis=1)
    y_nutrient = [1 if moisture < 40 else 0 for moisture in processed_data['Soil Moisture']]
    X_train_nutrient, X_test_nutrient, y_train_nutrient, y_test_nutrient = train_test_split(X_nutrient, y_nutrient, test_size=0.2, random_state=42)
    
    nutrient_model = train_nutrient_model(X_train_nutrient, y_train_nutrient, n_neighbors=3)    
    nutrient_predictions = predict_nutrient_deficiency(nutrient_model, X_nutrient)    
    recommendations = generate_recommendations(processed_data, nutrient_predictions)
    
    return recommendations
recommendations = run_analysis()
if recommendations:
    for idx, recommendation in enumerate(recommendations):
        print(f"Recommendation {idx+1}:<br>")
        print(recommendation.replace('\n', '<br>'))
