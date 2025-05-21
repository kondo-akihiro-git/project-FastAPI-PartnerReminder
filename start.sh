#!/usr/bin/env bash
uvicorn api.routes.main:app --host 0.0.0.0 --port 10000