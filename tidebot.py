import nextcord
import random
import json
import os

# ⚠️ トークンは環境変数から読み込む
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

intents = nextcord.Intents.default()
intents.message_content = True
client = nextcord.Client(intents=intents)

DATA_FILE = "tidebot_data.json"

# データ読み込み
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {}

# 拾えるアイテム
items = [
    "貝殻", "シーグラス", "星の砂", "小瓶", "流木",
    "君がいつか失くしたもの", "君がいつか忘れてしまった記憶",
    "珊瑚", "何か", "メッセージボトル", "古びた鍵",
    "青いビー玉", "白いビー玉", "ガラスの破片",
    "錆びた羅針盤", "欠けた指輪", "壊れたオルゴール",
    "誰かのボタン", "折れた羽根", "古い切符", "黒いリボン",
    "波に溶けた絵具", "欠けたカップ", "眠らない時計",
    "溶けかけのキャンドル", "錆びたブローチ", "誰かのコート",
]

# お題と対応色
prompt_colors = {
    "夕暮れ": 0xF3BF88, "朝焼け": 0xF9C5B7, "雨上がり": 0xA1C7D4,
    "傘": 0xC1B4D6, "制服": 0x7A90A4, "光": 0xFFF1A6,
    "夢": 0xE6B7E5, "孤独": 0x7F8FA6, "夏の匂い": 0xF0D890,
    "冬の海": 0x7FB3D5, "秘密": 0xC79ECF, "再会": 0xE1A68A,
    "記憶": 0xB7C9E2, "眠れない夜": 0x4C5270, "月明かり": 0xCDE6F5,
    "花びら": 0xF8C8DC, "手紙": 0xE6D2B5, "影": 0x7D7D7D,
    "約束": 0xFFD580, "異国": 0xD9C4A1
}

# データ保存用関数
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = str(message.author.id)

    # 「拾う」コマンド
    if message.content == "拾う":
        found = random.choice(items)
        await message.channel.send(f"{found}を拾った")

        data.setdefault(user_id, []).append(found)
        save_data()

    # 「図鑑」コマンド
    elif message.content == "図鑑":
        if not data.get(user_id):
            await message.channel.send("まだ何も拾っていません。")
        else:
            unique_items = sorted(set(data[user_id]))
            collected = "、".join(unique_items)

            embed = discord.Embed(
                title="･ﾟ✦List",
                description=collected,
                color=0x84A2D4
            )
            embed.set_footer(text="海辺で拾った思い出。")
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url
            )
            await message.channel.send(embed=embed)

    # 「お題」コマンド（数字指定対応）
    elif message.content.startswith("お題"):
        parts = message.content.replace("お題", "").strip()
        num = int(parts) if parts.isdigit() else 1
        num = max(1, min(10, num))  # 最大10個

        selected = random.sample(list(prompt_colors.keys()), num)
        color = prompt_colors[selected[0]] if num == 1 else random.choice(list(prompt_colors.values()))
        joined = "、".join(selected)

        embed = discord.Embed(
            title="‎‎.𖥔 ݁Theme",
            description=joined,
            color=color
        )
        embed.set_footer(text="潮風のなかで夢を見た。")
        await message.channel.send(embed=embed)

client.run(TOKEN)
