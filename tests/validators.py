from http import HTTPStatus


def validate_type(cls):
    class Inner(cls):

        def __eq__(self, value):
            return isinstance(value, cls)

    return Inner()


async def validate_error_msg(
        response,
        exp_error_msg: str,
        error_key: str = 'error',
        exp_status_code: int = HTTPStatus.BAD_REQUEST
) -> None:
    assert response.status == exp_status_code
    response_data = await response.json()
    assert response_data[error_key] == exp_error_msg
