from flask import Flask, jsonify, request
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

client = app.test_client()

engine = create_engine('sqlite:///db.sqllite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)   # creates schema of db in db when run the app


table_name = '/' + 'inventory'
table_id = 'inventory_id'


"""Below code shows the full-pac of CRUD-routes"""


@app.route(table_name, methods=['GET'])
def get_list():
    inventories = Inventory.query.all()
    serialized = []
    for inventory in inventories:
        serialized.append({
            'id': inventory.id,
            'title': inventory.title,
            'description': inventory.description
        })
    return jsonify(serialized)


@app.route(table_name, methods=['POST'])
def update_list():
    new_one = Inventory(**request.json)
    session.add(new_one)
    session.commit()
    serialized = []
    inventories = Inventory.query.all()
    for inventory in inventories:
        serialized.append({
            'id': inventory.id,
            'title': inventory.title,
            'description': inventory.description
        })
    return jsonify(serialized)


@app.route(table_name + '/<int:' + table_id + '>', methods=['PUT'])
def update_inventory(inventory_id: int):
    item = Inventory.query.filter(Inventory.id == inventory_id).first()
    params = request.json
    if not item:
        return {'message': 'no inventory with this id'}, 400
    for key, val in params.items():
        setattr(item, key, val)
    session.commit()
    serialized = {
        'id': item.id,
        'title': item.title,
        'description': item.description
    }
    return serialized


@app.route(table_name + '/<int:' + table_id + '>', methods=['DELETE'])
def delete_inventory(inventory_id: int) -> tuple:
    item = Inventory.query.filter(Inventory.id == inventory_id).first()
    if not item:
        return {'message': 'no inventory with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()
