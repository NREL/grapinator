from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView

from grapinator import settings, schema_settings, log
from grapinator.model import db_session
from grapinator.schema import *

# setup Flask
app = Flask(__name__)

# add CORS support
CORS(app, resources={r"/*": {
    "origins": settings.CORS_EXPOSE_ORIGINS
    ,"send_wildcard": settings.CORS_SEND_WILDCARD
    ,"methods": settings.CORS_ALLOW_METHODS
    ,"max_age": settings.CORS_HEADER_MAX_AGE
    ,"allow_headers": settings.CORS_ALLOW_HEADERS
    ,"expose_headers": settings.CORS_EXPOSE_HEADERS
    ,"supports_credentials": settings.CORS_SUPPORTS_CREDENTIALS
    }})

# set server_name if running local, not docker or server
if settings.FLASK_SERVER_NAME != '':
    app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS

app.add_url_rule(
    settings.FLASK_API_ENDPOINT,
    view_func=GraphQLView.as_view(
        'graphql',
        schema=gql_schema,
        graphiql=True # for having the GraphiQL interface     
    )
)

# set default response headers per NREL spec.
@app.after_request
def apply_custom_response(response):
    response.headers["X-Frame-Options"] = settings.HTTP_HEADERS_XFRAME
    response.headers["X-XSS-Protection"] = settings.HTTP_HEADERS_XSS_PROTECTION
    response.headers["Cache-Control"] = settings.HTTP_HEADER_CACHE_CONTROL
    response.headers["Access-Control-Allow-Headers"] = settings.CORS_ALLOW_HEADERS
    return response

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def main():
    log.info('>>>>> Starting development server at http://{}{} <<<<<'.format(app.config['SERVER_NAME'], settings.FLASK_API_ENDPOINT))
    # Note: can't use flask debug with vscode debugger.  default: False
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()
