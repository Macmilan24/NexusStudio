from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI # OpenRouter uses this
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from config.settings import settings

class LLMFactory:
    @staticmethod
    def get_llm(provider: str, model: str, temperature=0.7):
        """
        Returns a LangChain Chat Object based on the provider string.
        """
        if provider == "google":
            if not settings.google_api_key:
                raise ValueError("Google Provider selected but GOOGLE_API_KEY is missing.")
            return ChatGoogleGenerativeAI(
                model=model,
                temperature=temperature,
                google_api_key=settings.google_api_key
            )
        
        elif provider == "groq":
            if not settings.groq_api_key:
                raise ValueError("Groq Provider selected but GROQ_API_KEY is missing.")
            return ChatGroq(
                model_name=model,
                temperature=temperature,
                groq_api_key=settings.groq_api_key
            )
            
        elif provider == "openrouter":
            if not settings.openrouter_api_key:
                raise ValueError("OpenRouter selected but OPENROUTER_API_KEY is missing.")
            return ChatOpenAI(
                model=model,
                temperature=temperature,
                openai_api_key=settings.openrouter_api_key,
                openai_api_base="https://openrouter.ai/api/v1",
                default_headers={"HTTP-Referer": "http://localhost:3000", "X-Title": "NexusStudio"}
            )

        elif provider == "huggingface":
            # Using Serverless Inference API
            if not settings.hf_token:
                raise ValueError("HuggingFace selected but HF Token is missing.")
            llm = HuggingFaceEndpoint(
                repo_id=model,
                task="text-generation",
                huggingfacehub_api_token=settings.hf_token
            )
            return ChatHuggingFace(llm=llm)
        
        else:
            raise ValueError(f"Unknown provider: {provider}")

    @staticmethod
    def get_brain():
        """Get the high-intelligence model defined in .env"""
        return LLMFactory.get_llm(settings.brain_provider, settings.brain_model)

    @staticmethod
    def get_reflex():
        """Get the high-speed model defined in .env"""
        return LLMFactory.get_llm(settings.reflex_provider, settings.reflex_model, temperature=0.3)