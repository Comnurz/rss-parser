from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from models import models
from models.schemas import Token
from utils.database import engine
from api.router import api_router
from utils.database import get_db
from helpers.authenticator import authenticate_user, create_access_token
from helpers.security import ACCESS_TOKEN_EXPIRE_MINUTES

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Get Token via email and password

    :param form_data: OAuth2PasswordRequestForm
    :param db: Session
    :return: Token
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
async def root():
    """
    Welcome to route.

    :return: Dict[str, str]
    """
    return {"message": "Hello World!!"}


@app.get("/ready", summary="k8s Ready")
def ready() -> Response:
    """
    API for internal kubernetes.

    :return: Response
    """
    return Response(status_code=status.HTTP_200_OK, content="Success")


@app.get("/healthz", summary="k8s Healthz")
def healthz() -> Response:
    """
    API for internal kubernetes.

    :return: Response
    """
    return Response(status_code=status.HTTP_200_OK, content="Success")


# import uvicorn

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8888)
