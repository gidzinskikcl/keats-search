import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_static_file_serving_tmpfile():
    # Match the thumbnail directory in main.py
    thumbnail_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "thumbnails")
    )
    os.makedirs(thumbnail_dir, exist_ok=True)

    test_filename = "985c567f01d3ad47d737c3b33eb678ea_MIT18_404f20_lec21_thumbnail.jpg"
    test_file_path = os.path.join(thumbnail_dir, test_filename)

    # Create a minimal fake JPEG file
    with open(test_file_path, "wb") as f:
        f.write(b"\xff\xd8\xff\xe0" + b"\x00" * 128)  # JPEG header + padding

    try:
        # Make request to static file route
        response = client.get(f"/thumbnails/{test_filename}")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("image/")
    finally:
        # Clean up the test file
        os.remove(test_file_path)
