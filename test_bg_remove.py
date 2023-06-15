import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import re


def is_russian(word):
    """Проверяем, что в строке только русские буквы"""
    return bool(re.match("^[А-Яа-яЁё ]+$", word))


def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


def fix_image(upload):
    image = Image.open(upload)
    st.write("Original Image :camera:")
    st.image(image)

    fixed = remove(image)
    st.write("Fixed Image :wrench:")
    st.image(fixed)
    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download fixed image", convert_image(fixed), "fixed.png", "image/png")


def test_is_russian():
    # Проверяем, что регулярное выражение работает корректно
    assert is_russian("") is True
    assert is_russian("Только русские буквы") is True
    assert is_russian("English letters only") is False
    assert is_russian("русские буквы и English") is False


def test_convert_image():
    # Тестирование функции конвертации изображения
    img = Image.new("RGB", (100, 100), color="red")
    byte_im = convert_image(img)
    assert byte_im[:8] == b"\x89PNG\r\n\x1a\n"


def test_fix_image():
    # Тестирование функции обработки изображения
    example_file = "./zebra.jpg"
    example_image = Image.open(example_file)
    buf = BytesIO()
    example_image.save(buf, format="PNG")
    example_png = buf.getvalue()

    # Тестирование, если изображение загружено
    with st.form(key="upload"):
        st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="uploader")
        st.form_submit_button("Submit")
    uploaded_file = st.session_state.uploader
    fix_image(upload=uploaded_file)

    # Тестирование, если изображение не загружено
    fix_image(example_file)
    downloaded_file = st._get_current_report()._widgets_by_id["sidebar"]._widgets[0]._prop_values["content"]._content.text
    assert example_png == downloaded_file
