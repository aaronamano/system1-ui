# System One playground

Local HTML UI backed by the Ollama Python library. No frontend build or web framework needed.

## Run

```sh
.venv/bin/python app.py
```

Open http://127.0.0.1:8000. Set `PORT` to change the UI port, or `OLLAMA_HOST` to change the Ollama server.

Your installed Ollama client and server must support `systemone` / `/v1/systemone`, and the model must be available. The existing virtual environment includes a client with this API. Retain your System One-enabled client; a package without `systemone` will not work.

## Use

Enter the model (defaults to `nimble`), context/state, and question/instructions.

- **noul:** probability of true. Optionally provide both true and false descriptions.
- **choice:** add/remove named choices with optional descriptions. Names must be unique.
- **score:** add/remove descriptions ordered lowest to highest. Scores are zero-based and may be fractional.

Click **Generate response**. The page displays the answer, available probabilities/confidence, and full response JSON. Errors appear in the response panel. Ollama requests use a 120-second timeout.

This server binds to localhost for local use. It calls the Python library directly; no shell command is executed.

## Checks

```sh
.venv/bin/python -m unittest -v
```
