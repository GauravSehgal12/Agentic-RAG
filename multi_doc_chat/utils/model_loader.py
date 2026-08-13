import os
import sys
import json
from dotenv import load_dotenv

from pydantic import SecretStr
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from multi_doc_chat.utils.config_loader import load_config
from multi_doc_chat.logger import GLOBAL_LOGGER as log
from multi_doc_chat.exception.custom_exception import DocumentPortalException


class ApiKeyManager:
    REQUIRED_KEYS = ["GROQ_API_KEY"]

    def __init__(self):
        load_dotenv()

        self.api_keys = {}

        raw = os.getenv("apikeyliveclass")

        if raw:
            try:
                parsed = json.loads(raw)

                if not isinstance(parsed, dict):
                    raise ValueError(
                        "apikeyliveclass is not a valid JSON object"
                    )

                self.api_keys = parsed

            except Exception as e:
                log.warning(
                    "Failed to parse API_KEYS as JSON",
                    error=str(e)
                )

        # Fallback to normal environment variable
        for key in self.REQUIRED_KEYS:
            if not self.api_keys.get(key):
                env_val = os.getenv(key)

                if env_val:
                    self.api_keys[key] = env_val

        # Check missing keys
        missing = [
            key for key in self.REQUIRED_KEYS
            if not self.api_keys.get(key)
        ]

        if missing:
            raise DocumentPortalException(
                "Missing required API keys",
                sys
            )

        log.info("Groq API key loaded successfully")

    def get(self, key: str) -> str:
        value = self.api_keys.get(key)

        if not value:
            raise KeyError(
                f"API key for {key} is missing"
            )

        return value


class ModelLoader:

    def __init__(self):
        self.api_key_mgr = ApiKeyManager()
        self.config = load_config()

    def load_embeddings(self):

        model_name = self.config["embedding_model"]["model_name"]

        log.info(
            "Loading Hugging Face embedding model",
            model=model_name
        )

        return HuggingFaceEmbeddings(
            model_name=model_name
        )

    def load_llm(self):

        llm_config = self.config["llm"]["groq"]

        model_name = llm_config["model_name"]

        temperature = llm_config.get(
            "temperature",
            0.2
        )

        max_tokens = llm_config.get(
            "max_output_tokens",
            2048
        )

        log.info(
            "Loading Groq LLM",
            model=model_name
        )

        return ChatGroq(
    model=model_name,
    api_key=SecretStr(
         self.api_key_mgr.get("GROQ_API_KEY")
        ),
    temperature=temperature,
    max_tokens=max_tokens
)


if __name__ == "__main__":

    loader = ModelLoader()

    # Hugging Face embeddings
    embeddings = loader.load_embeddings()

    print("Embedding model loaded successfully")

    result = embeddings.embed_query(
        "What is Agentic AI?"
    )

    print("Embedding size:", len(result))

    # Groq LLM
    llm = loader.load_llm()

    print("Groq LLM loaded successfully")

    result = llm.invoke(
        "Explain Agentic AI in simple words."
    )

    print(result.content)