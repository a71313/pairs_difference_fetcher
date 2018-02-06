from aiohttp.web_urldispatcher import UrlDispatcher

from application.api import get_diff

router = UrlDispatcher()

router.add_get("/api/get_diff", get_diff, name="diff", allow_head=False)
