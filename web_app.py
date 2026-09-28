import os

from flask import Flask, render_template, request
import requests

from main import get_random_cat_image_url, get_random_dog_image_url

app = Flask(__name__)

PET_CONFIG = {
    "dog": {
        "title": "Случайная собачка",
        "alt": "Случайная собачка",
        "error": "Не удалось получить изображение собаки. Попробуйте ещё раз.",
    },
    "cat": {
        "title": "Случайный котик (мяу)",
        "alt": "Случайный котик",
        "error": "Не удалось получить изображение котика. Попробуйте ещё раз.",
    },
}


@app.route("/")
def index():
    pet = request.args.get("pet")

    if pet not in PET_CONFIG:
        pet = None

    image_url = None
    error_message = None
    page_title = "Кого покажем?"
    image_alt = None

    if pet is not None:
        try:
            if pet == "cat":
                image_url = get_random_cat_image_url()
            else:
                image_url = get_random_dog_image_url()
        except (requests.exceptions.RequestException, ValueError):
            error_message = "API временно недоступен. Попробуйте обновить страницу чуть позже."

        pet_config = PET_CONFIG[pet]
        page_title = pet_config["title"]
        image_alt = pet_config["alt"]

        if not image_url and error_message is None:
            error_message = pet_config["error"]

    return render_template(
        "index.html",
        image_url=image_url,
        selected_pet=pet,
        title=page_title,
        image_alt=image_alt,
        error_message=error_message,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
