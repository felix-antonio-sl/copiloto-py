import requests
from flask import current_app


def call_deepseek_api(message, conversation_context=None, model="deepseek-chat"):
    """
    Sends a request to the DeepSeek API to generate a response given a user message and optionally a conversation context.
    
    :param message: A string containing the user message.
    :param conversation_context: Optional list of messages representing previous conversation context. Each message is a dict with keys 'role' and 'content'.
    :param model: The DeepSeek model to be used (default is 'deepseek-chat').
    :return: The JSON response from the API call.
    """
    # Return a simulated response if using the placeholder API key
    if current_app.config.get("DEEPSEEK_API_KEY") == "your_deepseek_api_key_here":
        return {"choices": [{"message": {"content": "Mensaje simulado: " + message}}]}
    
    url = f"{current_app.config.get('DEEPSEEK_BASE_URL')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {current_app.config.get('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }

    if conversation_context:
        messages_payload = conversation_context + [{"role": "user", "content": message}]
    else:
        messages_payload = [{"role": "user", "content": message}]

    payload = {
        "model": model,
        "messages": messages_payload
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"DeepSeek API error: {response.status_code} {response.text}") 