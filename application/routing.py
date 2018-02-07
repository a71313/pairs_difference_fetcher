from aiohttp.web_urldispatcher import UrlDispatcher

from application.api import get_diff, index_view, get_diff_timeline

router = UrlDispatcher()

router.add_get('/', index_view, name='index')
router.add_get('/api/get_diff', get_diff, name='diff', allow_head=False)
router.add_get('/api/get_diff_timeline/{cur1}/{cur2}', get_diff_timeline, name='get_diff_timeline', allow_head=False)
