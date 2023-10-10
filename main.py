import wikipedia
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Article(BaseModel):
    name: str
    content: str


class Articles(BaseModel):
    names: list[str]


class ArticleInput(BaseModel):
    name: str
    num: int


@app.get('/{request}', response_model=Articles)
def get_name(request: str):
    try:
        return Articles(names=wikipedia.search(request)[:8])
    except:
        return Articles(names=[])


@app.get('/article/{name}', response_model=Article)
def get_article(name: str, sentences: int):
    try:
        return Article(name=name, content=wikipedia.summary(name, sentences=sentences))
    except:
        return Article(name=name, content="Не найдено")


@app.post("/", response_model=Article)
def create_article(article_input: ArticleInput):
    try:
        return Article(name=article_input.name,
                       content=wikipedia.summary(article_input.name, sentences=article_input.num))
    except:
        return Article(name=article_input.name, content="Не найдено")
