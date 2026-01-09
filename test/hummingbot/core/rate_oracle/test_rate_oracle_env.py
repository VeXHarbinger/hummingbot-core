def get_oracle_type(rate_oracle):
    return type(rate_oracle.source)

import os
import importlib
import pytest
from hummingbot.core.rate_oracle.rate_oracle import RateOracle, ALL_RATE_ORACLES, RATE_ORACLE_SOURCES

def clear_rate_oracle_singleton():
    # Helper to clear singleton between tests
    RateOracle._shared_instance = None

@pytest.mark.parametrize("oracle_name", ALL_RATE_ORACLES)
def test_env_var_selects_correct_rate_source(monkeypatch, oracle_name):
    """
    Test that setting MY_RATE_ORACLE to each valid oracle name selects the correct RateSource class.
    """
    monkeypatch.setenv("MY_RATE_ORACLE", oracle_name)
    clear_rate_oracle_singleton()
    importlib.reload(importlib.import_module("hummingbot.core.rate_oracle.rate_oracle"))
    rate_oracle = RateOracle()
    assert get_oracle_type(rate_oracle) == RATE_ORACLE_SOURCES[oracle_name]

def test_env_var_invalid_falls_back_to_binance(monkeypatch):
    """
    Test that setting MY_RATE_ORACLE to an invalid value falls back to BinanceRateSource.
    """
    monkeypatch.setenv("MY_RATE_ORACLE", "not_a_real_oracle")
    clear_rate_oracle_singleton()
    importlib.reload(importlib.import_module("hummingbot.core.rate_oracle.rate_oracle"))
    rate_oracle = RateOracle()
    from hummingbot.core.rate_oracle.sources.binance_rate_source import BinanceRateSource
    assert isinstance(rate_oracle.source, BinanceRateSource)

def test_env_var_empty_string_falls_back_to_binance(monkeypatch):
    """
    Test that setting MY_RATE_ORACLE to an empty string falls back to BinanceRateSource.
    """
    monkeypatch.setenv("MY_RATE_ORACLE", "")
    clear_rate_oracle_singleton()
    importlib.reload(importlib.import_module("hummingbot.core.rate_oracle.rate_oracle"))
    rate_oracle = RateOracle()
    from hummingbot.core.rate_oracle.sources.binance_rate_source import BinanceRateSource
    assert isinstance(rate_oracle.source, BinanceRateSource)

def test_env_var_missing_falls_back_to_binance(monkeypatch):
    """
    Test that when MY_RATE_ORACLE is not set, the default is BinanceRateSource.
    """
    monkeypatch.delenv("MY_RATE_ORACLE", raising=False)
    clear_rate_oracle_singleton()
    importlib.reload(importlib.import_module("hummingbot.core.rate_oracle.rate_oracle"))
    rate_oracle = RateOracle()
    from hummingbot.core.rate_oracle.sources.binance_rate_source import BinanceRateSource
    assert isinstance(rate_oracle.source, BinanceRateSource)
