from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from authRouter import router as auth_router
from projectsRouter import router as project_router
from database import create_db_and_tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Main Routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(project_router, prefix="/projects", tags=["Projects"])
