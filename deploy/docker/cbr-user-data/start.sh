#!/bin/bash

uvicorn cbr_user_data.lambdas.handler:app --reload --host 0.0.0.0 --port 8080