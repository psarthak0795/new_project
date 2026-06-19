from fastapi import FastAPI

from app.routers import authh, login, manager, project, refresh, user

from app.database.connection import engine, Base


app = FastAPI()



Base.metadata.create_all(bind=engine)

app.include_router(authh.router)
app.include_router(login.router)
app.include_router(refresh.router)
app.include_router(user.router)
app.include_router(project.router)
app.include_router(manager.router)


