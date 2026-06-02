from typing import List, Tuple

from .integration_activity import MIN_SCORE

Detection = Tuple[Tuple[int, int, int, int], float, int]

class_names = {0: 'duckie', 1: 'truck', 2: 'sign'}

Y_STOP_RATIO = 0.45
AREA_RATIO_THRESHOLD = 0.01
CENTER_TOLERANCE = 0.35


def should_stop(detections: List[Detection], img_w: int, img_h: int) -> Tuple[bool, str]:
    """
    Stop when a confident object is low in the frame, large enough, and near center.

    Bboxes are in full-frame pixels; ``img_w`` / ``img_h`` must match that frame.
    """
    if img_w <= 0 or img_h <= 0:
        return False, ''

    img_area = float(img_w * img_h)
    center_x = img_w * 0.5
    y_close = img_h * Y_STOP_RATIO

    for bbox, score, pred_class in detections:
        if score < MIN_SCORE:
            continue

        xmin, ymin, xmax, ymax = bbox
        width = xmax - xmin
        height = ymax - ymin
        area = float(width * height)

        if ymax < y_close:
            continue

        if area < AREA_RATIO_THRESHOLD * img_area:
            continue

        box_center_x = (xmin + xmax) * 0.5
        normalized_offset = abs(box_center_x - center_x) / max(float(img_w), 1.0)

        if normalized_offset > CENTER_TOLERANCE:
            continue

        return True, (
            f"stop: {class_names[pred_class]} "
            f"score={score:.2f}, area={int(area)}, y2={ymax}"
        )

    return False, ""
