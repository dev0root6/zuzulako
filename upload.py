import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file provided"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "Filename is empty"
        }), 400

    original_name = secure_filename(file.filename)

    message = request.form.get("message", "").strip()
    os_name = request.form.get("os_name", "Unknown").strip()

    message = secure_filename(message) if message else uuid.uuid4().hex
    os_name = secure_filename(os_name)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    _, extension = os.path.splitext(original_name)

    new_filename = f"{message}_{os_name}_{timestamp}{extension}"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], new_filename)
    file.save(filepath)

    return jsonify({
        "success": True,
        "saved_as": new_filename,
        "original_filename": original_name,
        "os_name": os_name,
        "message": request.form.get("message", ""),
        "size": os.path.getsize(filepath),
        "uploaded_at": timestamp
    }), 200
