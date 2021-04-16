from flask import Flask
from flask_graphql import GraphQLView
from database import db, SCOPED_SESSION
from api.views import dsp as dsp_views
from config import DATABASE_URI


def create_app():
    app = Flask(__name__)
    app.debug = True

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.register_blueprint(dsp_views.dsp_app)
    db.init_app(app)

    # with app.app_context():
    #     # from api.models import dsp as dsp_model
    #     Base.metadata.create_all()
    return app


app = create_app()


@app.route('/')
def hello_world():
    return 'Home Index.'


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
    SCOPED_SESSION.remove()


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
