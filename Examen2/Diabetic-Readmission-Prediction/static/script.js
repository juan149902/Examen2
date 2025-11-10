document.getElementById("predictionForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    time_in_hospital: Number(document.getElementById("time_in_hospital").value),
    num_medications: Number(document.getElementById("num_medications").value),
    number_diagnoses: Number(document.getElementById("number_diagnoses").value),
    insulin: document.getElementById("insulin").value,
    A1Cresult: document.getElementById("A1Cresult").value,
    age: document.getElementById("age").value,
  };

  const resultBox = document.getElementById("result");
  resultBox.classList.add("hidden");
  resultBox.innerHTML = `<div class='loading'>⌛ Analizando...</div>`;

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (response.ok) {
      const color = result.prediction === 1 ? "danger" : "success";
      resultBox.innerHTML = `
        <div class="fade-in result-card ${color}">
          <h2>${result.prediction === 1 ? "⚠️ Riesgo de Readmisión" : "✅ Sin Riesgo"}</h2>
          <p><strong>Probabilidad:</strong> ${result.probability}%</p>
        </div>
      `;
    } else {
      throw new Error(result.error || "Error en la respuesta del servidor");
    }
  } catch (error) {
    resultBox.innerHTML = `<div class="error fade-in">❌ ${error}</div>`;
  }

  resultBox.classList.remove("hidden");
});
