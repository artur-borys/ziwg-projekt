from aiohttp.web_exceptions import HTTPBadRequest
from similarities import compare_text_with_corpus_cosine, compare_text_with_corpus_jaccard
from utils import load_statements, translate_statement_dict
from aiohttp import web
import aiohttp_cors
import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--port', '-p', type=int, help='Port nasłuchiwania', default=8080)

args = parser.parse_args()

routes = web.RouteTableDef()

statements = load_statements('./wypowiedzi.tsv').reset_index(drop=True)
statements_base = load_statements('./wypowiedzi_base.tsv').reset_index(drop=True)

@routes.get('/')
async def status(request):
  description = [
    {
      'method': route.method,
      'path': route.path
    }
    for route in routes
  ]
  data = {
    'status': 'ok',
    'endpoints': description
  }

  return web.json_response(data)

@routes.get('/text/{id}')
async def get_text(request):
  statement = statements.iloc[int(request.match_info['id'])]
  return web.json_response(translate_statement_dict(statement))

@routes.post('/similarity/')
async def post_similarity(request):
  payload = await request.json()
  errors = []

  try:
    payload['text']
    method = str(payload['method']).strip()
    corpus_variant = str(payload['corpus_variant']).strip()
    if corpus_variant == 'full':
      corpus = statements
    elif corpus_variant == 'base':
      corpus = statements_base
    else:
      errors.append('INVALID_CORPUS_VARIANT')
    
    if method not in ['bow', 'tfidf', 'jaccard']:
      errors.append('INVALID_METHOD')
  except KeyError as e:
    if e.args[0] == 'text':
      errors.append('INVALID_TEXT')
    elif e.args[0] == 'corpus_variant':
      errors.append('INVALID_CORPUS_VARIANT')
    elif e.args[0] == 'method':
      errors.append('INVALID_METHOD')
    else:
      errors.append('UNKNOWN_ERROR')

  
  if len(errors) > 0:
    body = json.dumps({
      'ok': False,
      'errors': errors
    })
    raise HTTPBadRequest(text=body, headers={'Content-Type': 'application/json'})

  if method == 'jaccard':
    results = compare_text_with_corpus_jaccard(payload['text'], corpus, display_corpus=statements)
  elif method == 'bow':
    results = compare_text_with_corpus_cosine(payload['text'], corpus, 'count', display_corpus=statements)
  elif method == 'tfidf':
    results = compare_text_with_corpus_cosine(payload['text'], corpus, 'tfidf', display_corpus=statements)

  return web.json_response(results)

app = web.Application()

app.add_routes(routes)

cors = aiohttp_cors.setup(app, defaults={
  "*": aiohttp_cors.ResourceOptions(
    allow_headers="*"
  )
})

for route in list(app.router.routes()):
  cors.add(route)

web.run_app(app, port=args.port)