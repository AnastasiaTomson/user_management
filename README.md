# Проект по управлению пользователями

## Описание
Проект представляет собой систему управления пользователями с реализацией CRUD операций, авторизацией через JWT токены и разграничением доступа на основе ролей (пользователь/администратор).

## Установка

### Шаги для развертывания проекта:

1. **Склонируйте репозиторий**.
    ```bash
    git clone 'https://github.com/AnastasiaTomson/user_managemet.git'
    cd user_managemet
    ```

2. **Сборка и запуск контейнеров**.
    Убедитесь, что Docker установлен на вашей машине. Далее выполните:
    ```bash
    docker-compose up --build
    ```

3. **Выполнение миграций**.
    После успешного запуска контейнеров, выполните миграции базы данных:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

4. **Доступ к приложению**.
    Приложение будет доступно по адресу [http://localhost:8000](http://localhost:8000).


5. **Тесты**.
    Для запуска тестов использовать команду:
    ```bash
    python manage.py test
    ```

## Эндпоинты API
### Регистрация пользователя

- **URL**: `/register/`

- **Метод**: `POST`

- **Тело запроса**: 
    ```json lines
    {
        "name": "Имя пользователя",
        "email": "email@example.com",
        "password": "Ваш_пароль",
        "role": "user" // (доступные роли: "user", "admin")
    }
    ```

- **Ответ**: 
    ```json lines
    {
        "id": 1,
        "name": "Имя пользователя",
        "email": "email@example.com",
        "role": "user",
        "created_at": "2024-10-01T00:00:00Z",
        "updated_at": "2024-10-01T00:00:00Z"
    }
    ```
  
### Аутентификация пользователя (вход)

- **URL**: `/login/`

- **Метод**: `POST`

- **Тело запроса**: 
    ```json lines
    {
        "email": "email@example.com",
        "password": "Ваш_пароль"
    }   
    ```

- **Ответ**: 
    ```json lines
    {
        "access": "JWT_токен_доступа",
        "refresh": "JWT_токен_обновления"
    }
    ```
  
### Получение информации о пользователе

- **URL**: `/users/<id>/`

- **Метод**: `GET`

- **Заголовки**: `Authorization: Bearer <JWT_токен_доступа>`

- **Ответ**: 
    ```json lines
    {
        "id": 1,
        "name": "Имя пользователя",
        "email": "email@example.com",
        "role": "user",
        "created_at": "2024-10-01T00:00:00Z",
        "updated_at": "2024-10-01T00:00:00Z"
    }   
    ```
  
### Обновление информации о пользователе

- **URL**: `/users/<id>/`

- **Метод**: `PUT` или `PATCH`

- **Заголовки**: `Authorization: Bearer <JWT_токен_доступа>`

- **Тело запроса**: 
    ```json lines
    {
        "name": "Новое имя пользователя",
        "email": "новый_email@example.com",
        "role": "user" // (можно обновить роль, если это администратор)
    }   
    ```
  
- **Ответ**: 
    ```json lines
    {
        "id": 1,
        "name": "Новое имя пользователя",
        "email": "новый_email@example.com",
        "role": "user",
        "created_at": "2024-10-01T00:00:00Z",
        "updated_at": "2024-10-01T00:00:00Z"
    }   
    ```
  
### Удаление пользователя

- **URL**: `/users/<id>/`

- **Метод**: `DELETE`

- **Заголовки**: `Authorization: Bearer <JWT_токен_доступа>`
  
- **Ответ**: 
    ```json lines
    {
        "detail": "User deleted successfully."
    }
    ```

### Завершение работы

Чтобы остановить и удалить контейнеры, выполните:
```bash
docker-compose down
