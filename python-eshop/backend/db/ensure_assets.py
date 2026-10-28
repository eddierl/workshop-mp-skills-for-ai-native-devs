import logging
from pathlib import Path

PRODUCT_IMAGE_COUNT = 12

logger = logging.getLogger(__name__)


def products_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "static" / "images" / "products"


def missing_product_images() -> list[str]:
    directory = products_dir()
    return [
        f"{number}.png"
        for number in range(1, PRODUCT_IMAGE_COUNT + 1)
        if not (directory / f"{number}.png").is_file()
    ]


def ensure_product_images() -> None:
    """Check the product images that ship with the repo are present.

    Images are committed under backend/static, so startup never needs the
    network. If any are missing the catalog would show broken images, so say
    so loudly instead of failing silently.
    """
    missing = missing_product_images()
    if missing:
        logger.warning(
            "Missing product images in %s: %s. Restore them from git "
            "(git checkout -- python-eshop/backend/static).",
            products_dir(),
            ", ".join(missing),
        )
