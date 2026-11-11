
from flask import Flask, render_template, request
from main import simplify_uploaded_report

app = Flask(__name__)

# Maximum upload size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}


@app.route("/", methods=["GET", "POST"])
def home():

    explanation = None
    error = None

    if request.method == "POST":

        uploaded_file = request.files.get("report")
        language = request.form.get("language", "Both")

        if not uploaded_file or not uploaded_file.filename:
            error = "Please select a report first."

        else:
            filename = uploaded_file.filename.lower()
            extension = "." + filename.rsplit(".", 1)[-1]

            if extension not in ALLOWED_EXTENSIONS:
                error = "Please upload a PDF, JPG, JPEG, or PNG file."

            else:
                try:
                    file_bytes = uploaded_file.read()

                    explanation = simplify_uploaded_report(
                        file_bytes,
                        extension,
                        language
                    )

                except Exception as e:

                    error_message = str(e)

                    if (
                        "429" in error_message
                        or "RESOURCE_EXHAUSTED" in error_message
                    ):
                        error = (
                            "Our AI service is temporarily busy. "
                            "Please wait 60 seconds and try again."
                        )

                    else:
                        print("Application error:", error_message)

                        error = (
                            "Something went wrong while processing "
                            "your report. Please try again."
                        )

    return render_template(
        "index.html",
        explanation=explanation,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
