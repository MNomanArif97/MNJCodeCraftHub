from datetime import datetime
from pathlib import Path
import json

from flask import Flask, jsonify, request


# Create the Flask application
app = Flask(__name__)


# Store courses.json in the same folder as this app.py file
DATA_FILE = Path(__file__).resolve().parent / "courses.json"


# These are the only valid course status values
VALID_STATUSES = {
    "Not Started",
    "In Progress",
    "Completed"
}


# Required fields when creating or replacing a course
REQUIRED_FIELDS = {
    "name",
    "description",
    "target_date",
    "status"
}


class StorageError(Exception):
    """
    Custom exception used when courses.json cannot be read or written.
    """
    pass


def ensure_data_file():
    """
    Create courses.json automatically if it does not already exist.

    The file starts with an empty JSON list because courses will be stored
    as a list of dictionaries.
    """
    try:
        if not DATA_FILE.exists():
            DATA_FILE.write_text("[]", encoding="utf-8")
    except OSError as error:
        raise StorageError(
            f"Unable to create the data file: {error}"
        ) from error


def load_courses():
    """
    Read and return all courses from courses.json.

    Returns:
        list: A list of course dictionaries.

    Raises:
        StorageError: If the file cannot be read or contains invalid JSON.
    """
    ensure_data_file()

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            courses = json.load(file)

    except OSError as error:
        raise StorageError(
            f"Unable to read courses.json: {error}"
        ) from error

    except json.JSONDecodeError as error:
        raise StorageError(
            f"courses.json contains invalid JSON: {error}"
        ) from error

    # Make sure the JSON file contains a list
    if not isinstance(courses, list):
        raise StorageError(
            "courses.json must contain a JSON list."
        )

    return courses


def save_courses(courses):
    """
    Save all courses to courses.json.

    Args:
        courses (list): The list of course dictionaries.

    Raises:
        StorageError: If the file cannot be written.
    """
    ensure_data_file()

    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(courses, file, indent=4)

    except OSError as error:
        raise StorageError(
            f"Unable to write to courses.json: {error}"
        ) from error


def get_current_timestamp():
    """
    Return the current UTC time as an ISO 8601 string.

    Example:
        2026-10-20T15:30:45.123456+00:00
    """
    return datetime.now().astimezone().isoformat()


def validate_course_data(data, require_all_fields=True):
    """
    Validate course data received from an API request.

    Args:
        data (dict): Request JSON data.
        require_all_fields (bool): If True, all course fields are required.
            This is used for POST and PUT requests.

    Returns:
        str or None: An error message if validation fails, otherwise None.
    """
    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    if require_all_fields:
        missing_fields = REQUIRED_FIELDS - set(data.keys())

        if missing_fields:
            fields = ", ".join(sorted(missing_fields))
            return f"Missing required field(s): {fields}"
    else:
        # Used if partial validation is needed in the future
        if not data:
            return "Request body cannot be empty."

    # Validate the name field
    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return "name is required and must be a non-empty string."

    # Validate the description field
    if "description" in data:
        if (
            not isinstance(data["description"], str)
            or not data["description"].strip()
        ):
            return (
                "description is required and must be a non-empty string."
            )

    # Validate the target_date field
    if "target_date" in data:
        target_date = data["target_date"]

        if not isinstance(target_date, str):
            return "target_date must be a string in YYYY-MM-DD format."

        try:
            # This checks both the format and whether the date is valid.
            # For example, 2026-02-30 will be rejected.
            datetime.strptime(target_date, "%Y-%m-%d")
        except ValueError:
            return "target_date must use YYYY-MM-DD format."

    # Validate the status field
    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            valid_values = ", ".join(sorted(VALID_STATUSES))
            return (
                f"status must be one of: {valid_values}."
            )

    return None


def find_course(courses, course_id):
    """
    Find one course by its ID.

    Returns:
        dict or None: The matching course, if found.
    """
    return next(
        (
            course
            for course in courses
            if course.get("id") == course_id
        ),
        None
    )


def get_next_course_id(courses):
    """
    Generate the next course ID.

    The first course receives ID 1. After that, the next ID is one greater
    than the current highest ID.
    """
    if not courses:
        return 1

    highest_id = max(
        course.get("id", 0)
        for course in courses
    )

    return highest_id + 1


@app.errorhandler(StorageError)
def handle_storage_error(error):
    """
    Return a helpful response when courses.json cannot be used.
    """
    return jsonify({
        "error": str(error)
    }), 500


@app.errorhandler(404)
def handle_not_found(error):
    """
    Handle URLs that do not exist.
    """
    return jsonify({
        "error": "The requested endpoint was not found."
    }), 404


@app.errorhandler(500)
def handle_internal_error(error):
    """
    Handle unexpected server errors.

    The real error should be investigated in the server console.
    """
    return jsonify({
        "error": "An unexpected internal server error occurred."
    }), 500


@app.route("/api/courses", methods=["POST"])
@app.route("/api/courses/", methods=["POST"])
def create_course():
    """
    POST /api/courses

    Add a new course.
    """
    # silent=True prevents Flask from raising an exception for malformed JSON
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Request body must contain valid JSON."
        }), 400

    validation_error = validate_course_data(
        data,
        require_all_fields=True
    )

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    courses = load_courses()

    new_course = {
        "id": get_next_course_id(courses),
        "name": data["name"].strip(),
        "description": data["description"].strip(),
        "target_date": data["target_date"],
        "status": data["status"],
        "created_at": get_current_timestamp()
    }

    courses.append(new_course)
    save_courses(courses)

    return jsonify(new_course), 201


@app.route("/api/courses", methods=["GET"])
@app.route("/api/courses/", methods=["GET"])
def get_all_courses():
    """
    GET /api/courses

    Return all courses.
    """
    courses = load_courses()

    return jsonify(courses), 200


@app.route("/api/courses/<int:course_id>", methods=["GET"])
@app.route("/api/courses/<int:course_id>/", methods=["GET"])
def get_single_course(course_id):
    """
    GET /api/courses/<course_id>

    Return one course by ID.
    """
    courses = load_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with ID {course_id} was not found."
        }), 404

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["PUT"])
@app.route("/api/courses/<int:course_id>/", methods=["PUT"])
def update_course(course_id):
    """
    PUT /api/courses/<course_id>

    Replace all editable information for an existing course.

    PUT requires:
    - name
    - description
    - target_date
    - status

    The existing ID and created_at timestamp are preserved.
    """
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Request body must contain valid JSON."
        }), 400

    validation_error = validate_course_data(
        data,
        require_all_fields=True
    )

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    courses = load_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with ID {course_id} was not found."
        }), 404

    # Update only the editable course fields
    course["name"] = data["name"].strip()
    course["description"] = data["description"].strip()
    course["target_date"] = data["target_date"]
    course["status"] = data["status"]

    # ID and created_at remain unchanged
    save_courses(courses)

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    """
    DELETE /api/courses/<course_id>

    Delete a course by ID.
    """
    courses = load_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with ID {course_id} was not found."
        }), 404

    # Create a new list without the course being deleted
    remaining_courses = [
        existing_course
        for existing_course in courses
        if existing_course.get("id") != course_id
    ]

    save_courses(remaining_courses)

    return jsonify({
        "message": f"Course with ID {course_id} was deleted successfully."
    }), 200


if __name__ == "__main__":
    # Create courses.json before starting the development server
    ensure_data_file()

    print("CodeCraftHub API is running.")
    print("Courses file:", DATA_FILE)
    print("API URL: http://127.0.0.1:5000")

    # debug=True is useful during development.
    # Do not use debug=True in production.
    app.run(debug=True)