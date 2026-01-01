import numpy as np
from pandas import DataFrame
import pytest
from data import generator

@pytest.mark.data
@pytest.mark.parametrize("m, n", [
  # (invalid, boundary, valid) i, b, v
  (0, 1), # (b, b)
  (4, 1), # (v, b)
  (0, 2), # (b, v)
  (10, 3), # (v, v) 
  (200, 3), # (v, v)
])
def test_count_and_dimensions_valid(m: int, n: int): # generator requires parameters 'm' and 'n'. test data shape is within the parameters
  seed: int = 45 # arbitrary seed number
  spread: int = 60 # arbitrary spread number

  x, y, _ = generator(m = m, n = n, seed = seed, spread = spread)
  assert x.shape == (m , n)
  assert y.shape == (m ,)

@pytest.mark.data
@pytest.mark.parametrize("m, n", [
  # (invalid, boundary, valid) i, b, v
  (-1, 0), # (i, i)
  (-10, -1), # (i, i)
])
def test_count_and_dimensions_invalid(m: int, n: int): # failure if the number of samples is negative or if the dimensions are below 2d
  seed: int = 45 # arbitrary seed number
  spread: int = 60 # arbitrary spread number

  with pytest.raises(ValueError): 
    generator(m = m, n = n, seed = seed, spread = spread)

@pytest.mark.data
@pytest.mark.parametrize("seed", [
  100,
  200,
  250,
  275,
])
def test_seed_reproducibility(seed: int):
  m: int = 10 # arbitrary seed number
  n: int = 3 # arbitrary seed number
  spread: int = 60 # arbitrary spread number

  x_I, y_I, _ = generator(m = m, n = n, seed = seed, spread = spread)
  x_II, y_II, _ = generator(m = m, n = n, seed = seed, spread = spread)

  data_I: np.ndarray = np.column_stack((x_I, y_I))
  data_II: np.ndarray = np.column_stack((x_II, y_II))

  np.testing.assert_array_equal(data_I, data_II)
  np.testing.assert_array_equal(data_II, data_I)

@pytest.mark.data
@pytest.mark.parametrize("seed_I, seed_II", [
  (100, 200),
  (12, 34),
  (47, 98),
])
def test_seed_reproducibility_(seed_I: int, seed_II):
  m: int = 10 # arbitrary seed number
  n: int = 3 # arbitrary seed number
  spread: int = 60 # arbitrary spread number

  x_I, y_I, _ = generator(m = m, n = n, seed = seed_I, spread = spread)
  x_II, y_II, _ = generator(m = m, n = n, seed = seed_II, spread = spread)

  data_I: np.ndarray = np.column_stack((x_I, y_I))
  data_II: np.ndarray = np.column_stack((x_II, y_II))

  with pytest.raises(AssertionError):
    np.testing.assert_array_equal(data_I, data_II)