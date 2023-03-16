"""
Описание схем объектов (DTO).
"""

from typing import Optional

from pydantic import BaseModel, Field


class BookModel(BaseModel):
    """
    Модель книги:

    .. code-block::

        BookModel(
            authors="Иванов И.М., Петров С.Н.",
            title="Наука как искусство",
            edition="3-е",
            city="СПб.",
            publishing_house="Просвещение",
            year=2020,
            pages=999,
            doi="https://doi.org/10.1002/9781119466642"
        )
    """

    authors: str
    title: str
    edition: Optional[str]
    city: str
    publishing_house: str
    year: int = Field(..., gt=0)
    pages: int = Field(..., gt=0)
    doi: Optional[str]


class InternetResourceModel(BaseModel):
    """
    Модель интернет ресурса:

    .. code-block::

        InternetResourceModel(
            article="Наука как искусство",
            website="Ведомости",
            link="https://www.vedomosti.ru/",
            access_date="01.01.2021",
        )
    """

    article: str
    website: str
    link: str
    access_date: str


class ArticlesCollectionModel(BaseModel):

    """
    Модель сборника статей:

    .. code-block::

        ArticlesCollectionModel(
            authors="Иванов И.М., Петров С.Н.",
            article_title="Наука как искусство",
            collection_title="Сборник научных трудов",
            city="СПб.",
            publishing_house="АСТ",
            year=2020,
            pages="25-30",
        )
    """

    authors: str
    article_title: str
    collection_title: str
    city: str
    publishing_house: str
    year: int = Field(..., gt=0)
    pages: str


class DissertationModel(BaseModel):
    """
    Модель дисертации:

    .. code-block::

        DissertationModel(
            authors="Иванов И.М.",
            dissertation_title="Наука как искусство",
            degree="канд.",
            science_branch="экон.",
            specialty_code="01.01.01",
            city="СПб.",
            year=2020,
            pages="199",
        )
    """

    authors: str
    dissertation_title: str
    degree: str
    science_branch: str
    specialty_code: str
    city: str
    year: int = Field(..., gt=0)
    pages: int = Field(..., gt=0)


class ArticleModel(BaseModel):
    """
    Модель статьи:

    .. code-block::

        ArticleModel(
            authors="Иванов И.М., Петров С.Н.",
            article_title="Наука как искусство",
            journal_title="Образование и наука",
            year=2020,
            journal_number=10,
            pages="25-30",
        )
    """

    authors: str
    article_title: str
    journal_title: Optional[str]
    year: int = Field(..., gt=0)
    journal_number: Optional[int] = Field(..., gt=0)
    pages: str
    doi: Optional[str]
