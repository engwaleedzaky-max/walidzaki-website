from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import cloudinary
import cloudinary.api
import cloudinary.uploader
from flask import Flask, redirect, render_template, request, session, url_for

BASE_DIR = Path(__file__).resolve().parent
CONTENT_FILE = BASE_DIR / "data" / "site_content.json"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-this-secret-key")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "change-this-password")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")
CLOUDINARY_FOLDER = os.getenv("CLOUDINARY_FOLDER", "walid-portfolio-gallery")

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)

MAX_UPLOAD_MB = 10
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024


def read_json(file_path: Path, fallback: Any) -> Any:
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return fallback


def is_cloudinary_configured() -> bool:
    return all(
        [
            CLOUDINARY_CLOUD_NAME,
            CLOUDINARY_API_KEY,
            CLOUDINARY_API_SECRET,
        ]
    )


def list_gallery_images() -> list[dict[str, Any]]:
    if not is_cloudinary_configured():
        return []

    result = cloudinary.api.resources(
        type="upload",
        resource_type="image",
        prefix=f"{CLOUDINARY_FOLDER}/",
        max_results=100,
    )

    resources = result.get("resources", [])
    resources.sort(key=lambda item: item.get("created_at", ""), reverse=True)

    return [
        {
            "public_id": item.get("public_id", ""),
            "image_url": item.get("secure_url", ""),
            "created_at": item.get("created_at", ""),
            "label": item.get("display_name") or item.get("filename") or "Portfolio image",
        }
        for item in resources
    ]


def upload_images(files: list[Any]) -> None:
    for uploaded_file in files:
        if not uploaded_file or not uploaded_file.filename:
            continue

        if not uploaded_file.mimetype.startswith("image/"):
            raise ValueError("Only image files are allowed.")

        cloudinary.uploader.upload(
            uploaded_file,
            folder=CLOUDINARY_FOLDER,
            resource_type="image",
            use_filename=True,
            unique_filename=True,
            overwrite=False,
            filename_override=Path(uploaded_file.filename).stem,
        )


def admin_required() -> bool:
    return bool(session.get("is_admin"))


@app.context_processor
def inject_globals() -> dict[str, Any]:
    return {
        "is_admin": admin_required(),
    }


@app.route("/")
def home() -> str:
    content = read_json(CONTENT_FILE, {})
    gallery = list_gallery_images()
    if not gallery:
        gallery = read_json(CONTENT_FILE, {}).get("gallery", {}).get("default_items", [])
    lang = "ar" if request.args.get("lang") == "ar" else "en"

    return render_template(
        "home.html",
        content=content,
        gallery=gallery,
        lang=lang,
        cloudinary_ready=is_cloudinary_configured(),
        current_year=__import__("datetime").datetime.now().year,
    )


@app.route("/health")
def health() -> tuple[dict[str, bool], int]:
    return {"ok": True}, 200


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if admin_required():
        return redirect(url_for("admin_dashboard"))

    error = ""

    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_dashboard"))
        error = "Invalid password."

    return render_template("admin_login.html", error=error)


@app.route("/admin/logout", methods=["POST"])
def admin_logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/admin")
def admin_dashboard():
    if not admin_required():
        return redirect(url_for("admin_login"))

    content = read_json(CONTENT_FILE, {})
    gallery = list_gallery_images()

    return render_template(
        "admin_dashboard.html",
        content=content,
        gallery=gallery,
        cloudinary_ready=is_cloudinary_configured(),
        success=request.args.get("success", ""),
        error=request.args.get("error", ""),
    )


@app.route("/admin/gallery/upload", methods=["POST"])
def admin_gallery_upload():
    if not admin_required():
        return redirect(url_for("admin_login"))

    if not is_cloudinary_configured():
        return redirect(url_for("admin_dashboard", error="Cloudinary is not configured"))

    files = request.files.getlist("photos")
    valid_files = [file for file in files if file and file.filename]

    if not valid_files:
        return redirect(url_for("admin_dashboard", error="Please choose at least one image"))

    try:
        upload_images(valid_files)
        return redirect(url_for("admin_dashboard", success="Images uploaded successfully"))
    except ValueError as error:
        return redirect(url_for("admin_dashboard", error=str(error)))
    except Exception:
        return redirect(url_for("admin_dashboard", error="Upload failed"))


@app.route("/admin/gallery/delete", methods=["POST"])
def admin_gallery_delete():
    if not admin_required():
        return redirect(url_for("admin_login"))

    if not is_cloudinary_configured():
        return redirect(url_for("admin_dashboard", error="Cloudinary is not configured"))

    public_id = request.form.get("public_id", "").strip()
    if not public_id:
        return redirect(url_for("admin_dashboard", error="Missing image identifier"))

    try:
        cloudinary.uploader.destroy(public_id, resource_type="image")
        return redirect(url_for("admin_dashboard", success="Image deleted successfully"))
    except Exception:
        return redirect(url_for("admin_dashboard", error="Delete failed"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")), debug=True)
