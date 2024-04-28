from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, database, models
from .user import current_user

router = APIRouter(tags=["recommendations"])


@router.get("/recommendations", response_model=list[schemas.Anime])
async def get_recommendations(
    current_user: schemas.UserOut = Depends(current_user),
    db: Session = Depends(database.get_db),
):
    # Get user's preferred genres
    user_preferences = (
        db.query(models.Preference)
        .filter(models.Preference.user_id == current_user.id)
        .all()
    )
    preferred_genre_ids = [
        preference.genre_id for preference in user_preferences]

    # Get anime ids for the preferred genres
    anime_ids_for_genres = (
        db.query(models.GenreAnime.anime_id)
        .filter(models.GenreAnime.genre_id.in_(preferred_genre_ids))
        .all()
    )
    anime_ids_for_genres = [anime_id[0] for anime_id in anime_ids_for_genres]

    # Get recommended animes based on genre preferences and ratings
    recommendations = (
        db.query(models.Anime)
        .filter(models.Anime.id.in_(anime_ids_for_genres))
        .order_by(models.Anime.rating.desc())
        .limit(10)  # You can adjust the limit as per your requirement
        .all()
    )

    return recommendations
