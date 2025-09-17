from ninja import NinjaAPI

from authorization.api import router as authorization_router
from tasks.api import router as tasks_router
from upgrades.api import router as upgrades_router
from users.api import router as users_router

api = NinjaAPI()
api.add_router("/v1/users", users_router)
api.add_router("/v1/user-tasks", tasks_router)
api.add_router("/v1/user-upgrades", upgrades_router)
api.add_router("/v1/auth", authorization_router)
