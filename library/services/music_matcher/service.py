from datetime import date

from asgiref.sync import sync_to_async

from library.models import (
    Album,
    DiscogsMarketplaceListing,
    UserAlbum,
)
from library.services.discogs.factory import create_discogs_service
from library.services.spotify.factory import create_spotify_service


class MusicService:
    def __init__(
        self,
        spotify_service=None,
        discogs_service=None,
    ):
        self.spotify_service = spotify_service or create_spotify_service()

        self.discogs_service = discogs_service or create_discogs_service()

    async def get_users_music(
        self,
        user,
        access_token,
    ):
        spotify_albums = await self.spotify_service.get_saved_albums(access_token)

        results = []

        for spotify_album in spotify_albums:
            album = await self._save_album(
                user,
                spotify_album,
            )

            if album is None:
                continue

            marketplace_listings = await self.discogs_service.search_marketplace(album)
            album_listings = await self._save_listings(
                album,
                marketplace_listings,
            )

            if album_listings:
                results.append(
                    {
                        "album": album,
                        "listings": album_listings,
                    }
                )

        return results

    @sync_to_async
    def _save_album(
        self,
        user,
        spotify_saved_album,
    ):
        spotify_album = spotify_saved_album.album

        title = spotify_album.name
        artist = spotify_album.artists[0].name

        if len(title) > 200:
            print(
                f"Skipping album with excessively long title: {len(title)} characters"
            )
            return None

        if len(artist) > 200:
            print(
                f"Skipping album with excessively long artist: {len(artist)} characters"
            )
            return None

        artwork = ""

        if spotify_album.images:
            artwork = spotify_album.images[0].url

        album, _ = Album.objects.update_or_create(
            spotify_id=spotify_album.id,
            defaults={
                "title": title,
                "artist": artist,
                "release_date": self._parse_release_date(spotify_album),
                "artwork": artwork,
            },
        )

        UserAlbum.objects.get_or_create(
            user=user,
            album=album,
        )

        return album

    @sync_to_async
    def _save_listings(
        self,
        album,
        marketplace_listings,
    ):
        listings = []

        for marketplace_listing in marketplace_listings:
            if not marketplace_listing.listing_id:
                continue

            listing, _ = DiscogsMarketplaceListing.objects.update_or_create(
                listing_id=marketplace_listing.listing_id,
                defaults={
                    "album": album,
                    "title": marketplace_listing.title,
                    "price": marketplace_listing.price,
                    "currency": marketplace_listing.currency,
                    "listing_url": marketplace_listing.listing_url,
                    "seller_country": (marketplace_listing.seller_country),
                    "media_condition": (marketplace_listing.media_condition),
                    "sleeve_condition": (marketplace_listing.sleeve_condition),
                    "seller_rating": (marketplace_listing.seller_rating),
                },
            )

            listings.append(listing)

        return listings

    @staticmethod
    def _parse_release_date(
        spotify_album,
    ):
        release_date = spotify_album.release_date

        if spotify_album.release_date_precision == "year":
            return date(
                int(release_date),
                1,
                1,
            )

        if spotify_album.release_date_precision == "month":
            year, month = release_date.split("-")

            return date(
                int(year),
                int(month),
                1,
            )

        return date.fromisoformat(release_date)
