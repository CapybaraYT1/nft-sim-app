import os
import time
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from supabase import create_client

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 7231807922
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BACKGROUNDS = [
    {"name": "Azure Blue", "color": "5CB0CA", "chance": 1.0},
    {"name": "Battleship Grey", "color": "8B8B83", "chance": 1.0},
    {"name": "Caramel", "color": "CF9831", "chance": 1.0},
    {"name": "Carmine", "color": "E05649", "chance": 1.0},
    {"name": "Fandango", "color": "E089B4", "chance": 1.0},
    {"name": "French Blue", "color": "5C9BC4", "chance": 1.0},
    {"name": "Gunmetal", "color": "4C5D64", "chance": 1.0},
    {"name": "Jade Green", "color": "55C39C", "chance": 1.0},
    {"name": "Lavender", "color": "B788E4", "chance": 1.0},
    {"name": "Mexican Pink", "color": "E36692", "chance": 1.0},
    {"name": "Navy Blue", "color": "6C9EDD", "chance": 1.0},
    {"name": "Onyx Black", "color": "4D5255", "chance": 1.0},
    {"name": "Pacific Cyan", "color": "5ABEA6", "chance": 1.0},
    {"name": "Pure Gold", "color": "CBAA3F", "chance": 1.0},
    {"name": "Ranger Green", "color": "5E7849", "chance": 1.0},
    {"name": "Raspberry", "color": "E07A85", "chance": 1.0},
    {"name": "Rifle Green", "color": "64685A", "chance": 1.0},
    {"name": "Satin Gold", "color": "BF9B47", "chance": 1.0},
    {"name": "Shamrock Green", "color": "8AB063", "chance": 1.0},
    {"name": "Silver Blue", "color": "80A5B8", "chance": 1.0},
    {"name": "Sky Blue", "color": "58B4C9", "chance": 1.0},
    {"name": "Strawberry", "color": "DD8E6F", "chance": 1.0},
    {"name": "Amber", "color": "D9B344", "chance": 1.2},
    {"name": "Black", "color": "2E2F31", "chance": 1.2},
    {"name": "Camo Green", "color": "75944E", "chance": 1.2},
    {"name": "Cappuccino", "color": "B1907D", "chance": 1.2},
    {"name": "Carrot Juice", "color": "DA9866", "chance": 1.2},
    {"name": "Chocolate", "color": "A56E59", "chance": 1.2},
    {"name": "Dark Green", "color": "526341", "chance": 1.2},
    {"name": "Deep Cyan", "color": "31B5AA", "chance": 1.2},
    {"name": "Electric Indigo", "color": "A880F3", "chance": 1.2},
    {"name": "Feldgrau", "color": "889289", "chance": 1.2},
    {"name": "Fire Engine", "color": "F15F50", "chance": 1.2},
    {"name": "French Violet", "color": "C261E6", "chance": 1.2},
    {"name": "Gunship Green", "color": "568A64", "chance": 1.2},
    {"name": "Hunter Green", "color": "90AE78", "chance": 1.2},
    {"name": "Indigo Dye", "color": "537990", "chance": 1.2},
    {"name": "Ivory White", "color": "BAB7B2", "chance": 1.2},
    {"name": "Lemongrass", "color": "AEB75A", "chance": 1.2},
    {"name": "Moonstone", "color": "7DB0B3", "chance": 1.2},
    {"name": "Mystic Pearl", "color": "D08B6C", "chance": 1.2},
    {"name": "Neon Blue", "color": "7496F8", "chance": 1.2},
    {"name": "Old Gold", "color": "B58D38", "chance": 1.2},
    {"name": "Orange", "color": "E5A659", "chance": 1.2},
    {"name": "Pacific Green", "color": "6FC794", "chance": 1.2},
    {"name": "Persimmon", "color": "DA8F5B", "chance": 1.2},
    {"name": "Platinum", "color": "B2ADA7", "chance": 1.2},
    {"name": "Purple", "color": "AD6AAD", "chance": 1.2},
    {"name": "Seal Brown", "color": "654C45", "chance": 1.2},
    {"name": "Steel Grey", "color": "959FA9", "chance": 1.2},
    {"name": "Tomato", "color": "E5783E", "chance": 1.2},
    {"name": "Turquoise", "color": "61B196", "chance": 1.2},
    {"name": "Aquamarine", "color": "53AEA3", "chance": 1.5},
    {"name": "Burgundy", "color": "9E5B64", "chance": 1.5},
    {"name": "Burnt Sienna", "color": "D76F3C", "chance": 1.5},
    {"name": "Celtic Blue", "color": "45B8EE", "chance": 1.5},
    {"name": "Chestnut", "color": "BF6F54", "chance": 1.5},
    {"name": "Cobalt Blue", "color": "6088CE", "chance": 1.5},
    {"name": "Copper", "color": "D08657", "chance": 1.5},
    {"name": "Coral Red", "color": "DA886B", "chance": 1.5},
    {"name": "Cyberpunk", "color": "8485EC", "chance": 1.5},
    {"name": "Dark Lilac", "color": "B17DA4", "chance": 1.5},
    {"name": "Desert Sand", "color": "B3A082", "chance": 1.5},
    {"name": "Electric Purple", "color": "C770C6", "chance": 1.5},
    {"name": "Emerald", "color": "79C585", "chance": 1.5},
    {"name": "English Violet", "color": "B186BB", "chance": 1.5},
    {"name": "Grape", "color": "9D74C2", "chance": 1.5},
    {"name": "Khaki Green", "color": "A0A66A", "chance": 1.5},
    {"name": "Light Olive", "color": "BBA95F", "chance": 1.5},
    {"name": "Malachite", "color": "8FB256", "chance": 1.5},
    {"name": "Marine Blue", "color": "4D679A", "chance": 1.5},
    {"name": "Midnight Blue", "color": "505C77", "chance": 1.5},
    {"name": "Mint Green", "color": "7ECC81", "chance": 1.5},
    {"name": "Mustard", "color": "D3980C", "chance": 1.5},
    {"name": "Pine Green", "color": "629E78", "chance": 1.5},
    {"name": "Pistachio", "color": "7C9A66", "chance": 1.5},
    {"name": "Roman Silver", "color": "9EA4B0", "chance": 1.5},
    {"name": "Rosewood", "color": "B17573", "chance": 1.5},
    {"name": "Sapphire", "color": "58A4C8", "chance": 1.5},
    {"name": "Tactical Pine", "color": "3F7C6B", "chance": 1.5},
]

