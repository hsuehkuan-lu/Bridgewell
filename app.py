from flask import Flask
from flask_graphql import GraphQLView
app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_world():
    return 'Home Index.'


import api
from gql_api import SCHEMA


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=SCHEMA,
        graphiql=True # for having the GraphiQL interface
    )
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    api.SCOPED_SESSION.remove()


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
