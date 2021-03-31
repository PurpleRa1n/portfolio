from aiohttp import hdrs

from auth import views

routes = [
    (hdrs.METH_POST, '/api/v1/auth/login/', views.LoginView),
    (hdrs.METH_POST, '/api/v1/auth/registration/', views.RegistrationView),
]
