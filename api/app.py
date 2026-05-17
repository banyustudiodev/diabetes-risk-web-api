from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

# Membuat aplikasi Flask
app = Flask(__name__)
CORS(app)

# Menentukan lokasi file model dan scaler
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "diabetes_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "..", "model", "scaler.pkl")

# Memuat model dan scaler
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

with open(SCALER_PATH, "rb") as file:
    scaler = pickle.load(file)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "API Prediksi Risiko Diabetes berjalan",
        "endpoint": "/predict",
        "method": "POST"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Mengambil data JSON dari request
        data = request.get_json()

        # Daftar field yang wajib dikirim dari aplikasi web
        required_fields = [
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeFunction",
            "Age"
        ]

        # Validasi apakah seluruh field tersedia
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"Field '{field}' wajib diisi"
                }), 400

        # Mengubah input JSON menjadi array numerik
        input_data = np.array([[
            float(data["Pregnancies"]),
            float(data["Glucose"]),
            float(data["BloodPressure"]),
            float(data["SkinThickness"]),
            float(data["Insulin"]),
            float(data["BMI"]),
            float(data["DiabetesPedigreeFunction"]),
            float(data["Age"])
        ]])

        # Melakukan scaling data sesuai scaler dari proses training
        input_scaled = scaler.transform(input_data)

        # Melakukan prediksi
        prediction = model.predict(input_scaled)[0]

        # Mengambil probabilitas kelas 1 atau risiko diabetes
        probability = model.predict_proba(input_scaled)[0][1]

        # Interpretasi hasil prediksi
        if prediction == 1:
            result = "Berisiko Diabetes"
        else:
            result = "Tidak Berisiko Diabetes"

        # Menentukan tingkat risiko berdasarkan probabilitas
        if probability >= 0.70:
            risk_level = "Tinggi"
        elif probability >= 0.40:
            risk_level = "Sedang"
        else:
            risk_level = "Rendah"

        # Mengirim response ke aplikasi web
        return jsonify({
            "status": "success",
            "prediction": int(prediction),
            "result": result,
            "probability": round(float(probability), 4),
            "risk_level": risk_level
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)