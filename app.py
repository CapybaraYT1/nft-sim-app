import os
import time
from flask import Flask, render_template, request, jsonify
from supabase import create_client

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user", methods=["POST"])
def get_or_create_user():
    data = request.json
    user_id = data.get("id")
    username = data.get("username", "unknown")
    referrer_id = data.get("referrer_id")
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

    # Атомарная проверка через select for update эмуляция
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

        # Пробуем обновить sold только если он не изменился (оптимистичная блокировка)
        result = supabase.table("gifts").update({"sold": new_sold}).eq("id", gift_id).eq("sold", gift["sold"]).execute()

        if result.data:
            # Успешно заняли слот
            supabase.table("users").update({"stars": user["stars"] - gift["price"]}).eq("id", user_id).execute()
            supabase.table("user_gifts").insert({"user_id": user_id, "gift_id": gift_id}).execute()

            # Автовыдача награды за задание "Купить подарок"
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
            # Кто-то купил одновременно — повторяем
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

    # Атомарно получаем следующий NFT номер
    for attempt in range(3):
        gift = supabase.table("gifts").select("*").eq("id", ug["gift_id"]).execute().data[0]
        current_nft = gift.get("nft_count", 0)
        new_nft = current_nft + 1

        result = supabase.table("gifts").update({"nft_count": new_nft}).eq("id", ug["gift_id"]).eq("nft_count", current_nft).execute()

        if result.data:
            supabase.table("users").update({"stars": user["stars"] - 25}).eq("id", user_id).execute()
            supabase.table("user_gifts").update({"is_upgraded": True, "nft_number": new_nft}).eq("id", user_gift_id).execute()
            user_updated = supabase.table("users").select("*").eq("id", user_id).execute().data[0]
            return jsonify({"success": True, "nft_number": new_nft, "stars": user_updated["stars"]})
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

    user = supabase.table("users").select("*").eq("id", user_id).execute().data[0]
    supabase.table("users").update({"stars": user["stars"] + earn}).eq("id", user_id).execute()
    supabase.table("user_gifts").delete().eq("id", user_gift_id).execute()

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)@app.route("/buy_gift", methods=["POST"])
def buy_gift():
    data = request.json
    user_id = data.get("user_id")
    gift_id = data.get("gift_id")
    gift = supabase.table("gifts").select("*").eq("id", gift_id).execute().data[0]
    user = supabase.table("users").select("*").eq("id", user_id).execute().data[0]
    if user["stars"] < gift["price"]:
        return jsonify({"error": "Недостаточно звёзд"}), 400
    if gift["sold"] >= gift["total_supply"]:
        return jsonify({"error": "Тираж закончился"}), 400
    supabase.table("users").update({"stars": user["stars"] - gift["price"]}).eq("id", user_id).execute()
    supabase.table("gifts").update({"sold": gift["sold"] + 1}).eq("id", gift_id).execute()
    number = gift["sold"] + 1
    supabase.table("user_gifts").insert({"user_id": user_id, "gift_id": gift_id, "number_in_collection": number}).execute()
    # Автовыдача награды за задание "Купить подарок"
    tasks = supabase.table("tasks").select("*").eq("title", "Купить подарок").execute()
    if tasks.data:
        task_id = tasks.data[0]["id"]
        already = supabase.table("user_tasks").select("*").eq("user_id", user_id).eq("task_id", task_id).execute()
        if not already.data:
            supabase.table("user_tasks").insert({"user_id": user_id, "task_id": task_id}).execute()
            supabase.table("users").update({"stars": user["stars"] - gift["price"] + tasks.data[0]["reward"]}).eq("id", user_id).execute()
    user_updated = supabase.table("users").select("*").eq("id", user_id).execute().data[0]
    return jsonify({"success": True, "stars_left": user_updated["stars"]})

@app.route("/upgrade_gift", methods=["POST"])
def upgrade_gift():
    data = request.json
    user_id = data.get("user_id")
    user_gift_id = data.get("user_gift_id")
    user = supabase.table("users").select("*").eq("id", user_id).execute().data[0]
    if user["stars"] < 25:
        return jsonify({"error": "Нужно 25 звёзд для улучшения"}), 400
    supabase.table("users").update({"stars": user["stars"] - 25}).eq("id", user_id).execute()
    supabase.table("user_gifts").update({"is_upgraded": True}).eq("id", user_gift_id).execute()
    return jsonify({"success": True})

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
            return jsonify({"error": "Сначала подпишитесь на канал @cat_zz"}), 400
    user = supabase.table("users").select("*").eq("id", user_id).execute().data[0]
    supabase.table("users").update({"stars": user["stars"] + task["reward"]}).eq("id", user_id).execute()
    supabase.table("user_tasks").insert({"user_id": user_id, "task_id": task_id}).execute()
    return jsonify({"success": True, "stars": user["stars"] + task["reward"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
