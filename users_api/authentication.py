from rest_framework_simplejwt.authentication import JWTAuthentication


class BearerJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that adds 'Bearer ' prefix to the token
    for proper Swagger documentation.
    """

    def authenticate_header(self, request):
        return "Bearer"

    def get_header(self, request):
        header = super().get_header(request)
        if header and not header.startswith(b"Bearer "):
            # If the header doesn't start with 'Bearer ', add it
            if isinstance(header, bytes):
                return b"Bearer " + header
            return "Bearer " + header
        return header
