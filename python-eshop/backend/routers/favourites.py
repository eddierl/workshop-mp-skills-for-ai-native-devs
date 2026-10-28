"""API endpoints for the Favourites feature (ticket #2).

POST /api/favourites/{catalog_item_id} — add a favourite
GET  /api/favourites — list user's favourites
DELETE /api/favourites/{catalog_item_id} — remove a favourite
"""
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import FavouriteService, get_favourite_service, require_authenticated_user
from models.schemas import FavouriteResponse

router = APIRouter(prefix="/api/favourites", tags=["favourites"])


@router.post("/{catalog_item_id}", response_model=FavouriteResponse, status_code=status.HTTP_201_CREATED)
def add_favourite(
    catalog_item_id: int,
    user_email: str = Depends(require_authenticated_user),
    service: FavouriteService = Depends(get_favourite_service),
) -> FavouriteResponse:
    """Add a product to the user's favourites."""
    try:
        user = service.db.get_user_by_email(user_email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return service.add_favourite(user.id, catalog_item_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except Exception as exc:
        if "UNIQUE" in str(exc) or "constraint" in str(exc).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already in favourites",
            )
        raise


@router.get("", response_model=list[FavouriteResponse])
def get_favourites(
    user_email: str = Depends(require_authenticated_user),
    service: FavouriteService = Depends(get_favourite_service),
) -> list[FavouriteResponse]:
    """List the current user's favourites."""
    user = service.db.get_user_by_email(user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return service.get_favourites(user.id)


@router.delete("/{catalog_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favourite(
    catalog_item_id: int,
    user_email: str = Depends(require_authenticated_user),
    service: FavouriteService = Depends(get_favourite_service),
) -> None:
    """Remove a product from the user's favourites."""
    user = service.db.get_user_by_email(user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    fav = service.get_favourite(user.id, catalog_item_id)
    if fav is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not a favourite",
        )
    service.remove_favourite(user.id, catalog_item_id)
