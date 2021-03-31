from aiohttp import hdrs

from tic_tac_toe import views

routes = [
    (hdrs.METH_POST, '/api/v1/tic-tac-toe/', views.GameView),
    (hdrs.METH_PATCH, '/api/v1/tic-tac-toe/{id:\d+}/', views.GameView),
    (hdrs.METH_GET, '/api/v1/tic-tac-toe/{id:\d+}/stats/', views.GameLogView),
]
