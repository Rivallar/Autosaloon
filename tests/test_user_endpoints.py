import pytest

from cars.models import Auto


def test_cars_autos_list(client, setup_cars_autos):
    response = client.get('http://localhost:8000/cars/autos/')
    assert response.status_code == 200
    response = response.json()
    #print(response)
    assert response['count'] == Auto.objects.all().count()


@pytest.mark.parametrize(
    "car_exist, validity",
    [
        (True, 200),     # existing car
        (False, 404)     # car_id is wrong
    ])
@pytest.mark.django_db
def test_cars_autos_retrieve(client, setup_cars_autos, car_exist, validity):
    if car_exist:
        car_id = setup_cars_autos
        car = Auto.objects.get(id=car_id)
        url = f'http://localhost:8000/cars/autos/{car_id}/'
    else:
        url = f'http://localhost:8000/cars/autos/9999999999/'
    response = client.get(url, format='json')
    assert response.status_code == validity
    if car_exist:
        response = response.json()
        assert car.model_name == response['model_name']