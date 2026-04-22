from fastapi import FastAPI
from database import create_tables
from routers import mentee, mentor, mentorship, goal

app = FastAPI(
    title="Mentor-Mentee Growth Platform",
    description=(
        "Backend API for the Mentor-mentee Growth platform."
    ),
    version="1.0.0",
    docs_url="/docs" #Swagger api specification
)

#for table creation 
@app.on_event("startup")
def on_startup():
    create_tables()


# Routers
app.include_router(mentee.router)
app.include_router(mentor.router)
app.include_router(mentorship.router)
app.include_router(goal.router)

# Swagger spec with base url 
@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Application is running ...",
        "docs": "/docs"
    }

# Health endpoint to test the application running
@app.get("/health", tags=["Health"])
def health():
    return {"status": "Healthy"}
