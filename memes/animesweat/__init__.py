from pathlib import Path
from typing import List

from meme_generator import add_meme
from meme_generator.exception import MemeGeneratorException
from pil_utils import BuildImage

img_dir = Path(__file__).parent / "images"


def animesweat(images: List[BuildImage], texts, args):
    frame = images[0].convert("RGBA")
    droplet = BuildImage.open(img_dir / "0.png")

    import animeface

    faces = animeface.detect(frame.image)
    for face in faces:
        PROPORTION = 0.4
        max_width = face.face.pos.width * PROPORTION
        max_height = face.face.pos.height * PROPORTION
        ratio = max(max_width / droplet.width, max_height / droplet.height)
        droplet = droplet.resize(
            (int(droplet.width * ratio), int(droplet.height * ratio))
        )
        left_eye_x = face.left_eye.pos.x
        left_eye_y = face.left_eye.pos.y
        droplet_x = int(left_eye_x + face.left_eye.pos.width * 0.4)
        droplet_y = int(left_eye_y - face.left_eye.pos.height * 1.3)
        frame.paste(droplet, (droplet_x, droplet_y), alpha=True)
    if not faces:
        raise MemeGeneratorException("这张图片里面没有识别到任何脸，换一张试试？")

    return frame.save_png()


add_meme("animesweat", animesweat, min_images=1, max_images=1, keywords=["流汗"])
