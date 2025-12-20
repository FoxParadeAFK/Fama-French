from contextlib import asynccontextmanager
from typing import Annotated
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import numpy as np
from fastapi import FastAPI, Form, Request
import json
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

class Data(BaseModel):
    Mkt_RF: float =  Field(..., ge = -34.88, le = 22.72)
    SMB: float = Field(..., ge=-22.30, le=12.16)
    HML: float = Field(..., ge=-10.06, le=13.46)
    RMW: float = Field(..., ge=-5.94, le=9.14)
    CMA: float = Field(..., ge=-10.62, le=4.96)
    RF: float = Field(..., ge=0.00, le=0.12)

model = {}

@asynccontextmanager
async def lifespan(api: FastAPI):
  with open("fama_french_parameters.json") as file:
    parameters: dict = json.load(file)

    model["M"] = np.array(parameters["M"])
    model["C"] = np.array(parameters["C"])
  yield

api: FastAPI = FastAPI(
  docs_url = None,
  redoc_url = None,
  openapi_url = None,
  lifespan = lifespan
)
api.mount("/static", StaticFiles(directory="static"), name="static")
templates: Jinja2Templates = Jinja2Templates(directory = "template")

@api.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, error: RequestValidationError):

  if request.url.path == "/predict":
    print(error)
    return JSONResponse(
      status_code = 422,
      content = {
        "errors": {error["loc"][1]: error["msg"] for error in error.errors()}
      }
    )

  forms: dict = dict(await request.form())
  errors: dict = {error["loc"][1]: error["msg"] for error in error.errors()}

  forms: dict = {key: value for key, value in forms.items() if key not in errors}

  return templates.TemplateResponse(
    request = request,
    name = "index.html",
    context = {
      "form": forms,
      "errors": errors
    }
  )

def fama_french(data: Data):
  x: np.ndarray = np.array([data.Mkt_RF, data.SMB, data.HML, data.RMW, data.CMA, data.RF])
  y: np.ndarray = (x @ model["M"]) + model["C"]
  return y.item()

@api.post("/predict")
async def prediction_json(data: Data):
  y: float = fama_french(data)
  return {"results": y}


@api.get("/")
async def main(request: Request):
  return templates.TemplateResponse(request = request, name = "index.html", 
                                    context = {
                                      "errors": {},
                                      "form": {},
                                    })

@api.post("/", response_class = HTMLResponse)
async def prediction(request: Request, data: Annotated[Data, Form()]):
  y: float = fama_french(data)

  return templates.TemplateResponse(
    request = request,
    name = "index.html",
    context = {
      "results": y,
      "errors": {},
      "form": {},
    }
  )