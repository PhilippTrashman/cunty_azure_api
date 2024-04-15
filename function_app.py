import azure.functions as func
import datetime
import json
import logging

import sys
import os

app = func.FunctionApp()
backend = None

TOKEN = os.environ["TOKEN"]
print(f"TOKEN: {TOKEN}")

@app.route('hello', methods=['GET'], auth_level=func.AuthLevel.ANONYMOUS)
def get_hello_world(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(f"Hello World")
