def get_llm(model_backend="ollama", model_name=None):
    if model_backend == "openai":
        from langchain.chat_models import ChatOpenAI
        return ChatOpenAI(
            temperature=0,
            model=model_name or "gpt-3.5-turbo"
        )
    elif model_backend == "ollama":
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(
            temperature=0,
            model=model_name or "gemma3:latest"
        )
    else:
        raise ValueError(f"Unknown backend: {model_backend}")
