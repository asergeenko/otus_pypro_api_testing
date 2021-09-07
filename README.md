# Scoring API
API сервиса скоринга

[Структура запроса](#Структура-запроса)

[Структура ответа](#Структура-ответа)

[Методы](#Методы)

[online_score](#online_score)

[clients_interests](#clients_interests)

[Запуск](#Запуск)

[Параметры](#Параметры)

[Тестирование](#Тестирование)

### Структура запроса

`{"account": "<имя компании партнера>", "login": "<имя пользователя>", "method": "<имя метода>", "token": "
<аутентификационный токен>", "arguments": {<словарь с аргументами вызываемого метода>}}`

**account** - строка, опционально, может быть пустым

**login** - строка, обязательно, может быть пустым

**method** - строка, обязательно, может быть пустым

**token** - строка, обязательно, может быть пустым

**arguments** - словарь, обязательно, может быть пустым

### Структура ответа

**OK**

`{"code": <числовой код>, "response": {<ответ вызываемого метода>}}`

**Ошибка**

`{"code": <числовой код>, "error": {<сообщения об ошибке>}}`

### Методы

#### online_score

##### Аргументы

**phone** - строка или число, длиной 11, начинается с 7, опционально, может быть пустым

**email** - строка, в которой есть @, опционально, может быть пустым

**first_name** - строка, опционально, может быть пустым

**last_name** - строка, опционально, может быть пустым

**birthday** - дата в формате DD.MM.YYYY, с которой прошло не больше 70 лет, опционально, может быть пустым

**gender** - число 0, 1 или 2, опционально, может быть пустым

##### Структура ответа

**OK**

`{"score": <число>}`

**Ошибка**

`{"code": 422, "error": "<сообщение о том какое поле(я) невалидно(ы) и как именно>"}`

**Пример**

`$ curl -X POST -H "Content-Type: application/json" -d '{"account": "horns&hoofs", "login": "h&f", "method":
"online_score", "token":
"55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd
"arguments": {"phone": "79175002040", "email": "user@mail.com", "first_name": "Иванов", "last_name":
"Иван", "birthday": "01.01.1990", "gender": 1}}' http://127.0.0.1:8080/method/`

Ответ:

`{"code": 200, "response": {"score": 5.0}}`

#### clients_interests

##### Аргументы

**client_ids** - массив числе, обязательно, не пустое

**date** - дата в формате DD.MM.YYYY, опционально, может быть пустым

##### Структура ответа

**OK**

В ответ выдается словарь *<id клиента>:<список интересов>*

`{"client_id1": ["interest1", "interest2" ...], "client2": [...] ...}`

**Ошибка**

`{"code": 422, "error": "<сообщение о том какое поле(я) невалидно(ы) и как именно>"}`

**Пример**

`$ curl -X POST -H "Content-Type: application/json" -d '{"account": "horns&hoofs", "login": "admin", "method":
"clients_interests", "token":
"d3573aff1555cd67dccf21b95fe8c4dc8732f33fd4e32461b7fe6a71d83c947688515e36774c00fb630b039fe2223c991f045f13f240913860502
"arguments": {"client_ids": [1,2,3,4], "date": "20.07.2017"}}' http://127.0.0.1:8080/method/`

Ответ:

`{"code": 200, "response": {"1": ["books", "hi-tech"], "2": ["pets", "tv"], "3": ["travel", "music"], "4":
["cinema", "geek"]}}`

## Запуск
`api.py [-p|--port PORT] [-l|--log LOGPATH]`

### Параметры

*PORT* - номер порта для работы сервера (по умолчанию 8080)

*LOGPATH* - путь до лог-файла (по умолчанию логирование производится в stdout) 

## Тестирование

- модульное
  `python -m unittest discover -s tests/unit`

- функциональное
  `python -m unittest discover -s tests/func`

- все тесты целиком
  `python -m unittest discover -s tests`

## Требования
- Python >= 3.6
- redis
- fakeredis
