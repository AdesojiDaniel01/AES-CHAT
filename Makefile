# Common venv names. 
VENVS := .venv venv env .env .python-venv

# Check for Windows or Unix. 
PY_WIN := $(firstword $(wildcard $(addsuffix /Scripts/python.exe,$(VENVS))))

PY_UNIX := $(firstword $(wildcard $(addsuffix /bin/python,$(VENVS))))



ifdef VIRTUAL_ENV
  PYTHON := $(VIRTUAL_ENV)/Scripts/python.exe
else ifneq ($(PY_WIN),)
  PYTHON := $(PY_WIN)
else ifneq ($(PY_UNIX),)
  PYTHON := $(PY_UNIX)
else
  PYTHON := python
endif



server:
	$(PYTHON) app/server.py

client:
	$(PYTHON) app/client.py

tests:
	$(PYTHON) -m pytest tests