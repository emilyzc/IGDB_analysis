import json
from requests import post
from ratelimiter import RateLimiter

headers = {
    'Client-ID': '',
    'Authorization': '',
}
Path = ''


all_games = []
rate_limiter = RateLimiter(max_calls=4, period=1)
offset = 0
limit = 500

while True: 
    data = f"""
    fields age_ratings.*,age_ratings.content_descriptions.category,aggregated_rating,
        aggregated_rating_count,alternative_names,bundles,category,collection,dlcs,expanded_games,
        expansions,first_release_date,follows,forks,franchise,game_engines,game_modes,genres,hypes,
        involved_companies.*,keywords,multiplayer_modes,name,parent_game,platforms,player_perspectives,
        ports,rating,rating_count,remakes,remasters,similar_games,slug,standalone_expansions,status,
        tags,themes,total_rating,total_rating_count,updated_at,url,version_parent,version_title,
        websites,game_localizations.region,language_supports.language,
        language_supports.language_support_type,multiplayer_modes.*;
    where platforms = (6);
    sort total_rating_count desc;
    limit {limit};
    offset {offset};
    """

    with rate_limiter:
        response = post('https://api.igdb.com/v4/games', headers=headers, data=data)
        records = response.json()

    if not records:
        break
    else:
        all_games.extend(records)
        offset += limit

# Save the records to a file.
with open(Path, 'w') as f:
    json.dump(all_games, f)