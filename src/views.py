from json import JSONDecodeError

from aiohttp import web

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
