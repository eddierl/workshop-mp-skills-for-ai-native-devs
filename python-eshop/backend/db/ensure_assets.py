from pathlib import Path

PRODUCT_IMAGE_COUNT = 12
GITHUB_BASE = (
    "https://raw.githubusercontent.com/dotnet-architecture/eShopOnWeb/main"
    "/src/Web/wwwroot/images/products"
)


def _products_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "static" / "images" / "products"


def _missing_image_numbers(products_dir: Path) -> list[int]:
    return [
        number
        for number in range(1, PRODUCT_IMAGE_COUNT + 1)
        if not (products_dir / f"{number}.png").is_file()
    ]


def _download_from_github(products_dir: Path, missing: list[int]) -> None:
    try:
        import urllib.request
    except ImportError:
        return

    for number in missing:
        url = f"{GITHUB_BASE}/{number}.png"
        target = products_dir / f"{number}.png"
        try:
            urllib.request.urlretrieve(url, target)
        except OSError:
            continue


def ensure_product_images() -> None:
    """Ensure product PNGs exist under backend/static (self-contained app)."""
    products_dir = _products_dir()
    products_dir.mkdir(parents=True, exist_ok=True)

    missing = _missing_image_numbers(products_dir)
    if missing:
        _download_from_github(products_dir, missing)
