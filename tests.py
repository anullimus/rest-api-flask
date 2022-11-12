from app import client, table_name
from models import Inventory


def test_simple():
    mylist = [1, 2, 3, 4, 5]

    assert 1 in mylist


def test_post():
    data = {
        'title': 'Cable',
        'description': 'for server #28'
    }
    res = client.post(table_name, json=data)

    db_data = Inventory.query
    assert res.status_code == 200
    assert len(res.get_json()) == len(db_data.all())
    assert res.get_json()[-1]['title'] == data['title']


def test_get():
    res = client.get(table_name)
    db_data = Inventory.query
    assert res.status_code == 200
    assert len(res.get_json()) == len(db_data.all())
    assert res.get_json()[0]['id'] == 1


def test_put():
    test_id, test_title = 1, "Cable"
    data = {'description': 'for server #34'}
    res = client.put(table_name + '/' + str(test_id), json=data)
    assert res.status_code == 200
    assert Inventory.query.get(test_id).title == test_title


def test_delete():
    test_id = 1
    res = client.delete(table_name + '/' + str(test_id))
    assert res.status_code == 204
    assert Inventory.query.get(test_id) is None
