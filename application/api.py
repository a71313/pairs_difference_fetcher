import inject
from aiohttp import web

from application import Application

@inject.params(app=Application)
async def get_diff(request, app):
    data = await app.get_currency_difference()
    return web.json_response(data=data)
