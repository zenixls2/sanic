from sanic import Sanic
from sanic.exceptions import PayloadTooLarge
from sanic.response import text


def test_payload_too_large_from_error_handler():
    data_received_app = Sanic('data_received')
    data_received_app.config.REQUEST_MAX_SIZE = 1

    @data_received_app.route('/1')
    async def handler1(request):
        return text('OK')

    @data_received_app.exception(PayloadTooLarge)
    def handler_exception(request, exception):
        return text('Payload Too Large from error_handler.', 413)

    response = data_received_app.test_client.get('/1', gather_request=False)
    assert response.status == 413
    assert response.text == 'Payload Too Large from error_handler.'


def test_payload_too_large_at_data_received_default():
    data_received_default_app = Sanic('data_received_default')
    data_received_default_app.config.REQUEST_MAX_SIZE = 1

    @data_received_default_app.route('/1')
    async def handler2(request):
        return text('OK')

    response = data_received_default_app.test_client.get(
        '/1', gather_request=False)
    assert response.status == 413
    assert response.text == 'Error: Payload Too Large'


def test_payload_too_large_at_on_header_default():
    on_header_default_app = Sanic('on_header')
    on_header_default_app.config.REQUEST_MAX_SIZE = 500

    @on_header_default_app.post('/1')
    async def handler3(request):
        return text('OK')

    data = 'a' * 1000
    response = on_header_default_app.test_client.post(
        '/1', gather_request=False, data=data)
    assert response.status == 413
    assert response.text == 'Error: Payload Too Large'
