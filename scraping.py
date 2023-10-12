from bs4 import BeautifulSoup

from config import URL
from data_base import db
from utils import validate_request, format_phone_number
from web_driver import get_page_html, driver


class AutoRiaScraping:

    @staticmethod
    def get_number_of_pages(html: str) -> int | None:
        validate = validate_request(url=html)
        if validate is not None:
            auto_ria_html = BeautifulSoup(validate.text, 'html.parser')
            number_of_pages = auto_ria_html.findAll('a', class_="page-link")
            return int(number_of_pages[-2].text.replace(' ', ''))

    @staticmethod
    def get_urls_list(html: str) -> list:
        html = BeautifulSoup(html, 'html.parser')
        return html.findAll(class_='m-link-ticket')

    @staticmethod
    def get_html(html: str) -> BeautifulSoup:
        return BeautifulSoup(html, 'html.parser')

    @staticmethod
    def get_title(html: BeautifulSoup) -> str | None:
        title = html.find('h1')
        if title is not None:
            return title.text.strip()

    @staticmethod
    def get_price(html: BeautifulSoup) -> int | None:
        auto_price = html.find('strong')
        if auto_price is not None:
            auto_price = [i for i in auto_price.text if i.isdigit()]
            return int(''.join(auto_price))

    @staticmethod
    def get_odometer(html: BeautifulSoup) -> int | None:
        auto_odometer = html.find('div', class_="base-information bold")
        if auto_odometer is not None:
            if 'тис.' in auto_odometer.text:
                return int(''.join([i for i in auto_odometer.text if i.isdigit()]) + '000')
            else:
                return int(''.join([i for i in auto_odometer.text if i.isdigit()]))

    @staticmethod
    def get_name(html: BeautifulSoup) -> str | None:
        name = html.find('div', class_="seller_info_name")
        if name is None:
            return html.find('h4', class_="seller_info_name").text.strip()
        else:
            return name.text.strip()

    @staticmethod
    def get_phone(html: BeautifulSoup) -> list | None:
        phones = html.find('div', class_="list-phone").findAll('a')
        if phones is not None:
            return [i.text for i in phones]

    @staticmethod
    def get_image(html: BeautifulSoup) -> str | None:
        auto_img = html.find('img', class_="outline m-auto").get('src')
        if auto_img is not None:
            return auto_img

    @staticmethod
    def get_count_image(html: BeautifulSoup) -> int | None:
        auto_img = html.find('span', class_="mhide")
        if auto_img is not None:
            return int(''.join([i for i in auto_img.text if i.isdigit()]))

    @staticmethod
    def get_vin_code(html: BeautifulSoup) -> str | None:
        vin = html.find('span', class_="vin-code")
        if vin is not None:
            return vin.text
        else:
            vin = html.find('span', class_="label-vin")
            if vin is not None:
                return vin.text

    @staticmethod
    def get_number(html: BeautifulSoup) -> str | None:
        auto_number = html.find('span', class_="state-num ua")
        if auto_number is not None:
            return auto_number.text[:10]


def scraping_auto_ria(start_page: int, stop_page: int = AutoRiaScraping.get_number_of_pages(html=URL)):
    print(f'Start page: {start_page}, Stop page: {stop_page}')
    for n in range(start_page, stop_page):
        request = validate_request(url=f'{URL}?page={n}')
        if request is not None:
            urls_list = AutoRiaScraping.get_urls_list(html=request.text)
            print(f'Page: {n}')

            for url in urls_list:
                url = url.get('href')
                try:
                    html_data = get_page_html(url=url, sleep=1)

                    html_data = AutoRiaScraping.get_html(html=html_data)
                    title = AutoRiaScraping.get_title(html=html_data)
                    price_usd = AutoRiaScraping.get_price(html=html_data)
                    odometer = AutoRiaScraping.get_odometer(html=html_data)
                    username = AutoRiaScraping.get_name(html=html_data)
                    phone_number = format_phone_number(phone_list=AutoRiaScraping.get_phone(html=html_data))
                    image_url = AutoRiaScraping.get_image(html=html_data)
                    images_count = AutoRiaScraping.get_count_image(html=html_data)
                    car_number = AutoRiaScraping.get_number(html=html_data)
                    car_vin = AutoRiaScraping.get_vin_code(html=html_data)

                    print('\nURL: ', url,
                          '\nTitle: ', title,
                          '\nPrice: ', price_usd,
                          '\nOdometer: ', odometer,
                          '\nUser Name: ', username,
                          '\nPhone: ', *phone_number,
                          '\nImage URL: ', image_url,
                          '\nImages count: ', images_count,
                          '\nCar Number: ', car_number,
                          '\nCar VIN: ', car_vin, '\n')
                    db.add_auto(
                        url=url,
                        title=title,
                        price_usd=price_usd,
                        odometer=odometer,
                        username=username,
                        phone_number=phone_number,
                        image_url=image_url,
                        images_count=images_count,
                        car_number=car_number,
                        car_vin=car_vin,
                    )

                except Exception as e:
                    print(e)
                    continue
    driver.quit()
