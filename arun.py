import asyncio
import aiohttp
from urllib.parse import urlparse
import json

file_path = './domain-list.json'
save_file_name = './new-domain-list.json'

new_data = {
    "blocklist": []
}

async def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"The file {file_path} is not a valid JSON format.")
        return None
    except Exception as e:
        print(f"An error occurred while opening the file: {e}")
        return None

async def save_json(data, save_file_name):
    try:
        with open(save_file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

async def extract_domain(url):
    try:
        parsed_url = urlparse(str(url))
        return parsed_url.netloc
    except ValueError:
        print("Invalid URL:", url)
        return None

async def get_final_url(session, url):
    if not url.startswith('http'):
        request_url = 'https://' + url
    else:
        request_url = url
    try:
        async with session.get(request_url, allow_redirects=True) as response:
            final_url = response.url
            final_domain = await extract_domain(final_url)
            return final_domain
    except Exception as e:
        print(f"An error occurred while getting the final URL for {url}: {e}")
        return None

async def process_url(url, data, session):
    final_domain = await get_final_url(session, url)
    if final_domain and final_domain != url and final_domain not in data['allowlist'] and final_domain not in data['blocklist']:
        print("Redirected domain", final_domain)
        new_data["blocklist"].append(final_domain)

async def main():
    data = await load_json(file_path)
    if data is None:
        return

    async with aiohttp.ClientSession() as session:
        tasks = [process_url(url, data, session) for url in data['blocklist']]
        await asyncio.gather(*tasks)

        # Remove duplicates and save the new data
        new_data['blocklist'] = list(set(new_data['blocklist']))
        await save_json(new_data, save_file_name)

if __name__ == "__main__":
    asyncio.run(main())