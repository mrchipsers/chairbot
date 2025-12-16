import math
import Utils

def test_sigmoid_zero():
    assert Utils.sigmoid(0) == 0.5

def test_sigmoid_minus_one():
    assert Utils.sigmoid(-1) == 1 / (1 + math.e)

def test_sigmoid_one():
    assert Utils.sigmoid(1) == math.e / (1 + math.e)

def test_remap_max_to_max():
    assert Utils.remap(1, 0, 1, -5, 15) == 15

def test_remap_min_to_min():
    assert Utils.remap(-3, -3, 2, 10, 100) == 10

def test_remap_equal_input():
    assert Utils.remap(5, 5, 5, -30, 15) == 5

def test_remap_equal_output():
    assert Utils.remap(-7, -67, 100, 0, 0) == 0

def test_remap_equal_input_output():
    assert Utils.remap(1, 1, 1, 0, 0) == 1

def test_remap_invert_input():
    assert Utils.remap(0, 1, -1, 0, 10) == 5

def test_remap_invert_output():
    assert Utils.remap(0, -1, 1, 10, 0) == 5

def test_remap_invert_input_output():
    assert Utils.remap(0, 1, -1, 10, 0) == 5