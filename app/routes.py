from flask import Blueprint, request, jsonify, render_template, current_app
from app import db
from app.models import Conversation
from app.deepseek import call_deepseek_api
from openai import OpenAI
import logging

bp = Blueprint('chat', __name__)

@bp.route('/', methods=['GET'])
def home():
    return jsonify({"status": "API funcionando"})

@bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    conversation_context = data.get('context', None)  # Contexto opcional

    if not user_message:
        return jsonify({'error': 'No se proporcionó mensaje.'}), 400

    try:
        # Call the DeepSeek API with the provided message and optional context using deepseek-chat model
        response_data = call_deepseek_api(user_message, conversation_context, model='deepseek-chat')
        # Extract the bot's response from the API response (assumes response structure based on DeepSeek docs)
        chat_response = response_data['choices'][0]['message']['content']

        # Save the conversation to the database
        conv = Conversation(user_message=user_message, bot_response=chat_response)
        db.session.add(conv)
        db.session.commit()

        return jsonify({'response': chat_response, 'conversation_id': conv.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/chat-ui', methods=['GET'])
def chat_ui():
    return render_template("chat-ui.html")

@bp.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos JSON"}), 400
    
    user_message = data.get("message")
    model_choice = data.get("model", "chat")
    
    if not user_message:
        return jsonify({"error": "No se proporcionó mensaje"}), 400

    try:
        model_name = "deepseek-chat" if model_choice == "chat" else "deepseek-reasoner"
        messages = [{"role": "user", "content": user_message}]
        
        response = get_response(messages, model_name)
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error en api_chat: {e}")
        return jsonify({"error": str(e)}), 500

def get_response(messages, model_name):
    try:
        client = OpenAI(
            api_key=current_app.config.get("DEEPSEEK_API_KEY"),
            base_url=current_app.config.get("DEEPSEEK_BASE_URL")
        )
        
        response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )
        
        if model_name == 'deepseek-reasoner':
            message = response.choices[0].message
            reasoning = getattr(message, "reasoning_content", "")
            answer = getattr(message, "content", "")
            return {"reasoning": reasoning, "answer": answer}
        return {"answer": response.choices[0].message.content}
    except Exception as e:
        logging.error(f"Error en get_response: {e}")
        return {"error": str(e)}