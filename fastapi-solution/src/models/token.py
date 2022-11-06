from pydantic import BaseModel, constr


class TokenRequest(BaseModel):
    """access токен"""

    Authorization: constr(regex=r"(^Bearer\s[\w.\\w.\\w])")
