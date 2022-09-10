import jwt
from settings import PRIVATE_JWT_KEY as private_key


def get_auth_token(name):
    return jwt.encode({
                'name': name
            },
            private_key,
            algorithm="HS256"
        )


def check_token(token):
    try:
        result = jwt.decode(
            token, private_key, algorithms=["HS256"]
        )
        print(result)
    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        return True