import json
from requests import post
from ratelimiter import RateLimiter

# 初始化变量
all_games = []
rate_limiter = RateLimiter(max_calls=4, period=1)  # 每秒最多 4 次请求


url = "https://api.igdb.com/v4/games"
headers = {}



# 限速执行 API 请求
for i in range(10):
    offset = i*500
    limit = 500
    data = f"""
    fields age_ratings.*,age_ratings.content_descriptions.category,aggregated_rating,
        aggregated_rating_count,alternative_names,bundles,category,collection,dlcs,expanded_games,
        expansions,first_release_date,follows,forks,franchise,game_engines,game_modes,genres,hypes,
        involved_companies.*,keywords,multiplayer_modes,name,parent_game,platforms,player_perspectives,
        ports,rating,rating_count,remakes,remasters,similar_games,slug,standalone_expansions,status,
        tags,themes,total_rating,total_rating_count,updated_at,url,version_parent,version_title,
        websites,game_localizations.region,language_supports.language,
        language_supports.language_support_type,multiplayer_modes.*;
    sort total_rating_count desc;
    limit {limit};
    offset {offset};
    """

    with rate_limiter:
        response = post(url, headers=headers, data=data)  # 发送 POST 请求
        response.raise_for_status()  # 检查是否返回错误
        records = response.json()

    print(f"finish {i+1}")

    # 如果没有数据，跳出循环
    # if not records:
    #     break

    # 将获取的数据添加到 all_games 列表
    all_games.extend(records)
    offset += limit

# 保存数据到本地 JSON 文件
output_path = "all_games_5000.json"
with open(output_path, 'w') as f:
    json.dump(all_games, f, indent=4)  # 格式化输出 JSON 文件

print(f"数据已成功保存到 {output_path}")
