from animit.kit.email import EmailStrDNS
from animit.kit.schemas import Schema


class LoginCodeRequest(Schema):
    email: EmailStrDNS


class AuthenticateRequest(Schema):
    email: EmailStrDNS
    code: str
