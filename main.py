import requests
import time
import random
import json
import uuid

def start_roulette(token, times=1):
    headers = {
        "authorization": f"Bearer {token}",
        "origin": "https://game.mars2049.online",
        "referer": "https://game.mars2049.online/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    for i in range(times):
        try:
            res = requests.post("https://api.mars2049.online/api/v1/monopoly/startRollRoulette", headers=headers)
            status = res.status_code
            print(f"🎲 ROULETTE: Putaran ke-{i+1} → Status: {status} {'✅' if status == 200 else '❌'}")
            try:
                data = res.json()
                # Sesuaikan key yang berisi reward atau message di response
                msg = data.get("message") or data.get("data") or str(data)
                print(f"    → Result: {msg}")
            except:
                print(f"    → Response: {res.text}")
            time.sleep(1)
        except Exception as e:
            print(f"    → Error start roulette ke-{i+1}: {e}")

def roll(token):
    GREEN = "\033[92m"
    BLACK = "\033[30m"
    RESET = "\033[0m"

    headers_base = {
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {token}",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://game.mars2049.online",
        "referer": "https://game.mars2049.online/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    roll_count = 0
    while True:
        headers = headers_base.copy()
        headers["callbackid"] = str(random.randint(10, 99))
        try:
            response = requests.post("https://api.mars2049.online/api/v1/monopoly/normalRoll", headers=headers, data="")
            status = response.status_code
            roll_count += 1

            if status != 200:
                print(f"{GREEN}🎯 Roll dadu ke-{roll_count}: → Status: {status} ❌{RESET}")
                print(f"{BLACK}    → Response: {response.text}{RESET}")
                break

            if not response.text.strip():
                print(f"{GREEN}🎯 Roll dadu ke-{roll_count}: → Response kosong, asumsikan roll berhasil ✅{RESET}")
                time.sleep(random.randint(2, 5))
                continue

            try:
                data = response.json()
            except json.JSONDecodeError:
                print(f"{GREEN}🎯 Roll dadu ke-{roll_count}: Response bukan JSON valid:{RESET}")
                print(f"{BLACK}    → {response.text}{RESET}")
                time.sleep(random.randint(2, 5))
                continue

            msg = data.get("message", "Roll sukses")
            print(f"{GREEN}🎯 Roll dadu ke-{roll_count}: → Status: {status} ✅{RESET}")
            print(f"{GREEN}    → Langkah berhasil, respons: \"{msg}\"{RESET}")

            # Jika ada indikator tidak bisa roll lagi, keluar loop
            can_roll = data.get("canRoll")
            if can_roll is False:
                break

            time.sleep(random.randint(2, 5))

        except Exception as e:
            print(f"{GREEN}🎯 Roll dadu ke-{roll_count}: → Error: {e}{RESET}")
            break

def get_current_tile(token):
    headers = {
        "authorization": f"Bearer {token}",
        "origin": "https://game.mars2049.online",
        "referer": "https://game.mars2049.online/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    }
    try:
        res = requests.get("https://api.mars2049.online/api/v1/player/getTick", headers=headers)
        if res.status_code == 200:
            data = res.json()
            return data.get("data", {}).get("tick", -1)
    except:
        pass
    return -1

def open_treasure_box():
    body = {
        "wid": str(uuid.uuid4()),
        "adFormat": "interstitial",
        "language": "en",
        "af": 0,
        "firstName": random.choice(["Anna", "Mike", "Lisa", "Tom", "John"]),
        "lastName": "",
        "from": "window",
        "isPremium": False,
        "motivated": False,
        "platform": "weba",
        "telegramId": random.randint(7000000000, 7999999999),
        "tonConnected": True,
        "username": f"user{random.randint(10000,99999)}",
        "version": "1.27"
    }
    headers = {
        "content-type": "text/plain;charset=UTF-8",
        "origin": "https://game.mars2049.online",
        "referer": "https://game.mars2049.online/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    try:
        res = requests.post("https://bid.tgads.live/bid-request", json=body, headers=headers)
        print(f"    → Treasure box opened: {res.status_code} {'✅' if res.status_code == 200 else '❌'}")
        try:
            print("    → Response:", res.json())
        except:
            print("    → Response:", res.text)
    except Exception as e:
        print("    → Error buka treasure box:", str(e))

def claim_mission_reward(token, mission_id):
    callbackid = str(random.randint(100, 199))
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {token}",
        "callbackid": callbackid,
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://game.mars2049.online",
        "referer": "https://game.mars2049.online/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    data = f"missionId={mission_id}"
    try:
        response = requests.post("https://api.mars2049.online/api/v1/mission/getMissionReward", headers=headers, data=data)
        print(f"    → Klaim mission ID {mission_id}: → Status: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
        if response.headers.get("content-type", "").startswith("application/json"):
            print("    → JSON:", response.json())
        else:
            print("    → Response:", response.text)
    except Exception as e:
        print(f"    → Error klaim mission ID {mission_id}: {e}")

def get_buildings(token):
    headers = {
        "authorization": f"Bearer {token}",
        "callbackid": str(random.randint(10, 99)),
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://game.mars2049.online",
        "referer": "https://game.mars2049.online/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get("https://api.mars2049.online/api/v1/building/buildingsData", headers=headers)
        return resp.json().get("data", [])
    except Exception as e:
        print(f"    → Error parsing get_buildings response: {e}")
        return []

def build_building(token, building_id):
    headers = {
        "authorization": f"Bearer {token}",
        "callbackid": str(random.randint(100, 199)),
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://game.mars2049.online",
        "referer": "https://game.mars2049.online/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    data = f"id={building_id}"
    resp = requests.post("https://api.mars2049.online/api/v1/building/build", headers=headers, data=data)
    print(f"    → [ID {building_id}] Build → Status: {resp.status_code} {'✅' if resp.status_code == 200 else '❌'}")

def upgrade_building(token, building_id, levels):
    for i in range(levels):
        headers = {
            "authorization": f"Bearer {token}",
            "callbackid": str(random.randint(200, 299)),
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://game.mars2049.online",
            "referer": "https://game.mars2049.online/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        }
        data = f"id={building_id}"
        resp = requests.post("https://api.mars2049.online/api/v1/building/levelUp", headers=headers, data=data)
        print(f"    → [ID {building_id}] Level up ({i+1}/{levels}) → Status: {resp.status_code} {'✅' if resp.status_code == 200 else '❌'}")
        time.sleep(random.randint(1, 3))

def handle_buildings(token, target_level):
    print("🏗️ Proses Bangunan: Upgrade ke Level", target_level)
    building_ids = [1, 2, 26, 27, 51, 52, 76, 77]
    existing = get_buildings(token)

    for bid in building_ids:
        bangunan = next((b for b in existing if b.get("id") == bid), None)
        current_level = bangunan.get("level", 0) if bangunan else 0

        if current_level == 0:
            print(f"    → [ID {bid}] Belum dibangun, membangun... ✅")
            build_building(token, bid)
            current_level = 1
            time.sleep(random.randint(1, 2))

        if current_level < target_level:
            level_to_upgrade = target_level - current_level
            print(f"    → [ID {bid}] Level sudah {current_level}, upgrade +{level_to_upgrade}...")
            upgrade_building(token, bid, level_to_upgrade)
        else:
            print(f"    → [ID {bid}] Level sudah {current_level} ≥ target {target_level}, tidak perlu upgrade")

    # Ringkasan akhir
    updated = get_buildings(token)
    print("\n📊 Ringkasan Akhir Bangunan:")
    for bid in building_ids:
        bangunan = next((b for b in updated if b.get("id") == bid), None)
        level = bangunan.get("level", 0) if bangunan else 0
        print(f"    - ID {bid}  → Level {level}")

def main():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except Exception:
        print("Gagal baca config.json, default semua False")
        config = {"roulette": False, "mission": False, "upgrade": False}

    try:
        with open("token.txt", "r") as f:
            tokens = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print("Gagal baca token.txt:", e)
        return

    mission_ids = [1005, 1006, 1007, 1002]
    treasure_tiles = [17, 21, 28, 35]

    for i, token in enumerate(tokens):
        print(f"\n══════════════════════════════════════════════════════════════")
        print(f"🔹 [{i+1}] Memproses akun dengan token: {token[:20]}...{token[-3:]}")
        print(f"══════════════════════════════════════════════════════════════\n")

        if config.get("roulette", False):
            times = input("Mau spin roulette berapa kali? (angka): ")
            try:
                times = int(times)
            except:
                times = 1
            start_roulette(token, times)

        if config.get("mission", False):
            for mid in mission_ids:
                claim_mission_reward(token, mid)
                time.sleep(random.randint(1, 3))

        if config.get("upgrade", False):
            handle_buildings(token, 6)

        # Roll dadu
        roll(token)

        # Check posisi tile dan buka treasure box jika perlu
        tile = get_current_tile(token)
        print(f"    → Posisi tile saat ini: {tile}")
        if tile in treasure_tiles:
            print(f"    → Tile {tile} adalah lokasi treasure box, membuka...")
            open_treasure_box()
        else:
            print("    → Tidak di lokasi treasure box, tidak membuka.")

        print("\n=== Selesai proses akun ini ===\n")
        time.sleep(random.randint(2, 5))

if __name__ == "__main__":
    main()
