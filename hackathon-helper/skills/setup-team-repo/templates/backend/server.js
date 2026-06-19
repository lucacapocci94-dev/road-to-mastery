import express from "express";
import cors from "cors";
import Anthropic from "@anthropic-ai/sdk";

const app = express();
app.use(cors());
app.use(express.json());

// Legge la chiave da ANTHROPIC_API_KEY (vedi .env)
const client = new Anthropic();

// Scheletro che cammina: controllo di salute
app.get("/api/health", (req, res) => res.json({ ok: true }));

// Endpoint che parla con Claude
app.post("/api/ask", async (req, res) => {
  try {
    const prompt = (req.body && req.body.prompt) || "Ciao!";
    const response = await client.messages.create({
      // Default potente. Per piu velocita/meno costo: "claude-haiku-4-5".
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [{ role: "user", content: prompt }],
    });
    const block = response.content.find((b) => b.type === "text");
    res.json({ text: block ? block.text : "" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: String(err) });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Backend acceso su http://localhost:${PORT}`);
});
