import pytest
import requests

BASE_URL = "https://reqres.in/api"

def test_get_users_list():
    """
    Тест API 1: Получение списка пользователей (GET /api/users?page=2)
    """
    response = requests.get(f"{BASE_URL}/users?page=2")
    assert response.status_code == 200, f"Ожидался статус 200, получено {response.status_code}"
    data = response.json()
    assert "data" in data, "В ответе отсутствует ключ 'data'"

def test_get_single_user():
    """
    Тест API 2: Получение конкретного пользователя (GET /api/users/2)
    """
    response = requests.get(f"{BASE_URL}/users/2")
    assert response.status_code == 200, f"Ожидался статус 200, получено {response.status_code}"
    data = response.json()
    assert "data" in data and data["data"]["id"] == 2, "Неверные данные пользователя"

def test_create_user():
    """
    Тест API 3: Создание пользователя (POST /api/users)
    """
    payload = {"name": "John", "job": "QA"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201, f"Ожидался статус 201, получено {response.status_code}"
    data = response.json()
    assert data.get("name") == "John", "Имя пользователя не соответствует"
    assert data.get("job") == "QA", "Должность пользователя не соответствует"

def test_update_user():
    """
    Тест API 4: Обновление данных пользователя (PUT /api/users/2)
    """
    payload = {"name": "John", "job": "Lead QA"}
    response = requests.put(f"{BASE_URL}/users/2", json=payload)
    assert response.status_code == 200, f"Ожидался статус 200, получено {response.status_code}"
    data = response.json()
    assert data.get("job") == "Lead QA", "Должность не обновлена"

def test_delete_user():
    """
    Тест API 5: Удаление пользователя (DELETE /api/users/2)
    """
    response = requests.delete(f"{BASE_URL}/users/2")
    assert response.status_code == 204, f"Ожидался статус 204, получено {response.status_code}"

def test_login_failure():
    """
    Тест API 6: Авторизация (негативный сценарий) (POST /api/login)
    """
    payload = {"email": "test@mail.com", "password": "1234"}
    response = requests.post(f"{BASE_URL}/login", json=payload)
    # Согласно документации ReqRes, при некорректных данных возвращается статус 400
    assert response.status_code == 400, f"Ожидался статус 400, получено {response.status_code}"
