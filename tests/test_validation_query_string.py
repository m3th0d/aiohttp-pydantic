from typing import Optional

from aiohttp import web

from aiohttp_pydantic import PydanticView


class ArticleView(PydanticView):
    async def get(
        self, with_comments: bool, age: Optional[int] = None, nb_items: int = 7
    ):
        return web.json_response(
            {"with_comments": with_comments, "age": age, "nb_items": nb_items}
        )


async def test_get_article_without_required_qs_should_return_an_error_message(
    aiohttp_client, loop
):
    app = web.Application()
    app.router.add_view("/article", ArticleView)

    client = await aiohttp_client(app)
    resp = await client.get("/article")
    assert resp.status == 418
    assert resp.content_type == "application/json"
    assert await resp.json() == [
        {
            "in": "query string",
            "loc": ["with_comments"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]


async def test_get_article_with_wrong_qs_type_should_return_an_error_message(
    aiohttp_client, loop
):
    app = web.Application()
    app.router.add_view("/article", ArticleView)

    client = await aiohttp_client(app)
    resp = await client.get("/article", params={"with_comments": "foo"})
    assert resp.status == 418
    assert resp.content_type == "application/json"
    assert await resp.json() == [
        {
            "in": "query string",
            "loc": ["with_comments"],
            "msg": "value could not be parsed to a boolean",
            "type": "type_error.bool",
        }
    ]


async def test_get_article_with_valid_qs_should_return_the_parsed_type(
    aiohttp_client, loop
):
    app = web.Application()
    app.router.add_view("/article", ArticleView)

    client = await aiohttp_client(app)

    resp = await client.get("/article", params={"with_comments": "yes", "age": 3})
    assert resp.status == 200
    assert resp.content_type == "application/json"
    assert await resp.json() == {"with_comments": True, "age": 3, "nb_items": 7}


async def test_get_article_with_valid_qs_and_omitted_optional_should_return_default_value(
    aiohttp_client, loop
):
    app = web.Application()
    app.router.add_view("/article", ArticleView)

    client = await aiohttp_client(app)

    resp = await client.get("/article", params={"with_comments": "yes"})
    assert await resp.json() == {"with_comments": True, "age": None, "nb_items": 7}
    assert resp.status == 200
    assert resp.content_type == "application/json"
