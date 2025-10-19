from langchain_groq import ChatGroq


from src.config.settings import settings_obj

def get_groq_llm():
    return ChatGroq(
        api_key=settings_obj.GROQ_API_KEY,
        model=settings_obj.MODEL_NAME,
        temperature=settings_obj.TEMPERATURE,

    )
