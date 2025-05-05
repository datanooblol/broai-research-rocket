from package.database.user.db import UserDB
from package.database.session.db import SessionDB
from package.database.web_register.db import WebDB
from broai.experiments.huggingface_embedding import BAAIEmbedding
from broai.experiments.cross_encoder import ReRanker
from broai.experiments.vector_store import DuckVectorStore
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables
baai_em = BAAIEmbedding()
reranker = ReRanker()


def get_UserDB():
    try:
        yield UserDB(db_name=os.getenv("DB_NAME"))
    finally:
        pass


def get_SessionDB():
    try:
        yield SessionDB(db_name=os.getenv("DB_NAME"))
    finally:
        pass


def get_WebDB():
    try:
        yield WebDB(db_name=os.getenv("DB_NAME"))
    finally:
        pass


def get_KnowledgeDB():
    try:
        yield DuckVectorStore(
            db_name=os.getenv("DB_NAME"),
            table="knowledge",
            embedding=baai_em
        )
    finally:
        pass


def get_ReRanker():
    try:
        yield reranker
    finally:
        pass