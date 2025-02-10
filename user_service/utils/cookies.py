from fastapi import Response

def set_token_in_cookie(responce: Response,
                         token: str):
    
    responce.set_cookie(key="access_token",
                        value=token,
                        httponly=True)