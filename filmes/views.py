from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db import transaction
from django.db.models import Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from .models import Filme, Genero, Ator, Streaming, Avaliacao
from .forms import AvaliacaoForm
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

        # Avaliação do usuário atual
        avaliacao_usuario = None
        if request.user.is_authenticated:
            avaliacao_usuario = Avaliacao.objects.filter(
                user=request.user, filme=filme
            ).first()

        # Todas as avaliações do filme
        avaliacoes = Avaliacao.objects.filter(filme=filme).select_related('user').order_by('-criado_em')
        
        # Média das avaliações dos usuários
        media_avaliacoes = avaliacoes.aggregate(media=Avg('nota'))['media']
        total_avaliacoes = avaliacoes.count()

        # Formulário de avaliação
        form = AvaliacaoForm(instance=avaliacao_usuario) if avaliacao_usuario else AvaliacaoForm()

        ctx = {
            "filme": filme,
            "IMG": settings.TMDB_IMAGE_BASE_URL,
            "form": form,
            "avaliacao_usuario": avaliacao_usuario,
            "avaliacoes": avaliacoes[:10],  # Limita a 10 avaliações
            "media_avaliacoes": media_avaliacoes,
            "total_avaliacoes": total_avaliacoes,
        }
        return render(request, self.template_name, ctx)


@login_required(login_url="contas:entrar")
def avaliar_filme(request, filme_id):
    """View para avaliar ou atualizar avaliação de um filme."""
    filme = get_object_or_404(Filme, id=filme_id)
    
    if request.method == "POST":
        # Verifica se já existe avaliação
        avaliacao_existente = Avaliacao.objects.filter(
            user=request.user, filme=filme
        ).first()
        
        form = AvaliacaoForm(request.POST, instance=avaliacao_existente)
        
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.user = request.user
            avaliacao.filme = filme
            avaliacao.save()
            
            if avaliacao_existente:
                messages.success(request, f"Sua avaliação de '{filme.nome}' foi atualizada!")
            else:
                messages.success(request, f"Você avaliou '{filme.nome}' com nota {avaliacao.nota}!")
            
            return redirect(f"/filmes/detalhes?id={filme.tmdb_id}")
        else:
            messages.error(request, "Erro ao salvar avaliação. Verifique os dados.")
    
    return redirect(f"/filmes/detalhes?id={filme.tmdb_id}")


@login_required(login_url="contas:entrar")
def excluir_avaliacao(request, filme_id):
    """View para excluir avaliação de um filme."""
    filme = get_object_or_404(Filme, id=filme_id)
    
    avaliacao = Avaliacao.objects.filter(user=request.user, filme=filme).first()
    if avaliacao:
        avaliacao.delete()
        messages.success(request, f"Sua avaliação de '{filme.nome}' foi removida.")
    
    return redirect(f"/filmes/detalhes?id={filme.tmdb_id}")

