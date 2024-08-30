import json
from aiohttp import web
import aiohttp_cors
import controller

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(body=json.dumps({"text": text}), content_type='application/json')

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/controlApi', controller.controlApi),
                web.get('/t', controller.test),
                web.get('/{name}', handle)])

if __name__ == '__main__':
  cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
  for route in list(app.router.routes()):
        try:
            cors.add(route)
        except ValueError:
            pass
  web.run_app(app, port=1134)