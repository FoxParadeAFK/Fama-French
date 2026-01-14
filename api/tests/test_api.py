from typing import Any
import httpx
import pytest
from fastapi.testclient import TestClient

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from main import api

@pytest.fixture(scope = "module")
def lifespan():
  with TestClient(api) as client:
    yield client


@pytest.mark.parametrize("mkt_rf, smb, hml, rmw, cma, rf", [
  (-34.88, 0, 0, 0, 0, 0), # (b, v, v, v, v, v)
  (22.72, 0, 0, 0, 0, 0), # (b, v, v, v, v, v)
  (-34.88, -22.30, 0, 0, 0, 0), # (b, b, v, v, v, v)
  (22.72, 12.16, 0, 0, 0, 0), # (b, b, v, v, v, v)
  (-34.88, -22.30, -10.06, 0, 0, 0), # (b, b, b, v, v, v)
  (22.72, 12.16, 13.46, 0, 0, 0), # (b, b, b, v, v, v)
  (-34.88, -22.30, -10.06, -5.94, 0, 0), # (b, b, b, b, v, v)
  (22.72, 12.16, 13.46, 9.14, 0, 0), # (b, b, b, b, v, v)
  (-34.88, -22.30, -10.06, -5.94, -10.62, 0), # (b, b, b, b, b, v)
  (22.72, 12.16, 13.46, 9.14, 4.96, 0), # (b, b, b, b, b, v)
  (-34.88, -22.30, -10.06, -5.94, -10.62, 0.00), # (b, b, b, b, b, b)
  (22.72, 12.16, 13.46, 9.14, 4.96, 0.12), # (b, b, b, b, b, b)
])
def test_valid_post(lifespan, mkt_rf: float, smb: float, hml: float, rmw: float, cma: float, rf: float):
  response: httpx.Response = lifespan.post("/predict", json = {
    "Mkt_RF": mkt_rf,
    "SMB": smb,
    "HML": hml,
    "RMW": rmw,
    "CMA": cma,
    "RF": rf
  })

  json: Any = response.json()

  assert response.status_code == 200
  assert "results" in json
  assert isinstance(json["results"], float)

@pytest.mark.parametrize("mkt_rf, smb, hml, rmw, cma, rf", [
  (-35.00, 0, 0, 0, 0, 0), # (i, v, v, v, v, v)
  (34.00, 0, 0, 0, 0, 0), # (i, v, v, v, v, v)
  (-104.88, -28.32, 0, 0, 0, 0), # (i, i, v, v, v, v)
  (122.72, 14.16, 0, 0, 0, 0), # (i, i, v, v, v, v)
  (-44.88, -26.30, -13.15, 0, 0, 0), # (i, i, i, v, v, v)
  (27.42, 15.51, 19.41, 0, 0, 0), # (i, i, i, v, v, v)
  (-37.88, -23.30, -12.53, -7.14, 0, 0), # (i, i, i, i, v, v)
  (28.57, 24.16, 18.24, 64.25, 0, 0), # (i, i, i, i, v, v)
  (-73.57, -57.35, -24.73, -14.60, -12.45, 0), # (i, i, i, i, i, v)
  (25.72, 15.27, 15.36, 11.65, 9.10, 0), # (i, i, i, i, i, v)
  (-84.46, -36.30, -13.15, -8.45, -11.23, -0.01), # (i, i, i, i, i, i)
  (25.57, 15.25, 19.25, 12.20, 42.13, 1.12), # (i, i, i, i, i, i)
])
def test_invalid_post(lifespan, mkt_rf: float, smb: float, hml: float, rmw: float, cma: float, rf: float):
  response: httpx.Response = lifespan.post("/predict", json = {
    "Mkt_RF": mkt_rf,
    "SMB": smb,
    "HML": hml,
    "RMW": rmw,
    "CMA": cma,
    "RF": rf
  })

  assert response.status_code == 422

  json: Any = response.json()
  assert len(json["errors"]) != 0