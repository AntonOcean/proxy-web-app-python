from views import store_request, repeat_request


def setup_routes(app):
    app.router.add_post('/store', store_request, name='store_request')
    app.router.add_get('/repeat', repeat_request, name='repeat_request')
