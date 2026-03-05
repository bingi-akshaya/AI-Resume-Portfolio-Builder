try:
    import qrcode
except ImportError:
    qrcode = None

import os


def create_qr(data, filename):
    """Generate a QR code image for the given data and save it to filename.

    If the ``qrcode`` module is not available the function returns ``None``
    and skips generation so the rest of the app can continue normally.
    """
    if qrcode is None:
        return None

    img = qrcode.make(data)
    # ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)
    return filename
