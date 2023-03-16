"""
Стиль цитирования по American Psychological Association 7th edition.
"""
from string import Template

from pydantic import BaseModel

from formatters.base import BaseCitationFormatter
from formatters.models import (
    BookModel,
    ArticleModel,
    InternetResourceModel,
    ArticlesCollectionModel,
    DissertationModel,
)
from formatters.styles.base import BaseCitationStyle
from logger import get_logger

logger = get_logger(__name__)


def get_doi(doi: str) -> str:
    """
    Получение отформатированной информации о doi.
    :param str doi: Необходимость указания doi в цитировании.
    :return str doi: Информация о doi.
    """
    if doi:
        return doi
    return ""


def get_authors(input_authors: str) -> str:
    """
    Получение отформатированной информации об авторах.
    :param input_authors | str input_authors: Входная строка с авторами.
    :return: Информация об авторах.
    """
    authors = input_authors.split(",")
    res = ""
    separator = "&"
    # один автор
    if len(authors) == 1:
        res = input_authors
    else:
        # если после удаления авторов больше 20, то удаляем всех после и записываем последнего
        if len(authors) > 20:
            temp_author = authors[len(authors) - 1]
            del authors[:-1]
            del authors[18:]
            separator = "..."

            for author in authors:
                res += author + ", "
            res += f"{separator} {temp_author}"
        else:
            res = authors[0]
            del authors[0]
            for author in authors:
                res += f", {separator} {author}"
    return res


class APABook(BaseCitationStyle):
    """
    Форматирование для книг.
    """

    data: BookModel

    @property
    def template(self) -> Template:
        return Template("$authors ($year). ITALIC$title.ITALIC $publishing_house. $doi")

    def substitute(self) -> str:

        logger.info('Форматирование книги "%s" ...', self.data.title)

        return self.template.substitute(
            authors=get_authors(self.data.authors),
            title=self.data.title,
            publishing_house=self.data.publishing_house,
            year=self.data.year,
            doi=get_doi(self.data.doi),
        )


class APAArticle(BaseCitationStyle):
    """
    Форматирование для статей.
    """

    data: ArticleModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors ($year). $article_title. ITALIC$journal_title,ITALIC $journal_number, $pages. $doi"
        )

    def substitute(self) -> str:

        logger.info(
            'Форматирование статьи из журнала "%s" ...', self.data.article_title
        )
        return self.template.substitute(
            authors=get_authors(self.data.authors),
            article_title=self.data.article_title,
            journal_title=self.data.journal_title,
            year=self.data.year,
            journal_number=self.data.journal_number,
            pages=self.data.pages,
            doi=get_doi(self.data.doi),
        )


class APAInternetResource(BaseCitationStyle):
    """
    Форматирование для интернет-ресурсов.
    """

    data: InternetResourceModel

    @property
    def template(self) -> Template:
        return Template("$website ($access_date) ITALIC$article ITALIC $link")

    def substitute(self) -> str:

        logger.info('Форматирование интернет-ресурса "%s" ...', self.data.article)

        return self.template.substitute(
            article=self.data.article,
            website=self.data.website,
            link=self.data.link,
            access_date=self.data.access_date,
        )


class APACollectionArticle(BaseCitationStyle):
    """
    Форматирование для статьи из сборника.
    """

    data: ArticlesCollectionModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors ($year) $article_title, ITALIC$collection_title ITALIC $city: $publishing_house, $pages p."
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


class APADissertation(BaseCitationStyle):
    """
    Форматирование для диссертации.
    """

    data: DissertationModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors ($year) $dissertation_title, дис. [$degree $science_branch $specialty_code] $city, $pages p."
        )

    def substitute(self) -> str:
        logger.info('Форматирование диссертации "%s" ...', self.data.dissertation_title)

        return self.template.substitute(
            authors=get_authors(self.data.authors),
            dissertation_title=self.data.dissertation_title,
            degree=self.data.degree,
            science_branch=self.data.science_branch,
            specialty_code=self.data.specialty_code,
            city=self.data.city,
            year=self.data.year,
            pages=self.data.pages,
        )


class APACitationFormatter(BaseCitationFormatter):
    """
    Базовый класс для итогового форматирования списка источников.
    """

    formatters_map = {
        BookModel.__name__: APABook,
        InternetResourceModel.__name__: APAInternetResource,
        ArticlesCollectionModel.__name__: APACollectionArticle,
        DissertationModel.__name__: APADissertation,
        ArticleModel.__name__: APAArticle,
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
