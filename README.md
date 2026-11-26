# System One playground

Local HTML UI backed by the Ollama Python library. No frontend build or web framework needed.

## Set up virtual environment
```sh
python3 -m venv .venv
```
**Enter virtual environment** (For MacOS users)
```sh
source .venv/bin/activate
```

**Exit virtual environment**
```sh
deactivate
```

## Install ollama
*make sure you're in the virtual environment*
```sh
pip install ollama
```

## Run
*make sure you're in the virtual environment and that you already installed the ollama Python package shown under "Install ollama"*

```sh
python3 app.py
```

Open http://127.0.0.1:8000

Your installed Ollama client and server must support `systemone` / `/v1/systemone`, and the model must be available. The existing virtual environment includes a client with this API. Retain your System One-enabled client; a package without `systemone` will not work.

## Use

Select a model from the **Model** dropdown:

- `nimble:latest` (default)
- `laya:latest`
- `pplx-decider-flash:latest`
- `tev1:latest`

Enter your **Context / state** and **Question / instructions**, then select an **Output type**:

- **noul:** probability of true. Optionally provide both true and false descriptions.
- **choice:** add/remove named choices with optional descriptions. Names must be unique.
- **score:** add/remove descriptions ordered lowest to highest. Scores are zero-based and may be fractional.

Click **Generate response**. The page displays the answer, available probabilities/confidence, and full response JSON. Errors appear in the response panel. Ollama requests use a 120-second timeout.

This server binds to localhost for local use. It calls the Python library directly; no shell command is executed.

## Checks

```sh
python3 -m test_app -v
```
