"""
REST API endpoints for AJAX calls and external integrations.
"""
from flask import Blueprint, jsonify, request
from datetime import date, datetime
from app.models.models import Department, Doctor
from app.services.crowd_predictor import CrowdPredictor
from app.services.slot_optimizer import SlotOptimizer
from app.services.queue_manager import QueueManager

api_bp = Blueprint("api", __name__)


@api_bp.route("/crowd-prediction")
def crowd_prediction():
    """Get crowd prediction for a department."""
    dept_id = request.args.get("department_id", 1, type=int)
    target_date = request.args.get("date", date.today().isoformat())
    hour = request.args.get("hour", datetime.now().hour, type=int)

    try:
        target = date.fromisoformat(target_date)
    except ValueError:
        target = date.today()

    predictor = CrowdPredictor()
    result = predictor.predict_crowd_level(dept_id, target, hour)
    return jsonify(result)


@api_bp.route("/crowd-timeline")
def crowd_timeline():
    """Get full-day crowd timeline."""
    dept_id = request.args.get("department_id", 1, type=int)
    target_date = request.args.get("date", date.today().isoformat())

    try:
        target = date.fromisoformat(target_date)
    except ValueError:
        target = date.today()

    predictor = CrowdPredictor()
    timeline = predictor.predict_day_timeline(dept_id, target)
    return jsonify({"timeline": timeline})


@api_bp.route("/available-slots")
def available_slots():
    """Get available slots for a doctor."""
    doctor_id = request.args.get("doctor_id", type=int)
    target_date = request.args.get("date", date.today().isoformat())

    if not doctor_id:
        return jsonify({"error": "doctor_id required"}), 400

    try:
        target = date.fromisoformat(target_date)
    except ValueError:
        target = date.today()

    optimizer = SlotOptimizer()
    slots = optimizer.get_available_slots(doctor_id, target)
    return jsonify({"slots": slots, "total": len(slots)})


@api_bp.route("/queue-stats")
def queue_stats():
    """Get queue statistics."""
    dept_id = request.args.get("department_id", type=int)
    queue_mgr = QueueManager()
    stats = queue_mgr.get_queue_stats(dept_id)
    return jsonify(stats)


@api_bp.route("/doctors-by-department")
def doctors_by_department():
    """Get doctors for a department."""
    dept_id = request.args.get("department_id", type=int)
    if not dept_id:
        return jsonify({"error": "department_id required"}), 400

    doctors = Doctor.query.filter_by(department_id=dept_id, is_available=True).all()
    result = [
        {
            "id": d.id,
            "name": d.name,
            "specialization": d.specialization,
            "availability": round(d.availability_percentage, 1),
        }
        for d in doctors
    ]
    return jsonify({"doctors": result})
