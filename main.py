import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest

api_id = 29912666  # O'zingiznikini yozing
api_hash = '717b859cf710a068305fc81e21f3b234'  # O'zingiznikini yozing
client = TelegramClient('session_name', api_id, api_hash)

user_name = "Muslimbek"
bio_list = ["Salom!"]
bio_index = 0

fonts = {
    "1": {'0': '⓪', '1': '①', '2': '②', '3': '③', '4': '④',
          '5': '⑤', '6': '⑥', '7': '⑦', '8': '⑧', '9': '⑨', ':': ':'},
    "2": {'0': '𝟘', '1': '𝟙', '2': '𝟚', '3': '𝟛', '4': '𝟜',
          '5': '𝟝', '6': '𝟞', '7': '𝟟', '8': '𝟠', '9': '𝟡', ':': ':'},
    "3": {'0': '０', '1': '１', '2': '２', '3': '３', '4': '４',
          '5': '５', '6': '６', '7': '７', '8': '８', '9': '９', ':': ':'}
}

current_font = fonts["1"]

def format_time_with_font(time_str, font_map):
    return ''.join(font_map.get(ch, ch) for ch in time_str)

@client.on(events.NewMessage(pattern=r'/setname (.+)'))
async def set_name(event):
    global user_name
    user_name = event.pattern_match.group(1)
    await event.respond(f"✅ Yangi ism: {user_name}")

@client.on(events.NewMessage(pattern=r'/bio (.+)'))
async def add_bio(event):
    new_bio = event.pattern_match.group(1)
    bio_list.append(new_bio)
    await event.respond(f"➕ Bio qo‘shildi: {new_bio}\nJami: {len(bio_list)} ta")

@client.on(events.NewMessage(pattern=r'/biolist'))
async def list_bios(event):
    if not bio_list:
        await event.respond("Bio ro‘yxati bo‘sh.")
        return
    message = "📋 Bio ro‘yxati:\n"
    for i, bio in enumerate(bio_list, 1):
        message += f"{i}. {bio}\n"
    await event.respond(message)

@client.on(events.NewMessage(pattern=r'/removebio (\d+)'))
async def remove_bio(event):
    global bio_index
    idx = int(event.pattern_match.group(1)) - 1
    if 0 <= idx < len(bio_list):
        removed = bio_list.pop(idx)
        await event.respond(f"❌ O'chirildi: {removed}")
        if bio_index > idx:
            bio_index -= 1
        elif bio_index == idx:
            bio_index = 0
    else:
        await event.respond("❗ Noto‘g‘ri raqam kiritildi.")

@client.on(events.NewMessage(pattern=r'/setfont (\d+)'))
async def set_font(event):
    global current_font
    choice = event.pattern_match.group(1)
    if choice in fonts:
        current_font = fonts[choice]
        await event.respond(f"🎨 Soat shrift variantiga {choice} tanlandi.")
    else:
        await event.respond("❗ Noto‘g‘ri variant. Mavjudlar: 1, 2, 3.")

async def update_name_loop():
    while True:
        now_raw = datetime.now().strftime("%H:%M")
        now = format_time_with_font(now_raw, current_font)
        name = f"{user_name} | {now}"
        try:
            await client(UpdateProfileRequest(first_name=name))
        except Exception as e:
            print(f"[Ism xatolik]: {e}")
        await asyncio.sleep(25)

async def update_bio_loop():
    global bio_index
    while True:
        if bio_list:
            current_bio = bio_list[bio_index % len(bio_list)]
            full_bio = current_bio  # Soat olib tashlandi
            try:
                await client(UpdateProfileRequest(about=full_bio))
            except Exception as e:
                print(f"[Bio xatolik]: {e}")
            bio_index += 1
        await asyncio.sleep(3600)

async def main():
    await client.start()
    print("Bot ishga tushdi!")
    await asyncio.gather(
        update_name_loop(),
        update_bio_loop(),
        client.run_until_disconnected()
    )

client.loop.run_until_complete(main())