import inject
from aiohttp import web

from application import Application


@inject.params(app=Application)
async def get_diff(request, app):
    data = await app.get_currency_difference()
    if not data:
        return web.json_response(data='Temporary unavailable')
    return web.json_response(data=data)
