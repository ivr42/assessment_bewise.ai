# Тестовое задание на должность "Python разработчик (Junior)" 
Компания [Bewise.ai][1] 

Оригинал задания — [ТАМ][2]

Копия задания — [ТУТ][3]

[1]: <https://bewise.ai/>
[2]: <https://docs.google.com/document/d/1Xw4L-_riLixQFA127Uyvoq3JNrJm6hgSr7c7ux6z_fY/edit#heading=h.kki9g09lok4c>
[3]: <MISSION.md>

---

## Стек технологий, использованных в проекте
- fastapi
- fastapi-restful
- asyncpg
- pydantic
- alembic
- uvicorn
- python-multipart
- aiohttp
- python-dotenv
- sqlalchemy

## Установка

Устанавливается решения с помощью `docker compose`:
```shell
docker compose --file bewise.ai.infra/docker-compose.yml up -d
```
Для работы, приложению нужны следующие переменные окружения:

## Переменные окружения

#### Переменные, используемые во всех контейнерах
```dotenv
DB_HOST=postgres  # имя хоста базы данных
DB_PORT=5432      # порт базы данных
```

#### Настройка базы данных postgres
```dotenv
POSTGRES_DB=postgres                    # имя системной базы данных postgres
POSTGRES_USER=postgres                  # имя суперпользователя postgres
POSTGRES_PASSWORD='Very$ecretPassw0rd'  # пароль суперпользователя postgres
```

#### Настройки, общие для всех контейнеров приложений
```dotenv
DEBUG=False
```

#### Настройки приложения *test1*
```dotenv
TASK1_ROOT_PATH=/api/task1                  # путь (URI) к приложению
TASK1_APP_DB_NAME=bewiseai_task1            # имя базы данных для приложеня
TASK1_APP_DB_USER=bewiseai_task1_user       # пользователь БД
TASK1_APP_DB_PASSWORD='Very$ecretPassw0rd'  # пароль пользователя БД
```

#### Настройки приложения *test2*
```dotenv
TASK2_ROOT_PATH=/api/task2                  # путь (URI) к приложению
TASK2_APP_DB_NAME=bewiseai_task2            # имя базы данных для приложеня
TASK2_APP_DB_USER=bewiseai_task2_user       # пользователь БД
TASK2_APP_DB_PASSWORD='Very$ecretPassw0rd'  # пароль пользователя БД
```

## Использование
Работоспособность решения можно проверить как развернув решение локально,
так и в Интернет.

Реализованы следующие эндпоинты:
- Задача 1:
  - `POST` http://ivr.sytes.net:8080/api/task1/ — загрузка с сайта
    [jservice.io](https://jservice.io/) и сохранение в БД вопросов 
- Задача 2:
  - `POST` http://ivr.sytes.net:8080/api/task2/user/ — создание нового пользователя
  - `POST` http://ivr.sytes.net:8080/api/task2/record/ — добавление аудиозаписи
  - `GET` http://ivr.sytes.net:8080/api/task2/record?id=record_id&user=user_id — 
    скачивание аудиозаписи 

### Использование сервиса с помощью интерфейса SwaggerUI
Можно протестировать работу приложений, используя интерфейс 
[Swagger UI](https://github.com/swagger-api/swagger-ui),
предоставляемый FastAPI.
После разворачивания приложения, с использованием указанных выше значений
переменных `TASK1_ROOT_PATH` и `TASK2_ROOT_PATH`, они доступны по адресам:
- http://ivr.sytes.net:8080/api/task1/docs
- http://ivr.sytes.net:8080/api/task2/docs

### Использование API сервиса

#### Пример использования API Задачи 1:
```python
import json
import requests

url = "http://ivr.sytes.net:8080/api/task1/"

payload = json.dumps({"questions_num": 1})
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.json())

```
ответ:
```json
[
    {
        "id": 216704,
        "created_at": "2022-12-30T22:07:43.004000",
        "updated_at": "2022-12-30T22:07:43.004000",
        "question": "U2 honored Martin Luther King, singing, \"Free at last, they took your life, they could not take your\" this",
        "answer": "pride"
    }
]
```

#### Пример использования API Задачи 2

##### Создание пользователя
```python
import json
import requests

url = "http://ivr.sytes.net:8080/api/task2/user/"

payload = json.dumps({"name": "user1"})
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.json())
```
Ответ:
```json
{
    "id": "8d763552-9e1e-4e8b-9c1b-0041a4ff939b",
    "access_token": "c7dae192-b645-4249-94dd-731db7517aa2"
}
```

##### Добавление аудиозаписи для созданного выше пользователя
```python
import requests

url = "http://ivr.sytes.net:8080/api/task2/record"

payload = {
    "user_id": "8d763552-9e1e-4e8b-9c1b-0041a4ff939b",
    "access_token": "c7dae192-b645-4249-94dd-731db7517aa2",
}

files = [
    (
        "audio",
        (
            "taunt.wav",
            open("/Users/ivr/Downloads/sample_wav/taunt.wav", "rb"),
            "audio/wav",
        ),
    )
]
headers = {}

response = requests.request(
    "POST", url, headers=headers, data=payload, files=files
)

print(response.json())
```
Ответ:
```json
{
    "url": "http://ivr.sytes.net:8080/api/task2/record/?id=5fd0d4e9-5f78-483e-9419-dfda8e8b2aba&user=8d763552-9e1e-4e8b-9c1b-0041a4ff939b"
}
```

##### Загрузка аудиозаписи
```python
import re
import requests

def get_filename_from_header(header):
    if not header:
        return None
    return re.search("filename=(?P<filename>.+)", header).group("filename")

record_id = "5fd0d4e9-5f78-483e-9419-dfda8e8b2aba"
user_id = "8d763552-9e1e-4e8b-9c1b-0041a4ff939b"

url = f"http://ivr.sytes.net:8080/api/task2/record/?id={record_id}&user={user_id}"

response = requests.request("GET", url)

if response.ok and response.headers.get("content-type", None) == "audio/mpeg":
    header = response.headers.get("content-disposition", None)
    filename = get_filename_from_header(header) or f"{record_id}.mp3"

    with open(filename, "wb") as mp3_file:
        mp3_file.write(response.content)

elif response.headers.get("content-type", None) == "application/json":
    print(response.json())
else:
    print(response.status_code, response.text)
```