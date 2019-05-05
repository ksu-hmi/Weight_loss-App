#!/bin/bash

. ./venv/bin/activate
export PYTHONPATH=app/database
python -i -c "import database; db=database.DatabaseContext()"
