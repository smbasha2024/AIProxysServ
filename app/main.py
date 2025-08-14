from fastapi import FastAPI
from app.routers import customer_router, user_router, demo_router, email_router
from app.configs import migration

app = FastAPI(
    title = "AIProxys Server",
    description = "AIProxys API Servrer. Follows CLEAN architecture principles.",
    version = "1.0.0"
)
app.include_router(user_router.userRoutes)
app.include_router(customer_router.customerRoutes)
app.include_router(demo_router.demoRoutes)
app.include_router(email_router.emailRoutes)

@app.get("/")
def root():
    return {"message": f"Welcome to {app.title} {app.version}. It's an {app.description}"}

# ----------------- Create Database and Tables if not exists --------------
migration.migrate()