# /* =========================================================
#    Examen: Predicción de Readmisión Diabética
#    Autor: Juan Antonio Ávalos García
#    Grupo: 9-C

#    ========================================================= */

from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import traceback
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Cargar modelo
try:
    model = joblib.load("diabetes_model.pkl")
    print("✅ Modelo cargado correctamente.")
except Exception as e:
    print("❌ Error al cargar el modelo:", e)
    model = None

# Características esperadas
feature_info = {
    "numeric_features": [
        'admission_type_id', 'discharge_disposition_id', 'admission_source_id',
        'time_in_hospital', 'num_lab_procedures', 'num_procedures',
        'num_medications', 'number_outpatient', 'number_emergency',
        'number_inpatient', 'number_diagnoses'
    ],
    "categorical_features": [
        'race', 'gender', 'age', 'diag_1', 'diag_2', 'diag_3', 'max_glu_serum',
        'A1Cresult', 'metformin', 'repaglinide', 'nateglinide', 'chlorpropamide',
        'glimepiride', 'acetohexamide', 'glipizide', 'glyburide', 'tolbutamide',
        'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol', 'troglitazone',
        'tolazamide', 'examide', 'citoglipton', 'insulin', 'glyburide-metformin',
        'glipizide-metformin', 'glimepiride-pioglitazone', 'metformin-rosiglitazone',
        'metformin-pioglitazone', 'change', 'diabetesMed'
    ]
}
all_features = feature_info["numeric_features"] + feature_info["categorical_features"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        print("📤 Datos recibidos:", data)

        if model is None:
            return jsonify({"error": "Modelo no cargado correctamente"}), 500

        input_df = pd.DataFrame([data])
        for col in all_features:
            if col not in input_df.columns:
                input_df[col] = 0 if col in feature_info["numeric_features"] else "None"

        input_df = input_df[all_features]
        prediction = model.predict(input_df)[0]
        probability = float(model.predict_proba(input_df)[0][1]) if hasattr(model, "predict_proba") else None

        result = {
            "prediction": int(prediction),
            "probability": round(probability * 100, 2) if probability is not None else None
        }

        print("✅ Resultado:", result)
        return jsonify(result)
    except Exception as e:
        print("❌ Error en backend:\n", traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
