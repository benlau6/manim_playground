import pandas as pd


def test_pandas():
    data = {"a": [1, 2, 3], "b": ["apple", "orange", "banana"]}
    df = pd.DataFrame(data)
    assert isinstance(df, pd.DataFrame)


def test_pandas2():
    data = {"a": [1, 2, 3], "b": ["apple", "orange", "banana"]}
    df = pd.DataFrame(data)
    assert isinstance(df, pd.DataFrame)
