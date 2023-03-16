"""
Фикстуры для моделей объектов (типов источников).
"""
import pytest

from formatters.models import (
    BookModel,
    InternetResourceModel,
    ArticlesCollectionModel,
    ArticleModel,
    DissertationModel,
)


@pytest.fixture
def book_model_fixture() -> BookModel:
    """
    Фикстура модели книги.

    :return: BookModel
    """

    return BookModel(
        authors="Иванов И.М., Петров С.Н.",
        title="Наука как искусство",
        edition="3-е",
        city="СПб.",
        publishing_house="Просвещение",
        year=2020,
        pages=999,
        doi="10.2196/16504",
    )


@pytest.fixture
def internet_resource_model_fixture() -> InternetResourceModel:
    """
    Фикстура модели интернет-ресурса.

    :return: InternetResourceModel
    """

    return InternetResourceModel(
        article="Наука как искусство",
        website="Ведомости",
        link="https://www.vedomosti.ru",
        access_date="01.01.2021",
    )


@pytest.fixture
def articles_collection_model_fixture() -> ArticlesCollectionModel:
    """
    Фикстура модели сборника статей.

    :return: ArticlesCollectionModel
    """

    return ArticlesCollectionModel(
        authors="Иванов И.М., Петров С.Н.",
        article_title="Наука как искусство",
        collection_title="Сборник научных трудов",
        city="СПб.",
        publishing_house="АСТ",
        year=2020,
        pages="25-30",
    )


@pytest.fixture
def article_model_fixture() -> ArticleModel:
    """
    Фикстура модели статьи из журнала.

    :return: ArticleModel
    """

    return ArticleModel(
        authors="Иванов И.М., Петров С.Н.",
        article_title="Наука как искусство",
        journal_title="Образование и наука",
        year=2020,
        journal_number=10,
        pages="25-30",
        doi="10.2196/16504",
    )


@pytest.fixture
def dissertation_model_fixture() -> DissertationModel:
    """
    Фикстура модели диссертации.

    :return: DissertationModel
    """

    return DissertationModel(
        authors="Иванов И.М.",
        dissertation_title="Наука как искусство",
        degree="д-р.",
        science_branch="экон.",
        specialty_code="01.01.01",
        city="СПб.",
        year=2020,
        pages=199,
    )
