import os

from main.forms import BookCreateForm
from main import app


def change_file_name(form: BookCreateForm, filename:str) -> str:
    title = form.title.data.split(' ')
    name = '_'.join(title) + '.' + filename.rsplit('.', 1)[1]
    return name


def upload_file(form: BookCreateForm):
    file = form.file.data
    if file:
        file_name = change_file_name(form, file.filename)
        file.save(os.path.join(app.config['UPLOAD_FILE_FOLDER'], file_name))
        file_path = file_name
        return file_path
    return None


def upload_image(form: BookCreateForm):
    image = form.image.data
    if image:
        image_name = change_file_name(form, image.filename)
        image.save(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], image_name))
        image_path = os.path.join('/static/images/', image_name)
        return image_path
    return None
