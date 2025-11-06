from django.shortcuts import render, redirect
from django.views import View
from django.db import transaction
from django.contrib import messages
from django.conf import settings
from .models import Filme, Genero, Ator, Streaming
from .tmdb import search_movie, movie_details, movie_credits, watch_providers

def _ensure_genres(genres):
    objs = []
    for g in genres or []:
        obj, _ = Genero.objects.get_or_create(nome=g.get("name","").strip()[:120])
        objs.append(obj)
    return objs

def _ensure_cast(cast):
    objs = []
    for a in (cast or [])[:20]:
        name = a.get("name","").strip()
        if not name: continue
        obj, _ = Ator.objects.get_or_create(nome=name[:200])
        objs.append(obj)
    return objs

def _providers_to_streaming(providers):
    objs = []
    names = set()
    for region, data in (providers or {}).get("results", {}).items():
        flatrate = data.get("flatrate") or []
        for s in flatrate:
            nm = s.get("provider_name")
            if not nm or nm in names: continue
            names.add(nm)
            obj, _ = Streaming.objects.get_or_create(nome=nm[:200])
            objs.append(obj)
    return objs

@transaction.atomic
def _upsert_movie_from_tmdb(tmdb_id:int):
    det = movie_details(tmdb_id)
    credits = movie_credits(tmdb_id)
    providers = watch_providers(tmdb_id)

    filme, _ = Filme.objects.update_or_create(
        tmdb_id=det["id"],
        defaults={
            "nome": det.get("title") or det.get("name") or "",
            "lancamento": det.get("release_date") or "",
            "tempo": det.get("runtime") or None,
            "sinopse": det.get("overview") or "",
            "nota_media": det.get("vote_average") or None,
            "poster_path": det.get("poster_path") or None,
            "backdrop_path": det.get("backdrop_path") or None,
        }
    )

    filme.genero.set(_ensure_genres(det.get("genres", [])))
    filme.atores.set(_ensure_cast((credits or {}).get("cast", [])))
    filme.streaming.set(_providers_to_streaming(providers))
    return filme

class ListaFilmes(View):
    template_name = "filmes/lista_filmes.html"

    def get(self, request):
        q = request.GET.get("q","").strip()
        filmes = []
        if q:
            data = search_movie(q)
            results = data.get("results", [])
            for r in results:
                tmdb_id = r["id"]
                f, _ = Filme.objects.update_or_create(
                    tmdb_id=tmdb_id,
                    defaults={
                        "nome": r.get("title") or "",
                        "lancamento": r.get("release_date") or "",
                        "nota_media": r.get("vote_average") or None,
                        "poster_path": r.get("poster_path") or None,
                    }
                )
                filmes.append(f)
        ctx = {"filmes": filmes, "IMG": settings.TMDB_IMAGE_BASE_URL}
        return render(request, self.template_name, ctx)

class Detalhes(View):
    template_name = "filmes/detalhes.html"

    def get(self, request):
        tmdb_id = request.GET.get("id")
        if not tmdb_id:
            messages.error(request, "ID do filme não informado.")
            return redirect("pages:home")
        try:
            tmdb_id = int(tmdb_id)
        except ValueError:
            messages.error(request, "ID inválido.")
            return redirect("pages:home")

        filme = Filme.objects.filter(tmdb_id=tmdb_id).first()
        if not filme or not (filme.sinopse and filme.tempo):
            filme = _upsert_movie_from_tmdb(tmdb_id)

        return render(request, self.template_name, {"filme": filme, "IMG": settings.TMDB_IMAGE_BASE_URL})
