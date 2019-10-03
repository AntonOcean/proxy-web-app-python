from views import store_request, repeat_request, proxy_request


def setup_routes(app):
    app.router.add_get('/store', store_request, name='store_request')
    app.router.add_get('/repeat/{id}', repeat_request, name='repeat_request')


def setup_routes_proxy(app):
    app.router.add_route('*', '/{tail:.*}', proxy_request, name='proxy')
