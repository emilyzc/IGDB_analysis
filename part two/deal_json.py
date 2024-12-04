import json
import csv

# 读取 JSON 文件
input_path = "all_games_5000.json"
output_path = "all_games.csv"

with open(input_path, "r", encoding="utf-8") as json_file:
    all_games = json.load(json_file)

fields = [
    "id",
    "name",
    "rating",
    "rating_count",
    "total_rating",
    "total_rating_count",
    "first_release_date",
    "genres",
    "platforms",
    "aggregated_rating",
    "aggregated_rating_count",
    "category",
    "game_engines",
    "game_modes",
    "involved_companies",
    "keywords",
    "player_perspectives",
    "themes",
    "language_supports",
    "game_localizations",


]

with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()

    for game in all_games:
        # 提取每个游戏的基本信息
        row = {
            "id": game.get("id"),
            "name": game.get("name"),
            "rating": game.get("rating"),
            "rating_count": game.get("rating_count"),
            "total_rating": game.get("total_rating"),
            "total_rating_count": game.get("total_rating_count"),
            "first_release_date": game.get("first_release_date"),
            "genres": ", ".join(map(str, game.get("genres", []))),  # 转换为逗号分隔的字符串
            "platforms": ", ".join(map(str, game.get("platforms", []))),  # 转换为逗号分隔的字符串
            "aggregated_rating": game.get("aggregated_rating"),
            "aggregated_rating_count": game.get("aggregated_rating_count"),
            "category": game.get("category"),
            "game_engines": ", ".join(map(str, game.get("game_engines", []))),
            "game_modes": ", ".join(map(str, game.get("game_modes", []))),
            "involved_companies": ", ".join(map(str, [i["company"] for i in game.get("involved_companies", [])])),
            "keywords": ", ".join(map(str, game.get("keywords", []))),
            "player_perspectives": ", ".join(map(str, game.get("player_perspectives", []))),
            "themes": ", ".join(map(str, game.get("themes", []))),
            "language_supports": ", ".join(map(str,[i["language"] for i in game.get("language_supports", [])])),
            "game_localizations": ", ".join(map(str, [i["region"] for i in game.get("game_localizations", [])])),

        }
        writer.writerow(row)

print(f"CSV 文件已生成：{output_path}")
