from fastapi import FastAPI
from second import Developer,Project


app = FastAPI()

@app.post("/developers/")
def create_developer(develope: Developer):
    return{"message":"Developer created successfully", "developer":Developer}

@app.post("/projects/")
def create_project(project : Project):
    return{"message":"Project created successfully","project":project}

@app.post("/projects/")
def get_project(project:Project):
    sample_project = Project(
        title="Sample project",
        description="this is a description"
        languages="Python,JavaScript"
        lead_developer= Developer(name="John Doe" experience=5)
    )
    return("projects": sample_project)