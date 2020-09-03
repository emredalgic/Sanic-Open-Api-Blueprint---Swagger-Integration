from sanic import Sanic,Blueprint
from sanic_cors import CORS, cross_origin
from sanic.response import json
from sanic.exceptions import NotFound,ServerError
from sanic_openapi import doc,swagger_blueprint
from app.testapp import testapp

app = Sanic(__name__)
CORS(app)
app.blueprint(swagger_blueprint)
app.blueprint(testapp)

app.config["API_VERSION"] = "0.1.0"
app.config["API_TITLE"] = "Sanic-OpenAPI"
app.config["API_DESCRIPTION"] = "An example Swagger from Sanic-OpenAPI"
app.config["API_TERMS_OF_SERVICE"] = "https://github.com/huge-success/sanic-openapi/blob/master/README.md"
app.config["API_CONTACT_EMAIL"] = "emre.dalgic"
app.config["API_SCHEMES"] = []

@app.exception(NotFound)
async def ignore_404s(request, exception):
    return text("Yep, I totally found the page: {}".format(request.url))

@app.exception(ServerError)
async def server_error_handler(request, exception):
    return text("Oops, server error", status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
