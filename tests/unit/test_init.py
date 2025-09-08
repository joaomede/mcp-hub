import pytest
import mcp_hub

def test_env_dict_parsing():
    env = ["FOO=bar", "BAZ=qux"]
    env_dict = {}
    for var in env:
        key, value = var.split("=", 1)
        env_dict[key] = value
    assert env_dict["FOO"] == "bar"
    assert env_dict["BAZ"] == "qux"
