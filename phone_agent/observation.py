"""Post-action observation helpers."""

import base64
from dataclasses import dataclass
from io import BytesIO

from PIL import Image, ImageDraw


@dataclass
class ObservationSheet:
    base64_data: str
    width: int
    height: int


def build_contact_sheet(frames: list[tuple[object, str]]) -> ObservationSheet:
    if not frames:
        raise ValueError("At least one observation frame is required")

    decoded: list[tuple[Image.Image, str]] = []
    for screenshot, label in frames:
        raw = base64.b64decode(screenshot.base64_data)
        decoded.append((Image.open(BytesIO(raw)).convert("RGB"), label))

    frame_width = decoded[0][0].width
    frame_height = decoded[0][0].height
    sheet = Image.new("RGB", (frame_width * 2, frame_height * 2), color="white")
    draw = ImageDraw.Draw(sheet)

    for index, (image, label) in enumerate(decoded[:4]):
        resized = image.resize((frame_width, frame_height))
        x = (index % 2) * frame_width
        y = (index // 2) * frame_height
        sheet.paste(resized, (x, y))
        draw.rectangle((x, y, x + 74, y + 22), fill=(0, 0, 0))
        draw.text((x + 6, y + 5), label, fill=(255, 255, 255))

    buffer = BytesIO()
    sheet.save(buffer, format="PNG")
    return ObservationSheet(
        base64_data=base64.b64encode(buffer.getvalue()).decode("utf-8"),
        width=sheet.width,
        height=sheet.height,
    )
