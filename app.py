"""Local System One UI. Run with .venv/bin/python app.py."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import httpx
import ollama
from pydantic import ValidationError


def build_request(data):
    if not isinstance(data, dict):
        raise ValueError('Expected a JSON object.')
    for field in ('model', 'state', 'instructions'):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f'{field.capitalize()} is required.')
    kind = data.get('type')
    criteria = data.get('criteria')
    if kind == 'choice':
        if not isinstance(criteria, list) or not criteria:
            raise ValueError('Add at least one choice.')
        choices = {}
        for row in criteria:
            if not isinstance(row, dict) or not isinstance(row.get('key'), str) or not row['key'].strip():
                raise ValueError('Every choice needs a name.')
            key = row['key'].strip()
            if key in choices:
                raise ValueError('Choice names must be unique.')
            description = row.get('description', '')
            if not isinstance(description, str):
                raise ValueError('Choice descriptions must be text.')
            choices[key] = description.strip() or None
        criteria = choices
    elif kind == 'score':
        if not isinstance(criteria, list) or not criteria or any(not isinstance(x, str) or not x.strip() for x in criteria):
            raise ValueError('Add nonempty score descriptions, lowest to highest.')
        criteria = [x.strip() for x in criteria]
    elif kind == 'noul':
        if criteria is not None:
            if not isinstance(criteria, dict) or set(criteria) != {'true', 'false'} or any(not isinstance(x, str) or not x.strip() for x in criteria.values()):
                raise ValueError('Provide both true and false descriptions, or leave both empty.')
    else:
        raise ValueError('Choose noul, choice, or score.')
    question = {'type': kind, 'instructions': data['instructions'].strip()}
    if criteria is not None:
        question['criteria'] = criteria
    return dict(model=data['model'].strip(), state=data['state'].strip(), questions={'output_response': question})


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path not in ('/', '/index.html'):
            self.send_error(404)
            return
        body = Path(__file__).with_name('index.html').read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != '/api/generate':
            self.send_error(404)
            return
        origin = self.headers.get('Origin')
        if origin and origin != f'http://{self.headers.get("Host")}':
            self.send_json(403, {'error': 'Cross-origin requests are not allowed.'})
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 1_000_000:
                raise ValueError('Request must be between 1 byte and 1 MB.')
            request = build_request(json.loads(self.rfile.read(length)))
        except (ValueError, UnicodeError) as exc:
            self.send_json(400, {'error': str(exc)})
            return
        try:
            with ollama.Client(timeout=120) as client:
                response = client.systemone(**request)
            self.send_json(200, response.model_dump(mode='json'))
        except ollama.ResponseError as exc:
            self.send_json(502, {'error': str(exc)})
        except (ConnectionError, httpx.HTTPError) as exc:
            self.send_json(502, {'error': f'Could not complete the Ollama request. Check that Ollama is running and OLLAMA_HOST is correct. {exc}'})
        except (ValidationError, AttributeError) as exc:
            self.send_json(502, {'error': f'The installed Ollama client/server must support System One. {exc}'})
        except Exception:
            self.send_json(500, {'error': 'Unexpected server error. See the Python terminal for details.'})
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8000'))
    print(f'System One UI: http://127.0.0.1:{port}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', port), Handler).serve_forever()
