import qrcode
from io import BytesIO


def generate_qr_code(shortened_url):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=15, border=4)
    qr.add_data(shortened_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_bytes = BytesIO()
    img.save('qrcode.png')
    img_bytes.seek(0)
    return img_bytes 