from aiogram import Bot, Dispatcher, types
from bs4 import BeautifulSoup
import aiohttp
import asyncio


async def scrape_website():
    url = "https://ethio-bookstore.com/product-category/amharic-books-%E1%8B%A8%E1%8A%A0%E1%88%9B%E1%88%AD%E1%8A%9B-%E1%88%98%E1%8C%BD%E1%88%90%E1%8D%8D%E1%89%B5/"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), "html.parser")
                products = soup.find_all("li", class_="product")
                scraped_data = []
                for product in products:
                    title = product.find("h2", class_="woocommerce-loop-product__title").text.strip()
                    image_url = product.find("img", class_="attachment-woocommerce_thumbnail").get("src")
                    price_elem = product.find("span", class_="woocommerce-Price-amount amount")
                    price = price_elem.text.strip() if price_elem else "N/A"
                    scraped_data.append({"Title": title, "Image URL": image_url, "Price": price})
                return scraped_data
            else:
                print("Failed to retrieve the webpage")
                return None

async def send_to_telegram_channel(item, user_name):
    bot_token = '6958764409:AAFktQRVLIpfsgyQn0hPodPHRNjmfht9F7I'
    bot = Bot(token=bot_token)
    channel_id = '-1002036044902'
    message = ""
    message += f"Title: {item['Title']}\n"
    message += f"Image URL: {item['Image URL']}\n"
    message += f"Price: {item['Price']}\n"
    message += f"User: {user_name}\n\n"
    await bot.send_message(chat_id=channel_id, text=message)

async def main():
    scraped_data = await scrape_website()
    if scraped_data:
        
        for item in scraped_data:
           
            await send_to_telegram_channel(item, "<amhbooks>")

if __name__ == "main":
    asyncio.run(main())