from app.utils.celery.celery import celery

if __name__ == "__main__":
    celery.start(argv=["worker", "--loglevel=info", "--pool=solo"])