GIFT_MODELS = {
    "Easter Egg": [
        {"name": "Purple Bird", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Purple%20Bird.webp", "chance": 2.5},
        {"name": "Protein Lamp", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Protein%20Lamp.webp", "chance": 2.5},
        {"name": "Porcelain", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Porcelain.webp", "chance": 2.5},
        {"name": "Mr. Benedict", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Mr.%20Benedict.webp", "chance": 2.5},
        {"name": "Moon Watch", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Moon%20Watch.webp", "chance": 2.5},
        {"name": "Meadow", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Meadow.webp", "chance": 2.5},
        {"name": "Matryoshka", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Matryoshka.webp", "chance": 2.5},
        {"name": "Khokhloma", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Khokhloma.webp", "chance": 2.5},
        {"name": "Gzhel", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Gzhel.webp", "chance": 2.5},
        {"name": "Frosted", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Frosted.webp", "chance": 2.5},
        {"name": "Flowers", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Flowers.webp", "chance": 2.5},
        {"name": "Flower Bed", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Flower%20Bed.webp", "chance": 2.5},
        {"name": "Crown Prince", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Crown%20Prince.webp", "chance": 2.5},
        {"name": "Bronze", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Bronze.webp", "chance": 2.5},
        {"name": "Brick Wall", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Brick%20Wall.webp", "chance": 2.5},
        {"name": "Ball of Steel", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Ball%20of%20Steel.webp", "chance": 2.5},
        {"name": "3D Render", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/3D%20Render.webp", "chance": 2.5},
        {"name": "Stamper", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Stamper.webp", "chance": 2.0},
        {"name": "Scrambull", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Scrambull.webp", "chance": 2.0},
        {"name": "Omeletron", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Omeletron.webp", "chance": 2.0},
        {"name": "OS Shell", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/OS%20Shell.webp", "chance": 2.0},
        {"name": "Magic Key", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Magic%20Key.webp", "chance": 2.0},
        {"name": "Ladybird", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Ladybird.webp", "chance": 2.0},
        {"name": "Jupiter", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Jupiter.webp", "chance": 2.0},
        {"name": "Free Flight", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Free%20Flight.webp", "chance": 2.0},
        {"name": "Fish Pod", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Fish%20Pod.webp", "chance": 2.0},
        {"name": "Fine Silver", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Fine%20Silver.webp", "chance": 2.0},
        {"name": "Eggsecutive", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Eggsecutive.webp", "chance": 2.0},
        {"name": "Eggburger", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Eggburger.webp", "chance": 2.0},
        {"name": "Creeper", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Creeper.webp", "chance": 2.0},
        {"name": "Chicken", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Chicken.webp", "chance": 2.0},
        {"name": "Boiled Pepe", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Boiled%20Pepe.webp", "chance": 2.0},
        {"name": "Treasure Map", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Treasure%20Map.webp", "chance": 1.5},
        {"name": "Stained Glass", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Stained%20Glass.webp", "chance": 1.5},
        {"name": "Pure Gold", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Pure%20Gold.webp", "chance": 1.5},
        {"name": "Ice Cream", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Ice%20Cream.webp", "chance": 1.5},
        {"name": "Foliage", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Foliage.webp", "chance": 1.5},
        {"name": "Eggmoji", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Eggmoji.webp", "chance": 1.5},
        {"name": "Dragon", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Dragon.webp", "chance": 1.0},
        {"name": "Starry Gift", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Starry%20Gift.webp", "chance": 1.0},
        {"name": "Pearl", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Pearl.webp", "chance": 1.0},
        {"name": "Pastel Candy", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Pastel%20Candy.webp", "chance": 1.0},
        {"name": "Meowling", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Meowling.webp", "chance": 1.0},
        {"name": "Koshchei", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Koshchei.webp", "chance": 1.0},
        {"name": "Faberge", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Faberge.webp", "chance": 1.0},
        {"name": "Egghead", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Egghead.webp", "chance": 1.0},
        {"name": "Dogel Mogel", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Dogel%20Mogel.webp", "chance": 1.0},
        {"name": "Deep Freeze", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Deep%20Freeze.webp", "chance": 1.0},
        {"name": "Chocolate", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Chocolate.webp", "chance": 1.0},
        {"name": "Cactus", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Cactus.webp", "chance": 1.0},
        {"name": "Unicorn", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Unicorn.webp", "chance": 0.5},
        {"name": "Sea Turtle", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Sea%20Turtle.webp", "chance": 0.5},
        {"name": "Red Whelp", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Red%20Whelp.webp", "chance": 0.5},
        {"name": "Little Doge", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Little%20Doge.webp", "chance": 0.5},
        {"name": "Little Dino", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Little%20Dino.webp", "chance": 0.5},
        {"name": "Jurassic", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Jurassic.webp", "chance": 0.5},
        {"name": "Easter Bunny", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Easter%20Bunny.webp", "chance": 0.5},
        {"name": "Early Bird", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Early%20Bird.webp", "chance": 0.5},
        {"name": "Cryptid", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Cryptid.webp", "chance": 0.5},
        {"name": "Choco Bunny", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Choco%20Bunny.webp", "chance": 0.5},
        {"name": "Baby Turtle", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Baby%20Turtle.webp", "chance": 0.5},
        {"name": "Baby Chick", "url": "https://telegifter.ru/wp-content/themes/gifts/assets/img/gifts/easteregg/Baby%20Chick.webp", "chance": 0.5},
    ]
}

def weighted_choice(items):
    total = sum(i["chance"] for i in items)
    r = random.uniform(0, total)
    cumulative = 0
    for item in items:
        cumulative += item["chance"]
        if r <= cumulative:
            return item
    return items[-1]

def check_ban(user_id):
    ban = supabase.table("bans").select("*").eq("user_id", user_id).execute().data
    if not ban:
        return None
    ban = ban[0]
    if ban["is_permanent"]:
        return {"banned": True, "permanent": True, "reason": ban.get("reason", "")}
    if ban["banned_until"]:
        until = datetime.fromisoformat(ban["banned_until"].replace("Z", "+00:00"))
        now = datetime.now(until.tzinfo)
        if now < until:
            diff = until - now
            hours = int(diff.total_seconds() // 3600)
            minutes = int((diff.total_seconds() % 3600) // 60)
            return {"banned": True, "permanent": False, "reason": ban.get("reason", ""), "hours": hours, "minutes": minutes}
        else:
            supabase.table("bans").delete().eq("user_id", user_id).execute()
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user", methods=["POST"])
def get_or_create_user():
    data = request.json
    user_id = data.get("id")
    username = data.get("username", "unknown")
    referrer_id = data.get("referrer_id")
    ban = check_ban(user_id)
    if ban:
        return jsonify({"banned": True, **ban}), 403
    existing = supabase.table("users").select("*").eq("id", user_id).execute()
    if not existing.data:
        supabase.table("users").insert({"id": user_id, "username": username, "stars": 100}).execute()
        if referrer_id and referrer_id != user_id:
            ref = supabase.table("users").select("*").eq("id", referrer_id).execute()
            if ref.data:
                supabase.table("users").update({"stars": ref.data[0]["stars"] + 500}).eq("id", referrer_id).execute()
    user = supabase.table("users").select("*").eq("id", user_id).execute()
    return jsonify(user.data[0])

@app.route("/gifts")
def get_gifts():
    gifts = supabase.table("gifts").select("*").order("price", desc=False).execute()
    return jsonify(gifts.data)

@app.route("/user_gifts/<int:user_id>")
def get_user_gifts(user_id):
    gifts = supabase.table("user_gifts").select("*, gifts(*)").eq("user_id", user_id).execute()
    return jsonify(gifts.data)

@app.route("/buy_gift", methods=["POST"])
def buy_gift():
    data = request.json
    user_id = data.get("user_id")
    gift_id = data.get("gift_id")
    ban = check_ban(user_id)
    if ban:
        return jsonify({"error": "Вы заблокированы"}), 403
    for attempt in range(3):
        gift = supabase.table("gifts").select("*").eq("id", gift_id).execute().data
        if not gift:
            return jsonify({"error": "Подарок не найден"}), 404
        gift = gift[0]
        user = supabase.table("users").select("*").eq("id", user_id).execute().data
        if not user:
            return jsonify({"error": "Пользователь не найден"}), 404
        user = user[0]
        if user["stars"] < gift["price"]:
            return jsonify({"error": "Недостаточно звёзд"}), 400
        if gift["sold"] >= gift["total_supply"]:
            return jsonify({"error": "Тираж закончился"}), 400
        new_sold = gift["sold"] + 1
        result = supabase.table("gifts").update({"sold": new_sold}).eq("id", gift_id).eq("sold", gift["sold"]).execute()
        if result.data:
            supabase.table("users").update({"stars": user["stars"] - gift["price"]}).eq("id", user_id).execute()
            supabase.table("user_gifts").insert({"user_id": user_id, "gift_id": gift_id}).execute()
            tasks = supabase.table("tasks").select("*").eq("title", "Купить подарок").execute()
            if tasks.data:
                task_id = tasks.data[0]["id"]
                already = supabase.table("user_tasks").select("*").eq("user_id", user_id).eq("task_id", task_id).execute()
                if not already.data:
                    supabase.table("user_tasks").insert({"user_id": user_id, "task_id": task_id}).execute()
                    bonus = tasks.data[0]["reward"]
                    current_stars = user["stars"] - gift["price"]
                    supabase.table("users").update({"stars": current_stars + bonus}).eq("id", user_id).execute()
            user_updated = supabase.table("users").select("*").eq("id", user_id).execute().data[0]
            return jsonify({"success": True, "stars_left": user_updated["stars"]})
        else:
            time.sleep(0.1)
    return jsonify({"error": "Попробуйте снова"}), 409

@app.route("/upgrade_gift", methods=["POST"])
def upgrade_gift():
    data = request.json
    user_id = data.get("user_id")
    user_gift_id = data.get("user_gift_id")
    user = supabase.table("users").select("*").eq("id", user_id).execute().data[0]
    if user["stars"] < 25:
        return jsonify({"error": "Нужно 25 звёзд для улучшения"}), 400
    ug = supabase.table("user_gifts").select("*").eq("id", user_gift_id).execute().data
    if not ug or ug[0]["is_upgraded"]:
        return jsonify({"error": "Уже улучшен"}), 400
    ug = ug[0]
    gift = supabase.table("gifts").select("*").eq("id", ug["gift_id"]).execute().data[0]
    gift_name = gift["name"]
    models = GIFT_MODELS.get(gift_name, [])
    if not models:
        return jsonify({"error": "Модели не найдены для: " + gift_name}), 400
    chosen_model = weighted_choice(models)
    chosen_bg = weighted_choice(BACKGROUNDS)
    for attempt in range(3):
        current_nft = gift.get("nft_count", 0)
        new_nft = current_nft + 1
        result = supabase.table("gifts").update({"nft_count": new_nft}).eq("id", ug["gift_id"]).eq("nft_count", current_nft).execute()
        if result.data:
            supabase.table("users").update({"stars": user["stars"] - 25}).eq("id", user_id).execute()
            supabase.table("user_gifts").update({
                "is_upgraded": True,
                "nft_number": new_nft,
                "model_name": chosen_model["name"],
                "model_url": chosen_model["url"],
                "model_chance": chosen_model["chance"],
                "bg_name": chosen_bg["name"],
                "bg_color": chosen_bg["color"],
                "bg_chance": chosen_bg["chance"],
            }).eq("id", user_gift_id).execute()
            user_updated = supabase.table("users").select("*").eq("id", user_id).execute().data[0]
            available = gift["total_supply"] - gift.get("sold_for_stars", 0)
            return jsonify({
                "success": True,
                "nft_number": new_nft,
                "stars": user_updated["stars"],
                "model_name": chosen_model["name"],
                "model_url": chosen_model["url"],
                "model_chance": chosen_model["chance"],
                "bg_name": chosen_bg["name"],
                "bg_color": chosen_bg["color"],
                "bg_chance": chosen_bg["chance"],
                "gift_name": gift_name,
                "nft_count": new_nft,
                "available": available,
                "username": user["username"],
            })
        else:
            time.sleep(0.1)
    return jsonify({"error": "Попробуйте снова"}), 409

@app.route("/sell_gift", methods=["POST"])
def sell_gift():
    data = request.json
    user_id = data.get("user_id")
    user_gift_id = data.get("user_gift_id")
    ug = supabase.table("user_gifts").select("*, gifts(*)").eq("id", user_gift_id).eq("user_id", user_id).execute().data
    if not ug:
        return jsonify({"error": "Подарок не найден"}), 404
    ug = ug[0]
    if ug["is_upgraded"]:
        return jsonify({"error": "Улучшенный подарок нельзя продать"}), 400
    price = ug["gifts"]["price"]
    earn = int(price * 0.85)
    gift_id = ug["gift_id"]
    user = supabase.table("users").select("*").eq("id", user_id).execute().data[0]
    supabase.table("users").update({"stars": user["stars"] + earn}).eq("id", user_id).execute()
    supabase.table("user_gifts").delete().eq("id", user_gift_id).execute()
    gift = supabase.table("gifts").select("*").eq("id", gift_id).execute().data[0]
    new_sfs = gift.get("sold_for_stars", 0) + 1
    supabase.table("gifts").update({"sold_for_stars": new_sfs}).eq("id", gift_id).execute()
    user_updated = supabase.table("users").select("*").eq("id", user_id).execute().data[0]
    return jsonify({"success": True, "stars": user_updated["stars"], "earned": earn})

@app.route("/tasks/<int:user_id>")
def get_tasks(user_id):
    tasks = supabase.table("tasks").select("*").execute()
    done = supabase.table("user_tasks").select("task_id").eq("user_id", user_id).execute()
    done_ids = [d["task_id"] for d in done.data]
    for t in tasks.data:
        t["done"] = t["id"] in done_ids
    return jsonify(tasks.data)

@app.route("/complete_task", methods=["POST"])
def complete_task():
    data = request.json
    user_id = data.get("user_id")
    task_id = data.get("task_id")
    already = supabase.table("user_tasks").select("*").eq("user_id", user_id).eq("task_id", task_id).execute()
    if already.data:
        return jsonify({"error": "Уже выполнено"}), 400
    task = supabase.table("tasks").select("*").eq("id", task_id).execute().data[0]
    if task["title"] == "Подписаться на канал":
        import requests as req
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
        resp = req.get(url, params={"chat_id": "@cat_zz", "user_id": user_id})
        result = resp.json()
        status = result.get("result", {}).get("status", "")
        if status not in ["member", "administrator", "creator"]:
            return jsonify({"error": "Сначала подпишитесь на @cat_zz"}), 400
    user = supabase.table("users").select("*").eq("id", user_id).execute().data[0]
    supabase.table("users").update({"stars": user["stars"] + task["reward"]}).eq("id", user_id).execute()
    supabase.table("user_tasks").insert({"user_id": user_id, "task_id": task_id}).execute()
    return jsonify({"success": True, "stars": user["stars"] + task["reward"]})

def is_admin(user_id):
    return int(user_id) == ADMIN_ID

@app.route("/admin/users")
def admin_users():
    if not is_admin(request.args.get("admin_id", 0)):
        return jsonify({"error": "Нет доступа"}), 403
    users = supabase.table("users").select("*").order("stars", desc=True).limit(50).execute()
    bans = supabase.table("bans").select("*").execute()
    ban_ids = {b["user_id"]: b for b in bans.data}
    result = []
    for u in users.data:
        u["is_banned"] = u["id"] in ban_ids
        u["ban_info"] = ban_ids.get(u["id"])
        result.append(u)
    return jsonify(result)

@app.route("/admin/ban", methods=["POST"])
def admin_ban():
    data = request.json
    if not is_admin(data.get("admin_id", 0)):
        return jsonify({"error": "Нет доступа"}), 403
    user_id = data.get("user_id")
    reason = data.get("reason", "")
    permanent = data.get("permanent", False)
    hours = data.get("hours", 0)
    ban_data = {"user_id": user_id, "reason": reason, "is_permanent": permanent}
    if not permanent and hours:
        from datetime import timedelta, timezone
        until = datetime.now(timezone.utc) + timedelta(hours=hours)
        ban_data["banned_until"] = until.isoformat()
    supabase.table("bans").upsert(ban_data).execute()
    return jsonify({"success": True})

@app.route("/admin/unban", methods=["POST"])
def admin_unban():
    data = request.json
    if not is_admin(data.get("admin_id", 0)):
        return jsonify({"error": "Нет доступа"}), 403
    supabase.table("bans").delete().eq("user_id", data.get("user_id")).execute()
    return jsonify({"success": True})

@app.route("/admin/gifts")
def admin_gifts():
    if not is_admin(request.args.get("admin_id", 0)):
        return jsonify({"error": "Нет доступа"}), 403
    gifts = supabase.table("gifts").select("*").execute()
    return jsonify(gifts.data)

@app.route("/admin/delete_gift_type", methods=["POST"])
def admin_delete_gift_type():
    data = request.json
    if not is_admin(data.get("admin_id", 0)):
        return jsonify({"error": "Нет доступа"}), 403
    gift_id = data.get("gift_id")
    gift = supabase.table("gifts").select("*").eq("id", gift_id).execute().data[0]
    price = gift["price"]
    owners = supabase.table("user_gifts").select("user_id").eq("gift_id", gift_id).execute().data
    for owner in owners:
        uid = owner["user_id"]
        user = supabase.table("users").select("*").eq("id", uid).execute().data[0]
        supabase.table("users").update({"stars": user["stars"] + price}).eq("id", uid).execute()
    supabase.table("user_gifts").delete().eq("gift_id", gift_id).execute()
    supabase.table("gifts").update({"sold": 0, "nft_count": 0, "sold_for_stars": 0}).eq("id", gift_id).execute()
    return jsonify({"success": True})

@app.route("/admin/delete_nft", methods=["POST"])
def admin_delete_nft():
    data = request.json
    if not is_admin(data.get("admin_id", 0)):
        return jsonify({"error": "Нет доступа"}), 403
    user_gift_id = data.get("user_gift_id")
    ug = supabase.table("user_gifts").select("*, gifts(*)").eq("id", user_gift_id).execute().data
    if not ug:
        return jsonify({"error": "Не найден"}), 404
    ug = ug[0]
    uid = ug["user_id"]
    price = ug["gifts"]["price"]
    user = supabase.table("users").select("*").eq("id", uid).execute().data[0]
    supabase.table("users").update({"stars": user["stars"] + price}).eq("id", uid).execute()
    supabase.table("user_gifts").delete().eq("id", user_gift_id).execute()
    gift = supabase.table("gifts").select("*").eq("id", ug["gift_id"]).execute().data[0]
    new_sold = max(0, gift["sold"] - 1)
    supabase.table("gifts").update({"sold": new_sold}).eq("id", ug["gift_id"]).execute()
    return jsonify({"success": True})

@app.route("/admin/user_gifts/<int:user_id>")
def admin_user_gifts(user_id):
    if not is_admin(request.args.get("admin_id", 0)):
        return jsonify({"error": "Нет доступа"}), 403
    gifts = supabase.table("user_gifts").select("*, gifts(*)").eq("user_id", user_id).execute()
    return jsonify(gifts.data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
