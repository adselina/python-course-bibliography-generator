"""
Тестирование функций оформления списка источников по ГОСТ Р 7.0.5-2008.
"""

from formatters.base import BaseCitationFormatter
from formatters.models import (
    BookModel,
    ArticleModel,
    DissertationModel,
    ArticlesCollectionModel,
    InternetResourceModel,
)
from formatters.styles.apa import (
    APABook,
    APAArticle,
    APADissertation,
    APACollectionArticle,
    APAInternetResource,
)


class TestAPA:
    """
    Тестирование оформления списка источников согласно American Psychological Association 7th edition.
    """

    def test_book(self, book_model_fixture: BookModel) -> None:
        """
        Тестирование форматирования книги.
        :param BookModel book_model_fixture: Фикстура модели книги
        :return:
        """

        model = APABook(book_model_fixture)

        assert (
            model.formatted
            == "Иванов И.М., &  Петров С.Н. (2020). ITALICНаука как искусство.ITALIC Просвещение. "
            "10.2196/16504"
        )

    def test_article(self, article_model_fixture: ArticleModel) -> None:
        """
        Тестирование форматирования статьи из журнала.
        :param ArticleModel article_model_fixture: Фикстура модели статьи
        :return:
        """

        model = APAArticle(article_model_fixture)

        assert (
            model.formatted
            == "Иванов И.М., &  Петров С.Н. (2020). Наука как искусство. ITALICОбразование и "
            "наука,ITALIC 10, 25-30. 10.2196/16504"
        )

    def test_dissertation(self, dissertation_model_fixture: DissertationModel) -> None:
        """
        Тестирование форматирования книги.
        :param DissertationModel dissertation_model_fixture: Фикстура модели книги
        :return:
        """

        model = APADissertation(dissertation_model_fixture)

        assert (
            model.formatted
            == "Иванов И.М. (2020) Наука как искусство, дис. [д-р. экон. 01.01.01] СПб., 199 p."
        )

    def test_internet_resource(
        self, internet_resource_model_fixture: InternetResourceModel
    ) -> None:
        """
        Тестирование форматирования интернет-ресурса.

        :param InternetResourceModel internet_resource_model_fixture: Фикстура модели интернет-ресурса
        :return:
        """

        model = APAInternetResource(internet_resource_model_fixture)

        assert (
            model.formatted
            == "Ведомости (01.01.2021) ITALICНаука как искусство ITALIC https://www.vedomosti.ru"
        )

    def test_articles_collection(
        self, articles_collection_model_fixture: ArticlesCollectionModel
    ) -> None:
        """
        Тестирование форматирования сборника статей.

        :param ArticlesCollectionModel articles_collection_model_fixture: Фикстура модели сборника статей
        :return:
        """

        model = APACollectionArticle(articles_collection_model_fixture)

        assert (
            model.formatted
            == "Иванов И.М., Петров С.Н. (2020) Наука как искусство, ITALICСборник научных трудов "
            "ITALIC СПб.: АСТ, 25-30 p."
        )

    def test_citation_formatter(
        self,
        book_model_fixture: BookModel,
        internet_resource_model_fixture: InternetResourceModel,
        articles_collection_model_fixture: ArticlesCollectionModel,
        article_model_fixture: ArticleModel,
        dissertation_model_fixture: DissertationModel,
    ) -> None:
        """
        Тестирование функции итогового форматирования списка источников.
        :param BookModel book_model_fixture: Фикстура модели книги
        :param InternetResourceModel internet_resource_model_fixture: Фикстура модели интернет-ресурса
        :param ArticlesCollectionModel articles_collection_model_fixture: Фикстура модели сборника статей
        :param ArticlesModel article_model_fixture: Фикстура модели статьи
        :param DissertationModel dissertation_model_fixture: Фикстура модели диссертации
        :return:
        """

        models = [
            APABook(book_model_fixture),
            APAInternetResource(internet_resource_model_fixture),
            APACollectionArticle(articles_collection_model_fixture),
            APAArticle(article_model_fixture),
            APADissertation(dissertation_model_fixture),
        ]

        result = BaseCitationFormatter(models).format()
        # тестирование сортировки списка источников
        assert result[0] == models[1]
        assert result[1] == models[4]
        assert result[2] == models[0]
        assert result[3] == models[3]
        assert result[4] == models[2]
