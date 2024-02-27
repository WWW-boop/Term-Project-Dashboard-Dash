import asyncio
from pyppeteer import launch

async def toggle_sidebar():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('YOUR_URL_HERE')  # เปลี่ยน URL เป็น URL ของเว็บไซต์ของคุณ

    # รอให้เว็บไซต์โหลดสมบูรณ์
    await page.waitForSelector('.sidebar')
    sidebar = await page.querySelector('.sidebar')

    toggle_btn = await page.querySelector('.toggle-btn')

    # คลิกปุ่ม toggle
    await toggle_btn.click()

    # รอสักครู่เพื่อให้มั่นใจว่าการเปลี่ยนแปลงมีผล
    await page.waitForTimeout(1000)

    # ตรวจสอบว่าคลาส 'active' ได้ถูกเพิ่มเข้าไปใน sidebar หรือไม่
    class_list = await page.evaluate('(element) => element.classList.toString()', sidebar)
    is_active = 'active' in class_list.split()

    print('Sidebar is active:', is_active)

    await browser.close()

asyncio.get_event_loop().run_until_complete(toggle_sidebar())
