import inject
from aiohttp import web

from application import Application


@inject.params(app=Application)
async def get_diff(request, app):
    data = await app.get_currency_difference()
    if not data:
        return web.json_response(data='Temporary unavailable')
    return web.json_response(data=data)


async def index_view(request):
    return web.FileResponse('./static/index.html')


@inject.params(app=Application)
async def get_diff_timeline(request, app):
    cur1 = request.match_info['cur1']
    cur2 = request.match_info['cur2']
    pair = f'{cur1}/{cur2}'
    return web.json_response(app.state[pair])
