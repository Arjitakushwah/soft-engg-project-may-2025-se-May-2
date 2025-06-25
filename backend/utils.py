from flask import jsonify
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt

def jwt_required(required_role=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                identity = get_jwt_identity()
                claims = get_jwt()
                role = claims.get("role")

                if required_role and role != required_role:
                    return jsonify({"error": "Unauthorized: incorrect role"}), 403

                # Attach user info to kwargs for convenience
                kwargs['current_user_id'] = int(identity)
                kwargs['current_user_role'] = role
                return fn(*args, **kwargs)

            except Exception as e:
                return jsonify({"error": "Invalid or missing token", "detail": str(e)}), 401
        return wrapper
    return decorator
