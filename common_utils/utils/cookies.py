from fastapi import Response

def set_tokens_in_cookie(response: Response,
                         tokens: dict):
    
    response.set_cookie(key="access_token",
                        value=tokens["access_token"],
                        httponly=True,
                        samesite="strict")
    
    response.set_cookie(key="refresh_token",
                        value=tokens["refresh_token"],
                        httponly=True,
                        samesite="strict")