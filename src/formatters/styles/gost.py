"""
Стиль цитирования по ГОСТ Р 7.0.5-2008.
"""
from string import Template


from pydantic import BaseModel

from formatters.base import BaseCitationFormatter
from formatters.models import (
    BookModel,
    InternetResourceModel,
    ArticleModel,
    ArticlesCollectionModel,
    DissertationModel,
)

from formatters.styles.base import BaseCitationStyle
from logger import get_logger

logger = get_logger(__name__)


class GOSTBook(BaseCitationStyle):
    """
    Форматирование для книг.
    """

    data: BookModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $title. – $edition$city: $publishing_house, $year. – $pages с."
        )

    def substitute(self) -> str:

        logger.info('Форматирование книги "%s" ...', self.data.title)

        return self.template.substitute(
            authors=self.data.authors,
            title=self.data.title,
            edition=self.get_edition(),
            city=self.data.city,
            publishing_house=self.data.publishing_house,
            year=self.data.year,
            pages=self.data.pages,
        )

    def get_edition(self) -> str:
        """
        Получение отформатированной информации об издательстве.

        :return: Информация об издательстве.
        """

        return f"{self.data.edition} изд. – " if self.data.edition else ""


class GOSTInternetResource(BaseCitationStyle):
    """
    Форматирование для интернет-ресурсов.
    """

    data: InternetResourceModel

    @property
    def template(self) -> Template:
        return Template(
            "$article // $website URL: $link (дата обращения: $access_date)."
        )

    def substitute(self) -> str:

        logger.info('Форматирование интернет-ресурса "%s" ...', self.data.article)

        return self.template.substitute(
            article=self.data.article,
            website=self.data.website,
            link=self.data.link,
            access_date=self.data.access_date,
        )


class GOSTCollectionArticle(BaseCitationStyle):
    """
    Форматирование для статьи из сборника.
    """

    data: ArticlesCollectionModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $article_title // $collection_title. – $city: $publishing_house, $year. – С. $pages."
        )

    def substitute(self) -> str:

        logger.info('Форматирование сборника статей "%s" ...', self.data.article_title)

        return self.template.substitute(
            authors=self.data.authors,
            article_title=self.data.article_title,
            collection_title=self.data.collection_title,
            city=self.data.city,
            publishing_house=self.data.publishing_house,
            year=self.data.year,
            pages=self.data.pages,
        )


class GOSTDissertation(BaseCitationStyle):
    """
    Форматирование для диссертации.
    Сидоров Б.Б. Название работы: дис. ... канд. психол. наук: 01.01.01 / Тверь, 2005. С. 54—55.
    """

    data: DissertationModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $dissertation_title: дис. $degree ... $science_branch. $specialty_code. $city, $year. С. $pages."
        )

    def substitute(self) -> str:
        logger.info('Форматирование диссертации "%s" ...', self.data.dissertation_title)

        return self.template.substitute(
            authors=self.data.authors,
            dissertation_title=self.data.dissertation_title,
            degree=self.data.degree,
            science_branch=self.data.science_branch,
            specialty_code=self.data.specialty_code,
            city=self.data.city,
            year=self.data.year,
            pages=self.data.pages,
        )


class GOSTArticle(BaseCitationStyle):
    """
    Форматирование для статьи.
    Иванов И.М., Петров С.Н. Наука как искусство2 // Образование и наука. 2020. № 10. С. 25-30.
    """

    data: ArticleModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $article_title // $journal_title. $year. № $journal_number. С. $pages."
        )

    def substitute(self) -> str:
        logger.info('Форматирование статьи "%s" ...', self.data.article_title)

        return self.template.substitute(
            authors=self.data.authors,
            article_title=self.data.article_title,
            journal_title=self.data.journal_title,
            year=self.data.year,
            journal_number=self.data.journal_number,
            pages=self.data.pages,
        )


class GOSTCitationFormatter(BaseCitationFormatter):
    """
    Базовый класс для итогового форматирования списка источников.
    """

    formatters_map = {
        BookModel.__name__: GOSTBook,
        InternetResourceModel.__name__: GOSTInternetResource,
        ArticlesCollectionModel.__name__: GOSTCollectionArticle,
        DissertationModel.__name__: GOSTDissertation,
        ArticleModel.__name__: GOSTArticle,
    }

    def __init__(self, models: list[BaseModel]) -> None:
        """
        Конструктор.
        :param models: Список объектов для форматирования
        """

        formatted_items = []
        for model in models:
            formatted_items.append(self.formatters_map.get(type(model).__name__)(model))  # type: ignore

        self.formatted_items = formatted_items

    def format(self) -> list[BaseCitationStyle]:
        """
        Форматирование списка источников.
        :return:
        """

        return sorted(self.formatted_items, key=lambda item: item.formatted)
