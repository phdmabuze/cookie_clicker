from ninja import NinjaAPI
from users.api import router as users_router
from tasks.api import router as tasks_router
from upgrades.api import router as upgrades_router
from authorization.api import router as authorization_router

api = NinjaAPI()
api.add_router("/users", users_router)
api.add_router("/tasks", tasks_router)
api.add_router("/upgrades", upgrades_router)
api.add_router("/auth", authorization_router)
