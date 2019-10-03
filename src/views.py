from json import JSONDecodeError

import aiohttp
from aiohttp import web
from aiohttp.web_request import Request

from models import create_store_dump, get_store_dump


async def store_request(request):
    try:
        data = await request.json()
    except JSONDecodeError:
        return web.HTTPBadRequest()

    db = request.app.get('mongo')
    import_id, err = await create_store_dump(db, data)
    if err:
        return web.HTTPBadRequest(text=str(err))

    response = {
        "import_id": str(import_id)
    }
    return web.json_response(status=201, data=response)


async def repeat_request(request):
    import_id = request.match_info.get('import_id')

    db = request.app.get('mongo')
    data, err = await get_store_dump(db, import_id)
    if err:
        return web.HTTPBadRequest(text=str(err))

    response = {
        "data": data
    }
    return web.json_response(status=200, data=response)


async def proxy_request(request: Request):
    data = await request.read()
    get_data = request.rel_url.query

    async with aiohttp.ClientSession() as session:

        if "Upgrade" in request.headers:
            ws_c2p = web.WebSocketResponse()
            await ws_c2p.prepare(request)

            async with session.ws_connect(request.rel_url) as ws_p2s:
                async for msg in ws_c2p:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        if msg.data == 'close':
                            await ws_c2p.close()
                        else:
                            ws_p2s.send_str(msg.data)
                            data_p2s = await ws_p2s.receive_str()
                            ws_c2p.send_str(data_p2s)
            return ws_c2p
        else:
            async with session.request(request.method, request.rel_url, headers=request.headers, params=get_data, data=data) as resp:
                res = resp
                raw = await res.read()

    return web.Response(body=raw, status=res.status, headers=res.headers)
