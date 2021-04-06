#!/bin/bash
set -x

flask db init;

flask db migrate -m "logistic_mesh_map table";

flask db upgrade;

flask run;
