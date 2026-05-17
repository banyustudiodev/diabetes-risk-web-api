const form = document.getElementById("predictionForm");

form.addEventListener("submit", async function (event) {
  event.preventDefault();

  const data = {
    Pregnancies: Number(document.getElementById("Pregnancies").value),
    Glucose: Number(document.getElementById("Glucose").value),
    BloodPressure: Number(document.getElementById("BloodPressure").value),
    SkinThickness: Number(document.getElementById("SkinThickness").value),
    Insulin: Number(document.getElementById("Insulin").value),
    BMI: Number(document.getElementById("BMI").value),
    DiabetesPedigreeFunction: Number(document.getElementById("DiabetesPedigreeFunction").value),
    Age: Number(document.getElementById("Age").value)
  };

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    const resultBox = document.getElementById("resultBox");
    const resultText = document.getElementById("resultText");
    const probabilityText = document.getElementById("probabilityText");
    const riskLevelText = document.getElementById("riskLevelText");

    if (result.status === "success") {
      resultBox.classList.remove("hidden");
      resultText.innerText = "Hasil: " + result.result;
      probabilityText.innerText = "Probabilitas Risiko: " + (result.probability * 100).toFixed(2) + "%";
      riskLevelText.innerText = "Tingkat Risiko: " + result.risk_level;
    } else {
      resultBox.classList.remove("hidden");
      resultText.innerText = "Terjadi kesalahan: " + result.message;
      probabilityText.innerText = "";
      riskLevelText.innerText = "";
    }

  } catch (error) {
    const resultBox = document.getElementById("resultBox");
    const resultText = document.getElementById("resultText");
    const probabilityText = document.getElementById("probabilityText");
    const riskLevelText = document.getElementById("riskLevelText");

    resultBox.classList.remove("hidden");
    resultText.innerText = "API belum berjalan atau tidak dapat diakses.";
    probabilityText.innerText = "";
    riskLevelText.innerText = "";
  }
});