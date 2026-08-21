from fastapi import FastAPI     

app = FastAPI(
    title="Carona API", 
    version= "0.1.0",
    description="API for Carona carpooling service",
    summary="This API allows users to create and manage carpooling rides, view available rides, and join existing rides."
)

