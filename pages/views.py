from datetime import datetime

from django.conf import settings
from django.views.generic import TemplateView

from filmes.tmdb import trending_movies, now_playing_movies


class Home(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "IMG": settings.TMDB_IMAGE_BASE_URL,
                "trending_groups": self._get_trending_groups(),
                "now_playing": self._get_now_playing(),
            }
        )
        return context

    def _get_trending_groups(self):
        groups = []
        for key, label in (("day", "Hoje"), ("week", "Nesta semana")):
            try:
                payload = trending_movies(key)
                results = payload.get("results", [])
            except Exception:
                results = []
            movies = [self._map_movie(result) for result in results[:15]]
            groups.append({"key": key, "label": label, "movies": movies})
        return groups

    def _get_now_playing(self):
        try:
            payload = now_playing_movies()
            results = payload.get("results", [])
        except Exception:
            results = []
        return [self._map_movie(result) for result in results[:10]]

    def _map_movie(self, data):
        release_date = data.get("release_date") or ""
        return {
            "id": data.get("id"),
            "title": data.get("title") or data.get("name") or "",
            "poster_path": data.get("poster_path"),
            "backdrop_path": data.get("backdrop_path"),
            "score": self._score_from_vote(data.get("vote_average")),
            "vote_average": data.get("vote_average"),
            "release_date": release_date,
            "release_display": self._format_release_date(release_date),
        }

    def _score_from_vote(self, vote_average):
        if vote_average is None:
            return None
        try:
            return int(round(float(vote_average) * 10))
        except (TypeError, ValueError):
            return None

    def _format_release_date(self, value):
        if not value:
            return ""
        try:
            dt = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return value
        month_names = [
            "janeiro",
            "fevereiro",
            "março",
            "abril",
            "maio",
            "junho",
            "julho",
            "agosto",
            "setembro",
            "outubro",
            "novembro",
            "dezembro",
        ]
        month = month_names[dt.month - 1]
        return f"{dt.day:02d} de {month} de {dt.year}"


class About(TemplateView):
    template_name = "pages/about.html"
