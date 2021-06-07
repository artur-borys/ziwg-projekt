from os import path
import aiohttp
from aiohttp.web_app import Application
from aiohttp.web_exceptions import HTTPBadRequest, HTTPNotFound
from numpy.lib import utils
from similarities import compare_text_with_corpus_cosine, compare_text_with_corpus_jaccard, compare_text_with_corpus_fasttext
from utils import get_available_corpuses, load_statements, translate_statement_dict
from aiohttp import web
import aiohttp_cors
import json
import argparse
import clarin

clarin.set_user('241323@student.pwr.edu.pl')

parser = argparse.ArgumentParser()
parser.add_argument('--port', '-p', type=int, help='Port nasłuchiwania', default=8080)
args = parser.parse_args()

routes = web.RouteTableDef()

app = web.Application()

def not_found_response():
  return HTTPNotFound(text=json.dumps({
      'error': 'NOT_FOUND'
    }), headers={
      'Content-Type': 'application/json'
    })

def bad_request_response(errors):
  body = json.dumps({
      'ok': False,
      'errors': errors
    })
  return HTTPBadRequest(text=body, headers={'Content-Type': 'application/json'})

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
  try:
    corpus_name = request.query['corpus_name']
    if corpus_name not in get_available_corpuses():
      return not_found_response()
    corpus = load_statements(f'./corpuses/{corpus_name}.tsv').reset_index(drop=True).fillna('')
    text = corpus.iloc[int(request.match_info['id'])]
    return web.json_response(translate_statement_dict(text))
  except IndexError:
    return not_found_response()
  except KeyError:
    return bad_request_response(['CORPUS_NAME_REQUIRED'])

@routes.get('/corpuses')
async def get_corpuses(request):
  corpuses = get_available_corpuses()
  return web.json_response({
    'data': corpuses
  })

@routes.post('/similarity')
async def post_similarity(request):
  payload = await request.json()
  errors = []

  try:
    text = payload['text']
    method = str(payload['method']).strip()
    corpus_variant = str(payload['corpus_variant']).strip()
    corpus_name = str(payload['corpus_name']).strip()
    if corpus_name not in get_available_corpuses():
      raise Exception('UNAVAILABLE_CORPUS')
    if corpus_variant == 'full':
      corpus = load_statements(path.join('./corpuses', f'{corpus_name}.tsv')).reset_index(drop=True).fillna('')
      display_corpus = corpus
    elif corpus_variant == 'base':
      corpus = load_statements(path.join('./corpuses', f'{corpus_name}_base.tsv')).reset_index(drop=True).fillna('')
      display_corpus = load_statements(path.join('./corpuses', f'{corpus_name}.tsv')).reset_index(drop=True).fillna('')
      text = clarin.get_base_words(text)
    else:
      errors.append('INVALID_CORPUS_VARIANT')
    
    if method not in ['bow', 'tfidf', 'jaccard', 'fastText']:
      errors.append('INVALID_METHOD')
  except KeyError as e:
    if e.args[0] == 'text':
      errors.append('INVALID_TEXT')
    elif e.args[0] == 'corpus_variant':
      errors.append('INVALID_CORPUS_VARIANT')
    elif e.args[0] == 'corpus_name':
      errors.append('INVALID_CORPUS_NAME')
    elif e.args[0] == 'method':
      errors.append('INVALID_METHOD')
    else:
      errors.append('UNKNOWN_ERROR')
  except Exception as e:
    if e.args[0] == 'UNAVAILABLE_CORPUS':
      errors.append(e.args[0])
    else:
      errors.append('UNKNOWN_ERROR')

  
  if len(errors) > 0:
    return bad_request_response(errors)

  if method == 'jaccard':
    results = compare_text_with_corpus_jaccard(text, corpus, display_corpus=display_corpus)
  elif method == 'bow':
    results = compare_text_with_corpus_cosine(text, corpus, 'count', display_corpus=display_corpus)
  elif method == 'tfidf':
    results = compare_text_with_corpus_cosine(text, corpus, 'tfidf', display_corpus=display_corpus)
  elif method == 'fastText':
    results = compare_text_with_corpus_fasttext(text, corpus, display_corpus=display_corpus)

  return web.json_response(results)

async def handle_404(request):
    return web.json_response({
      'ok': False,
      'errors': ['NOT_FOUND']
    },
    headers={'Access-Control-Allow-Origin': '*'}
    )


async def handle_500(request):
  return web.json_response({
    'ok': False,
    'errors': ['INTERNAL_ERROR']
  },
    headers={'Access-Control-Allow-Origin': '*'}
    )


def create_error_middleware(overrides):
  @web.middleware
  async def error_middleware(request, handler):
      try:
          return await handler(request)
      except web.HTTPException as ex:
          override = overrides.get(ex.status)
          if override:
              resp = await override(request)
              resp.set_status(ex.status)
              return resp

          raise
      except:
          resp = await overrides[500](request)
          resp.set_status(500)
          return resp

  return error_middleware


def setup_middlewares(app: Application):
  error_middleware = create_error_middleware({
    404: handle_404,
    500: handle_500
  })
  app.middlewares.append(error_middleware)

app.add_routes(routes)
# setup_middlewares(app)

cors = aiohttp_cors.setup(app, defaults={
  "*": aiohttp_cors.ResourceOptions(
    allow_headers="*"
  )
})

for route in list(app.router.routes()):
  cors.add(route)

web.run_app(app, port=args.port)
