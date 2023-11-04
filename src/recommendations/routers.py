import logging
from fastapi import Depends, APIRouter
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import mean_squared_error
from math import sqrt
from ..auth.dao import UserDAO
from ..films.dao import FilmDAO
from ..user_actions.dao import UserFilmRatingDAO
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session

router = APIRouter()

# Установим уровень логирования, чтобы выводить все сообщения DEBUG и выше
logging.basicConfig(level=logging.DEBUG, encoding="utf8")
logger = logging.getLogger("recommendations")

@router.get('/get_recommendations')
async def get_recomendations(db: AsyncSession = Depends(get_async_session)):

    logger.info("Шаг 1: Загрузка данных из базы данных")

    users = await UserDAO.find_all(db)
    films = await FilmDAO.find_all(db)
    user_film_ratings = await UserFilmRatingDAO.find_all(db)

    logger.info("Шаг 2: Размер матрицы данных: (%d, %d)", len(users), len(films))

    # Шаг 3: Создание матрицы данных
    n_users = len(users)
    n_films = len(films)
    data_matrix = np.zeros((n_users, n_films))
    
    user_id_to_index = {user.id: i for i, user in enumerate(users)}
    film_id_to_index = {film.id: i for i, film in enumerate(films)}

    # Шаг 3: Заполнение матрицы данными
    logger.info("Шаг 3: Заполнение матрицы данными выполнено")
    
    for rating in user_film_ratings:
        user_index = user_id_to_index.get(rating.user_id)
        film_index = film_id_to_index.get(rating.film_id)
        if user_index is not None and film_index is not None:
            data_matrix[user_index, film_index] = rating.rating

    # Шаг 4: Создание матрицы сходства
    user_similarity = pairwise_distances(data_matrix, metric='cosine')
    film_similarity = pairwise_distances(data_matrix.T, metric='cosine')

    logger.info("Шаг 4: Размер матрицы сходства пользователей: %s", user_similarity.shape)
    logger.info("Шаг 4: Размер матрицы сходства фильмов: %s", film_similarity.shape)

    # Шаг 5: Расчет предсказаний
    def predict(ratings, similarity, type='user'):
        if type == 'user':
            mean_user_rating = ratings.mean(axis=1)
            ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
            pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
        elif type == 'film':
            pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
        return pred

    user_prediction = predict(data_matrix, user_similarity, type='user')
    film_prediction = predict(data_matrix, film_similarity, type='film')
    
    logger.info("Шаг 5: Размер матрицы предсказаний пользователей: %s", user_prediction.shape)
    logger.info("Шаг 5: Размер матрицы предсказаний фильмов: %s", film_prediction.shape)
    
    # Шаг 6: Оценка качества предсказаний
    def rmse(prediction, ground_truth):
        logger.info("Входные данные для функции rmse: prediction shape=%s, ground_truth shape=%s", prediction.shape, ground_truth.shape)
        prediction = prediction[ground_truth.nonzero()].flatten()
        ground_truth = ground_truth[ground_truth.nonzero()].flatten()
        logger.info("Размеры данных после фильтрации: prediction shape=%s, ground_truth shape=%s", prediction.shape, ground_truth.shape)
        return sqrt(mean_squared_error(prediction, ground_truth))

    def rate_quality(user_prediction, film_prediction):
        # Оценка качества предсказаний для пользователей
        user_rmse = rmse(user_prediction, data_matrix)
        logger.info('User-based CF RMSE: %f', user_rmse)
        # Оценка качества предсказаний для фильмов
        film_rmse = rmse(film_prediction, data_matrix.T)
        logger.info('Film-based CF RMSE: %f', film_rmse)
    
    rate_quality(user_prediction, film_prediction)
