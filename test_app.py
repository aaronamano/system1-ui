import json
import unittest
from unittest.mock import MagicMock, patch

from app import Handler, build_request


class RequestTests(unittest.TestCase):
    def test_question_types(self):
        cases = [('noul', None, None), ('noul', {'true': 'Yes', 'false': 'No'}, {'true': 'Yes', 'false': 'No'}),
                 ('choice', [{'key': 'a', 'description': ''}], {'a': None}),
                 ('score', ['Low', 'High'], ['Low', 'High'])]
        for kind, criteria, expected in cases:
            with self.subTest(kind=kind, criteria=criteria):
                result = build_request(dict(model='nimble', state='Context', instructions='Question?', type=kind, criteria=criteria))
                question = result['questions']['output_response']
                self.assertEqual(question['type'], kind)
                self.assertEqual(question.get('criteria'), expected)

    def test_invalid_inputs(self):
        for kind, criteria in [('choice', []), ('choice', [{'key': 'a'}, {'key': ' a '}]), ('score', ['']), ('noul', {'true': 'yes', 'false': ''}), ('bad', None)]:
            with self.subTest(kind=kind):
                with self.assertRaises(ValueError):
                    build_request(dict(model='nimble', state='Context', instructions='Question?', type=kind, criteria=criteria))
        with self.assertRaises(ValueError):
            build_request({})


class EndpointTests(unittest.TestCase):
    def handler(self, payload):
        from io import BytesIO
        handler = Handler.__new__(Handler)
        body = json.dumps(payload).encode()
        handler.path = '/api/generate'
        handler.headers = {'Content-Length': str(len(body))}
        handler.rfile = BytesIO(body)
        handler.send_json = MagicMock()
        return handler

    def test_generation(self):
        response = {'model': 'nimble', 'answers': {'output_response': {'type': 'noul', 'noul': 0.8}}}
        handler = self.handler(dict(model='nimble', state='Context', instructions='True?', type='noul', criteria=None))
        with patch('app.ollama.Client') as client:
            instance = client.return_value.__enter__.return_value
            instance.systemone.return_value.model_dump.return_value = response
            handler.do_POST()
            handler.send_json.assert_called_once_with(200, response)
            instance.systemone.assert_called_once_with(model='nimble', state='Context', questions={'output_response': {'type': 'noul', 'instructions': 'True?'}})

    def test_invalid_request(self):
        handler = self.handler({})
        handler.do_POST()
        self.assertEqual(handler.send_json.call_args.args[0], 400)

    def test_connection_error(self):
        handler = self.handler(dict(model='nimble', state='Context', instructions='True?', type='noul', criteria=None))
        with patch('app.ollama.Client', side_effect=ConnectionError('Offline')):
            handler.do_POST()
        self.assertEqual(handler.send_json.call_args.args[0], 502)
        self.assertIn('Ollama', handler.send_json.call_args.args[1]['error'])


if __name__ == '__main__':
    unittest.main()
