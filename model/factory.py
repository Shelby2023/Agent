from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.ollama import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama.chat_models import ChatOllama
from utils.config_handler import rag_conf


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) ->Optional[OllamaEmbeddings | ChatOllama]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self) ->Optional[OllamaEmbeddings | ChatOllama]:
        return ChatOllama(model=rag_conf["chat_model_name"])

class EmbeddingsFactory(BaseModelFactory):
    def generator(self) ->Optional[OllamaEmbeddings | ChatOllama]:
        return OllamaEmbeddings(model=rag_conf["embedding_model_name"])


chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()