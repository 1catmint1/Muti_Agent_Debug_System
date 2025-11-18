# data/image_manager.py
import os
from config import CUSTOM_IMAGE_DIR

class ImageManager:
    def __init__(self):
        self.library = {
            "自然风光": {
                "scenery_001": {
                    "path": "assets/nature/scenery_001.jpg",
                    "thumbnail": "assets/nature/thumb_scenery_001.png"
                }
            },
            "自定义": {}
        }
        self.load_custom_images()

    def load_custom_images(self):
        if not os.path.exists(CUSTOM_IMAGE_DIR):
            os.makedirs(CUSTOM_IMAGE_DIR)
            return

        for file in os.listdir(CUSTOM_IMAGE_DIR):
            if file.lower().endswith(('jpg', 'jpeg', 'png', 'bmp')):
                name = os.path.splitext(file)[0]
                key = f"custom_{name}"
                self.library["自定义"][key] = {
                    "path": os.path.join(CUSTOM_IMAGE_DIR, file),
                    "thumbnail": os.path.join(CUSTOM_IMAGE_DIR, f"thumb_{file}")
                }

    def get_categories(self):
        return list(self.library.keys())

    def get_images_in_category(self, category):
        return self.library.get(category, {})