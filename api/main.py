from contextlib import asynccontextmanager
from typing import Sequence
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import numpy as np
from fastapi import Depends, FastAPI, Form, Request
import json
from fastapi.templating import Jinja2Templates

class Data:
  def __init__(
    self,
    Mkt_RF: float = Form(ge=-34.88, le=22.72),
    SMB: float = Form(ge=-22.30, le=12.16),
    HML: float = Form(ge=-10.06, le=13.46),
    RMW: float = Form(ge=-5.94, le=9.14),
    CMA: float = Form(ge=-10.62, le=4.96),
    RF: float = Form(ge=0.00, le=0.12)
    ):

    self.Mkt_RF = Mkt_RF
    self.SMB = SMB
    self.HML = HML
    self.RMW = RMW
    self.CMA = CMA
    self.RF = RF

model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
  with open("../notebooks/fama_french_parameters.json") as file:
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

@api.get("/")
async def main(request: Request):
  return templates.TemplateResponse(request = request, name = "index.html")

@api.post("/", response_class = HTMLResponse)
async def prediction(request: Request, data: Data = Depends()):
  x: np.ndarray = np.array([data.Mkt_RF, data.SMB, data.HML, data.RMW, data.CMA, data.RF])
  y: np.ndarray = (x @ model["M"]) + model["C"]

  return templates.TemplateResponse(
    request = request,
    name = "index.html",
    context = {
      "results": y.item(),
      "errors": {},
      "form": {},
    }
  )