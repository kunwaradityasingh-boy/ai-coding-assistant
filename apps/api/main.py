import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from src.analysis.evidence_builder import build_code_evidence
from src.fixer.local_fixer import LocalFixer
from src.review.review_service import ReviewService
from src.runtime.python_runner import run_python_code
from src.tutor.local_tutor import LocalTutor
from src.verification.verifier import Verifier


app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024


@app.errorhandler(413)
def handle_request_too_large(error):
    return jsonify(
        {
            "success": False,
            "error": "Request body is too large.",
        }
    ), 413


CORS(
    app,
    origins=["http://127.0.0.1:5001"],
)


@app.get("/")
def home():
    return "AI Coding Assistant is running!"


@app.post("/run")
def run_code():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {
                "success": False,
                "error": "Invalid JSON request.",
            }
        ), 400

    if not data or "code" not in data:
        return jsonify(
            {
                "success": False,
                "error": "Code is required.",
            }
        ), 400

    code = data["code"]

    if not isinstance(code, str):
        return jsonify(
            {
                "success": False,
                "error": "Code must be a string.",
            }
        ), 400

    if not code.strip():
        return jsonify(
            {
                "success": False,
                "error": "Code cannot be empty.",
            }
        ), 400

    try:
        result = run_python_code(code)

        return jsonify(
            {
                "success": result["success"],
                "stdout": result["stdout"],
                "stderr": result["stderr"],
                "return_code": result["return_code"],
                "timed_out": result["timed_out"],
            }
        )

    except Exception:
        app.logger.exception(
            "Unexpected error while running code."
        )

        return jsonify(
            {
                "success": False,
                "error": "Internal server error.",
            }
        ), 500


@app.post("/analyze")
def analyze_code():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {
                "success": False,
                "error": "Invalid JSON request.",
            }
        ), 400

    if not data or "code" not in data:
        return jsonify(
            {
                "success": False,
                "error": "Code is required.",
            }
        ), 400

    code = data["code"]

    if not isinstance(code, str):
        return jsonify(
            {
                "success": False,
                "error": "Code must be a string.",
            }
        ), 400

    if not code.strip():
        return jsonify(
            {
                "success": False,
                "error": "Code cannot be empty.",
            }
        ), 400

    try:
        # -------------------------------------------------
        # 1. Build deterministic evidence
        # -------------------------------------------------
        evidence = build_code_evidence(code)

        # -------------------------------------------------
        # 2. Code Review
        # -------------------------------------------------
        review_service = ReviewService()

        review_result = review_service.review(
            code,
            evidence,
        )

        # -------------------------------------------------
        # 3. Beginner Tutor
        # -------------------------------------------------
        tutor = LocalTutor()

        tutor_result = tutor.teach(
            code,
            evidence,
        )

        # -------------------------------------------------
        # 4. Automatic Fix
        # -------------------------------------------------
        fixer = LocalFixer()

        fix_result = fixer.fix(
            code,
            evidence,
        )

        # -------------------------------------------------
        # 5. Verify generated fix
        # -------------------------------------------------
        verification_result = None

        if fix_result.success and fix_result.fixed_code:
            verifier = Verifier()

            verification_result = verifier.verify(
                original_code=code,
                fixed_code=fix_result.fixed_code,
            )

        # -------------------------------------------------
        # 6. Final API response
        # -------------------------------------------------
        return jsonify(
            {
                "success": True,

                "review": {
                    "summary": review_result.summary,
                    "source": review_result.source,

                    "issues": [
                        {
                            "severity": issue.severity,
                            "category": issue.category,
                            "message": issue.message,
                            "line": issue.line,
                            "suggestion": issue.suggestion,
                        }
                        for issue in review_result.issues
                    ],

                    "positive_points": review_result.positive_points,
                },

                "tutor": {
                    "explanation": tutor_result.explanation,
                    "hints": tutor_result.hints,
                    "concept": tutor_result.concept,
                    "next_step": tutor_result.next_step,
                },

                "fix": {
                    "success": fix_result.success,
                    "fixed_code": fix_result.fixed_code,
                    "explanation": fix_result.explanation,
                    "changes": fix_result.changes,
                },

                "verification": (
                    {
                        "success": verification_result.success,
                        "syntax_valid": verification_result.syntax_valid,
                        "runtime_success": verification_result.runtime_success,
                        "errors": verification_result.errors,
                        "details": verification_result.details,
                    }
                    if verification_result
                    else None
                ),
            }
        )

    except Exception:
        app.logger.exception(
            "Unexpected error while analyzing code."
        )

        return jsonify(
            {
                "success": False,
                "error": "Internal server error.",
            }
        ), 500


if __name__ == "__main__":
    debug_mode = os.getenv(
        "FLASK_DEBUG",
        "false",
    ).lower() == "true"

    app.run(
        debug=debug_mode,
    )