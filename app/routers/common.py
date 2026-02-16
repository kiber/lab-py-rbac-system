from .. import schemas

def error_responses(*status_codes: int) -> dict[int, dict]:
    return {
        status_code: {"model": schemas.ErrorResponse}
        for status_code in status_codes
    }
