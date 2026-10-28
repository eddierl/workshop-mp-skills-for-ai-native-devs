from pathlib import Path

PRODUCT_IMAGE_COUNT = 12

_PLACEHOLDER_SVG = """<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 400 400'>
  <rect width='400' height='400' fill='#6366f1'/>
  <text x='200' y='210' font-family='Inter,Arial,sans-serif' font-size='48' fill='white' text-anchor='middle'>#{number}</text>
</svg>
"""


def _products_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "static" / "images" / "products"


def _write_placeholder_svg(products_dir: Path, number: int) -> None:
    target = products_dir / f"{number}.svg"
    if target.is_file():
        return
    target.write_text(_PLACEHOLDER_SVG.format(number=number), encoding="utf-8")


def ensure_product_images(products_dir: Path | None = None) -> None:
    """Ensure SVG placeholders exist for every catalog product image."""
    target_dir = products_dir or _products_dir()
    target_dir.mkdir(parents=True, exist_ok=True)

    for number in range(1, PRODUCT_IMAGE_COUNT + 1):
        _write_placeholder_svg(target_dir, number)
