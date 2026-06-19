// Indirizzo del backend (in locale)
const BACKEND = "http://localhost:3001";

document.getElementById("send").addEventListener("click", async () => {
  const out = document.getElementById("out");
  const prompt = document.getElementById("prompt").value;
  out.textContent = "...sto pensando...";
  try {
    const r = await fetch(`${BACKEND}/api/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
    const data = await r.json();
    out.textContent = data.text || data.error || "(nessuna risposta)";
  } catch (e) {
    out.textContent =
      "Errore: " + e + "\n(Il backend e acceso? Fai 'npm start' nella cartella backend.)";
  }
});
