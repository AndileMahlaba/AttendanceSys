from api.app import create_app

app = create_app()
with app.app_context():
    print("JWT Secret Key:", app.config.get('JWT_SECRET_KEY'))
    print("JWT Algorithm:", app.config.get('JWT_ALGORITHM', 'HS256'))
    print("JWT Access Token Expires:", app.config.get('JWT_ACCESS_TOKEN_EXPIRES'))
