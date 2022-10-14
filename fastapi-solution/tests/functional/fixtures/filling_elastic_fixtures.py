import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from ..settings import test_settings
from ..testdata.data import GENRES, MOVIES, PERSONS
from ..utils.helpers import elastic_filling_index, elastic_delete_data


@pytest_asyncio.fixture(scope="function")
async def es_write_genre(es_client: AsyncElasticsearch):
    """Фикстура для записи и удаления данных из индекса жанров в elasticsearch"""
    await elastic_filling_index(es_client, test_settings.genres_index, GENRES)
    yield
    await elastic_delete_data(es_client, test_settings.genres_index)


@pytest_asyncio.fixture(scope="function")
async def es_write_movies(es_client: AsyncElasticsearch):
    """Фикстура для записи и удаления данных из индекса кинопроизведений в elasticsearch"""
    await elastic_filling_index(es_client, test_settings.movies_index, MOVIES)
    yield
    await elastic_delete_data(es_client, test_settings.movies_index)


@pytest_asyncio.fixture(scope="function")
async def es_write_persons(es_client: AsyncElasticsearch):
    """Фикстура для записи и удаления данных из индекса персон в elasticsearch"""
    await elastic_filling_index(es_client, test_settings.persons_index, PERSONS)
    yield
    await elastic_delete_data(es_client, test_settings.persons_index)
