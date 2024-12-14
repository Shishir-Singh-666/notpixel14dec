import requests
import random
import json
import time


# Function to load proxies from a file and prepend "http://"
def load_proxies():
    try:
        with open('proxies.txt', 'r') as file:
            proxies = [f"http://{line.strip()}" for line in file.readlines() if line.strip()]
            if not proxies:
                raise ValueError("No valid proxies found in the file.")
            return proxies
    except Exception as e:
        print(f"[ERROR] Failed to load proxies: {e}")
        return []


# Function to generate random user agents
def generate_user_agent():
    os = ['Windows', 'Linux', 'iOS', 'Android']
    versions = ['8', '9', '10', '11', '12', '13', '14']
    devices = ['Samsung', 'Motorola', 'Xiaomi', 'Huawei', 'OnePlus']

    selected_os = random.choice(os)
    if selected_os == 'Android':
        version = random.choice(versions)
        device = random.choice(devices)
        return f"Mozilla/5.0 (Linux; Android {version}; {device}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36"
    else:
        return f"Mozilla/5.0 ({selected_os} NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"


# Function to generate random headers
def generate_headers():
    user_agent = generate_user_agent()
    return {
        'Host': 'api.adsgram.ai',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua-platform': '"Android"',
        'User-Agent': user_agent,
        'sec-ch-ua': '"Android WebView";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'Accept': '*/*',
        'Origin': 'https://app.notpx.app',
        'X-Requested-With': 'org.telegram.messenger',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://app.notpx.app/',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en,en-US;q=0.9'
    }


# Function to validate a proxy
def validate_proxy(proxy):
    try:
        test_url = "https://api.adsgram.ai/"
        response = requests.get(test_url, proxies={'http': proxy, 'https': proxy}, timeout=5)
        return response.status_code == 200
    except Exception:
        return False


# Function to generate a random chat instance
def generate_chat_instance():
    return str(random.randint(10000000000000, 99999999999999))


# Function to make API requests
def make_api_request(user_id, tg_id, proxy):
    url = f"https://api.adsgram.ai/adv?blockId=4853&tg_id={tg_id}&tg_platform=android&platform=Linux%20aarch64&language=en&chat_type=sender&chat_instance={generate_chat_instance()}&top_domain=app.notpx.app"
    headers = generate_headers()
    proxy_config = {'http': proxy, 'https': proxy}

    try:
        response = requests.get(url, headers=headers, proxies=proxy_config, timeout=10)
        print(f"[DEBUG] Full Response for {user_id}: {response.text}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] Status {response.status_code} for {user_id}")
    except Exception as e:
        print(f"[ERROR] Proxy failure {proxy} for {user_id}: {e}")
    return None


# Function to extract rewards from the API response
def extract_reward(response):
    if response and 'banner' in response and 'trackings' in response['banner']:
        for tracking in response['banner']['trackings']:
            if tracking.get('name') == 'reward':
                return tracking.get('value')
    return None


# Main function
def main():
    try:
        # Load users and proxies
        with open('users.json', 'r') as file:
            users = json.load(file)

        proxies = load_proxies()
        if not proxies:
            print("[ERROR] No valid proxies loaded.")
            return

        total_points = 0
        user_points = {user_id: 0 for user_id in users}

        print("\n[INFO] Starting NOT PIXEL Engine\n")

        while True:
            rewards = []
            for user_id, user_data in users.items():
                tg_id = user_data['tg_id']

                # Pick a random proxy
                proxy = random.choice(proxies)
                print(f"[INFO] Sending request for User ID {user_id} with Proxy {proxy}")

                response = make_api_request(user_id, tg_id, proxy)
                if response:
                    reward = extract_reward(response)
                    if reward:
                        rewards.append((user_id, reward))
                        print(f"[SUCCESS] Reward received for {user_id}: {reward}")
                    else:
                        print(f"[ERROR] No reward found for {user_id}")
                else:
                    print(f"[ERROR] Request failed for {user_id}")

            # Update rewards and points
            for user_id, reward in rewards:
                user_points[user_id] += 16  # Assuming each reward is worth 16 PX
                total_points += 16
                print(f"[INFO] User {user_id} earned 16 PX. Total PX: {total_points}")

            print(f"\n[INFO] Total PX Earned: {total_points}\n")

            # Add random delay
            time.sleep(random.uniform(10, 13))

    except KeyboardInterrupt:
        print("[INFO] Script terminated by user.")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
