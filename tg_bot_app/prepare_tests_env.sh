#!/bin/bash
python3.10 -m venv venv_tests
source venv_tests/bin/activate && pip install -r tests/requirements_tests.txt && pip install -r requirements.txt
