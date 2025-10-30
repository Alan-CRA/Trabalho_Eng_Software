from django.shortcuts import render,redirect
from .models import Filme,Genero,Ator,Streaming
from .service import TmdbApiService
# Create your views here.
def lista_filmes(request):
    query = request.GET.get('q')
    api = TmdbApiService()
    filmes_dict = api.get_movies_by_name(query)
    lista=filmes_dict["results"]

    for i in lista:
        tmdb_id=i['id']
        if not Filme.objects.filter(id=tmdb_id).exists():
            filme_obj, criado = Filme.objects.update_or_create(
                    id=tmdb_id,
                    defaults={
                        'nome': i['title'],
                        'sinopse': i.get('overview'),
                        'nota_media': i.get('vote_average', 0.0),
                        'lancamento': i.get('release_date',"1111-11-11"),
                    }
                )
            
            generos_filme = i.get('genre_ids', [])
            for genero_id in generos_filme:
                if not Genero.objects.filter(id=genero_id):
                    generos_api=api.get_genres()
                    lista = generos_api["genres"]
                    for j in lista:
                        if genero_id == j["id"]:
                            genero_obj, criado = Genero.objects.update_or_create(
                                        id = j["id"],
                                        nome = j["name"],
                                    )
            filme_obj.generos.set(generos_filme)

            atores_api=api.get_movies_credit(tmdb_id)
            atores = atores_api.get('cast', [])[:5]
            ids_atores = [] 
            for ator_data in atores:
                ator_obj, _ = Ator.objects.update_or_create(
                    id=ator_data["id"],
                    nome = ator_data["name"],
                )
                ids_atores.append(ator_obj.id)
            filme_obj.atores.set(ids_atores)

            providers_api = api.get_movies_providers(tmdb_id)
            providers = providers_api.get('results', {})
            streamings_br = providers.get('BR', {}).get('flatrate', [])
            ids_streamings = []
            for provider_data in streamings_br:
                streaming_obj, _ = Streaming.objects.update_or_create(
                    id = provider_data["provider_id"],
                    nome = provider_data["provider_name"],
                )
                ids_streamings.append(streaming_obj.id)
                
            filme_obj.streaming.set(ids_streamings)
                
    context={
        "filmes" : Filme.objects.all()
    }
    return render(request,'filmes/lista_filmes.html',context)