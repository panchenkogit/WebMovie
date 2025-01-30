from locust import HttpUser, task, between
import random
from faker import Faker

fake = Faker()

class FilmUser(HttpUser):
    wait_time = between(1, 3)  # Имитация задержки между запросами (1-3 сек)

    def on_start(self):
        """Регистрируем и авторизуем пользователя"""
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()
        self.age = random.randint(14, 60)

        # Регистрация
        response = self.client.post("/reg", json={
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "age": self.age
        })

        if response.status_code == 200:
            self.token = response.cookies.get("access_token")  # Сохраняем токен из куков
        else:
            self.token = None

    @task(2)
    def add_film(self):
        """Добавление нового фильма"""
        if self.token:
            self.client.post("/film", json={
                "title": fake.sentence(nb_words=3),
                "description": fake.text(),
                "year": random.randint(1900, 2023),
                "rating": round(random.uniform(4.0, 10.0), 1)
            }, cookies={"access_token": self.token})

    @task(3)
    def get_all_films(self):
        """Получение списка всех фильмов"""
        self.client.get("/film/all")

    @task(2)
    def edit_film(self):
        """Редактирование случайного фильма"""
        if self.token:
            film_id = random.randint(1, 500)
            self.client.patch(f"/film/edit_film/{film_id}", json={
                "title": fake.sentence(nb_words=3),
                "description": fake.text()
            }, cookies={"access_token": self.token})

    @task(3)
    def rate_film(self):
        """Оценка случайного фильма"""
        if self.token:
            film_id = random.randint(1, 500)
            self.client.post(f"/film/rate_film/{film_id}", json={
                "rating": round(random.uniform(1.0, 10.0), 1)
            }, cookies={"access_token": self.token})

    @task(2)
    def add_film_to_library(self):
        """Добавление фильма в библиотеку"""
        if self.token:
            film_id = random.randint(1, 500)
            self.client.post(f"/film/add_film_in_library/{film_id}",
                cookies={"access_token": self.token})

    @task(2)
    def delete_film_from_library(self):
        """Удаление фильма из библиотеки"""
        if self.token:
            film_id = random.randint(1, 500)
            self.client.delete(f"/film/delete_film_in_library/{film_id}",
                cookies={"access_token": self.token})

    @task(1)
    def delete_film(self):
        """Удаление случайного фильма"""
        if self.token:
            film_id = random.randint(1, 500)
            self.client.delete(f"/film/delete_by_id/{film_id}",
                cookies={"access_token": self.token})

    @task(1)
    def create_director(self):
        """Добавление нового режиссера"""
        if self.token:
            self.client.post("/director", json={
                "name": fake.name(),
                "birthday": str(fake.date_of_birth(minimum_age=30, maximum_age=70))
            }, cookies={"access_token": self.token})

    @task(2)
    def get_film_by_id(self):
        """Получение информации о случайном фильме"""
        film_id = random.randint(1, 500)
        self.client.get(f"/film/get_by_id/{film_id}")

    @task(2)
    def get_recommendations(self):
        """Получение списка рекомендаций (если есть)"""
        if self.token:
            self.client.get("/recomend", cookies={"access_token": self.token})
