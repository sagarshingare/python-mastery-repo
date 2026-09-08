"""Production patterns for Flask applications.

Demonstrates application factories, blueprints, structured JSON error responses,
and health checks. Works seamlessly whether Flask is installed or in fallback mode.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

try:
    from flask import Blueprint, Flask, abort, jsonify, request
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False


def create_flask_app(test_config: dict[str, Any] | None = None) -> Any:
    """Application factory for a production-grade Flask API.

    To run:
        pip install flask
        FLASK_APP=api_development.flask.flask_app:create_flask_app flask run
    """
    if not HAS_FLASK:
        logger.warning("Flask is not installed in the current environment. Returning None.")
        return None

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev-secret-key-change-in-production",
        JSON_SORT_KEYS=False,
    )

    if test_config:
        app.config.update(test_config)

    # -----------------------------------------------------------------------
    # Blueprints
    # -----------------------------------------------------------------------
    api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

    # In-memory store
    _items: dict[str, dict[str, Any]] = {}

    @api_bp.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "healthy", "service": "flask-mastery-api"})

    @api_bp.route("/items", methods=["GET"])
    def list_items():
        return jsonify({"items": list(_items.values()), "count": len(_items)})

    @api_bp.route("/items", methods=["POST"])
    def create_item():
        data = request.get_json(silent=True)
        if not data or "name" not in data:
            return jsonify({"error": "Bad Request", "message": "'name' is required"}), 400

        item_id = str(len(_items) + 1)
        item = {"id": item_id, "name": data["name"], "price": float(data.get("price", 0.0))}
        _items[item_id] = item
        return jsonify(item), 201

    @api_bp.route("/items/<item_id>", methods=["GET"])
    def get_item(item_id: str):
        item = _items.get(item_id)
        if not item:
            abort(404)
        return jsonify(item)

    app.register_blueprint(api_bp)

    # -----------------------------------------------------------------------
    # Structured error handlers
    # -----------------------------------------------------------------------
    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "Not Found", "message": "The requested resource does not exist"}), 404

    @app.errorhandler(500)
    def handle_internal_error(error):
        logger.exception("Unhandled server error: %s", error)
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

    return app
