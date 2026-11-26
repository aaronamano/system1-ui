# System One playground

Local HTML UI backed by the Ollama Python library. No frontend build or web framework needed.

## Demo

https://github.com/user-attachments/assets/d23abedf-b524-4c2b-96aa-98eedcdc3b51

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

Check one or more models under **Models**:

- `nimble:latest` (default)
- `laya:latest`
- `pplx-decider-flash:latest`
- `tev1:latest`

Enter your **Context / state** and **Question / instructions**, then select an **Output type**:

- **noul:** probability of true. Optionally provide both true and false descriptions.
- **choice:** add/remove named choices with optional descriptions. Names must be unique.
- **score:** add/remove descriptions ordered lowest to highest. Scores are zero-based and may be fractional.

Click **Generate responses** to run the same question and criteria on every selected model. Each model has its own panel showing its answer, available probabilities/confidence, elapsed time, and expandable response JSON. Panels update independently, so an error from one model does not hide other results. Ollama requests use a 120-second timeout.

Under **Show responses**, uncheck a model to hide its panel and check it again to restore the response without rerunning it. These visibility controls are separate from the models selected for generation. Generating again replaces the previous panels.

This server binds to localhost for local use. It calls the Python library directly; no shell command is executed.

## Checks

```sh
python3 -m unittest -v
```
