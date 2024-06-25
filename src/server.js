import express from "express";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.join(path.dirname(__filename), "/");
const publicPath = path.join(__dirname, "../public/");
const portNumber = process.env.PORT || 8537;

const app = express();

app.use(express.static(publicPath));

app.get("*", (req, res) => {
  res.sendFile(path.resolve(`${publicPath}`, "index.html"));
});

app.listen(portNumber, () => {
  console.log(`App started on port http://localhost:${portNumber}...`);
});
