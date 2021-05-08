from flask import jsonify, Blueprint, request
from flask_restful import abort
from . import db_session
from .models import People

blueprint = Blueprint(
    'api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/get_all_accounts&login=<string:lg>&token=<string:key>', methods=['GET'])
def get_accounts(lg, key):
    if lg == 'x@a' and key == 'yandex_lyceum_project':
        db_sess = db_session.create_session()
        admins = db_sess.query(People).filter(People.role == 'Admin').all()
        users = db_sess.query(People).filter(People.role == 'User').all()
        return jsonify(
            {'Administrators': [item.to_dict(only=('id', 'email')) for item in admins]},
            {'Users': [item.to_dict(only=('id', 'email')) for item in users]}
        )
    abort(403)


