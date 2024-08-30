import json
from aiohttp import web
import aiohttp

async def test(request):
    print(request.query)


async def controlApi(request):
    print(request.query)
    text = ''

    return web.Response(body=json.dumps({"text": text}), content_type='application/json')
