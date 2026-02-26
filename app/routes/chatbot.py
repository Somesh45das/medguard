"""
Chatbot API routes for real-time chat assistance.
"""
from flask import Blueprint, jsonify, request, session
from flask_login import current_user
from app.services.chatbot_service import HospitalChatbot

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")

# Initialize chatbot instance
bot = HospitalChatbot()


@chatbot_bp.route("/message", methods=["POST"])
def process_message():
    """
    Process chatbot message and return response.
    
    Expected JSON:
    {
        "message": "user message text",
        "context": {
            "patient_id": 123,
            "phone": "1234567890"
        }
    }
    """
    data = request.get_json()
    
    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400
    
    message = data.get("message", "").strip()
    user_context = data.get("context", {})
    
    # Add user role from current_user if authenticated
    if current_user.is_authenticated:
        user_context["user_role"] = "admin" if current_user.is_admin() else "patient"
        user_context["user_id"] = current_user.id
        user_context["user_name"] = current_user.name
        
        # Add patient-specific context
        if not current_user.is_admin():
            user_context["phone"] = current_user.phone if hasattr(current_user, 'phone') else None
    else:
        # Default to patient role for unauthenticated users
        user_context["user_role"] = "patient"
    
    # Add session context if available
    if hasattr(session, "get"):
        user_context["session_id"] = session.get("_id")
    
    # Process message
    response = bot.process_message(message, user_context)
    
    return jsonify(response)


@chatbot_bp.route("/reset", methods=["POST"])
def reset_context():
    """Reset chatbot context for new conversation."""
    bot.context = {}
    return jsonify({"status": "success", "message": "Context reset"})
