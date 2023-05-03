"""
webapi/app.py

Just a placeholder starting script.
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# aqui es on el codi s'engega
def app() -> None:
    """
    Placeholder for doing something
    """
    print("Loading app")


if __name__ == "__main__":
    print("Hello WebAPI")
