import os
import uuid
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import threading
import generate_process as gp

UPLOAD_FOLDER = "user_uploads"
STATIC_REELS = "static/reels"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_REELS, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    myid = str(uuid.uuid1())

    if request.method == "POST":
        rec_id = request.form.get("uuid") or myid
        desc = request.form.get("text", "")
        folder_path = os.path.join(app.config["UPLOAD_FOLDER"], rec_id)
        os.makedirs(folder_path, exist_ok=True)

        input_files = []

        # Save images
        for key, file in request.files.items():
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(folder_path, filename)
                file.save(save_path)
                input_files.append(filename)

        # Save description
        with open(os.path.join(folder_path, "desc.txt"), "w", encoding="utf-8") as f:
            f.write(desc)

        # Create input.txt (clean UTF-8 + UNIX endings)
        input_txt_path = os.path.join(folder_path, "input.txt")
        with open(input_txt_path, "w", encoding="utf-8", newline="\n") as f:
            for img in input_files:
                f.write(f"file '{img}'\n")
                f.write("duration 1\n")

    return render_template("create.html", myid=myid)


@app.route("/gallery")
def gallery():
    reels = [
        r for r in os.listdir(STATIC_REELS)
        if r.endswith(".mp4")
    ]
    return render_template("gallery.html", reels=reels)


def start_worker():
    thread = threading.Thread(target=gp.start_processing, daemon=True)
    thread.start()


if __name__ == "__main__":
    start_worker()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
