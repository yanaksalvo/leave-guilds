import requests
import time

def leave_all_guilds(token):
    try:
        headers = {"Authorization": token}
        while True:
            response = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)

            if response.status_code == 200:
                guilds = response.json()
                if not guilds:
                    print("[INFO] Hesap herhangi bir sunucuda değil.")
                    return
                
                for guild in guilds:
                    guild_id = guild['id']
                    guild_name = guild['name']
                    response_leave = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{guild_id}", headers=headers)
                    if response_leave.status_code in [200, 201, 204]:
                        print(f"[STATUS] Left >> [ Guild ID: {guild_id}, Guild Name: {guild_name} ]")
                    elif response_leave.status_code == 429:
                        print(f"[STATUS] Failed Leave >> [ Guild ID: {guild_id} ]")
                        time.sleep(response_leave.json().get('retry_after', 5)) # 5 saniye bekleme varsayılan değer
                        continue  # 429 hatası aldığımızda bir sonraki sunucuya geç
                    else:
                        print(f"[STATUS] Error {response_leave.status_code} >> [ Guild ID: {guild_id} ]")
            
            else:
                print(f"[ERROR] Unable to fetch guilds. Status code: {response.status_code}")
                time.sleep(5)  # 5 saniye bekleme

    except Exception as e:
        print(f"[ERROR] An exception occurred: {str(e)}")

# Kullanıcıdan token'i al
token = input("Token =>: ")
leave_all_guilds(token)
