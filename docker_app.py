import json
from pydantic import parse_obj_as
from typing import Union

### Now create the Middleware and load the models

from aas2openapi.middleware.middleware import Middleware

middleware = Middleware()
middleware.generate_model_registry_api()

app = middleware.app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)