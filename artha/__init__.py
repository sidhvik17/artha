"""Artha package init.

ADK's `adk web` discovers the agent via `from . import agent`. That import
requires google-adk; the security/tool unit tests in /tests deliberately do
NOT require it. Guarding the import lets `python -m unittest` verify the
pure-logic layers (detectors, tool contracts) even in a bare CI environment,
while full agent discovery works wherever google-adk is installed.
"""
try:
    from . import agent  # noqa: F401  (requires google-adk)
except ImportError:  # pragma: no cover — bare test environments only
    agent = None
