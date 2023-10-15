from bs4 import BeautifulSoup

from configs.auto_ria_config import URL
from utils.auto_ria_utils import validate_request, format_phone_number
from web_drivers.auto_ria_web_driver import AutoRiaWebDriver


class AutoRiaScraping:

    @staticmethod
    def get_count_of_the_pages(html: str) -> int | None:
        """ Search for the count of the pages """
        validate = validate_request(url=html)
        if validate is not None:
            auto_ria_html = BeautifulSoup(validate.text, 'html.parser')
            number_of_pages = auto_ria_html.findAll('a', class_="page-link")
            return int(number_of_pages[-2].text.replace(' ', ''))

    @staticmethod
    def get_urls_of_the_cars_list(html: str) -> list:
        """ Search for the URLs of the cars on the page """
        html = BeautifulSoup(html, 'html.parser')
        return html.findAll(class_='m-link-ticket')

    @staticmethod
    def get_html_data(html: str) -> BeautifulSoup:
        """ Getting the HTML data from the page """
        return BeautifulSoup(html, 'html.parser')

    @staticmethod
    def get_title(html: BeautifulSoup) -> str | None:
        """ Search for the title of the car """
        title = html.find('h1')
        if title is not None:
            return title.text.strip()

    @staticmethod
    def get_price_usd(html: BeautifulSoup) -> int | None:
        """ Search for the value of the price """
        auto_price = html.find('strong')
        if auto_price is not None:
            auto_price = [i for i in auto_price.text if i.isdigit()]
            return int(''.join(auto_price))

    @staticmethod
    def get_odometer(html: BeautifulSoup) -> int | None:
        """ Search for the value of the odometer """
        auto_odometer = html.find('div', class_="base-information bold")
        if auto_odometer is not None:
            if 'тис.' in auto_odometer.text:
                return int(''.join([i for i in auto_odometer.text if i.isdigit()]) + '000')
            else:
                return int(''.join([i for i in auto_odometer.text if i.isdigit()]))

    @staticmethod
    def get_username(html: BeautifulSoup) -> str | None:
        """ Search for the username """
        name = html.find('div', class_="seller_info_name")
        if name is None:
            return html.find('h4', class_="seller_info_name").text.strip()
        else:
            return name.text.strip()

    @staticmethod
    def get_phone_number(html: BeautifulSoup) -> list | None:
        """ Search for the phone number of the user """
        phones = html.find('div', class_="list-phone").findAll('a')
        if phones is not None:
            return [i.text for i in phones]

    @staticmethod
    def get_image_url(html: BeautifulSoup) -> str | None:
        """ Search for the image URL """
        auto_img = html.find('img', class_="outline m-auto").get('src')
        if auto_img is not None:
            return auto_img

    @staticmethod
    def get_images_count(html: BeautifulSoup) -> int | None:
        """ Search for the count of the images """
        auto_img = html.find('span', class_="mhide")
        if auto_img is not None:
            return int(''.join([i for i in auto_img.text if i.isdigit()]))

    @staticmethod
    def get_car_number(html: BeautifulSoup) -> str | None:
        """ Search for the number of the car """
        auto_number = html.find('span', class_="state-num ua")
        if auto_number is not None:
            return auto_number.text[:10]

    @staticmethod
    def get_car_vin(html: BeautifulSoup) -> str | None:
        """ Search for the VIN code of the car """
        vin = html.find('span', class_="vin-code")
        if vin is not None:
            return vin.text
        else:
            vin = html.find('span', class_="label-vin")
            if vin is not None:
                return vin.text

    @staticmethod
    def start_scraping_auto_ria(db, start_page: int, stop_page: int = 0):
        """ A general method for scraping the AutoRia site """
        driver = AutoRiaWebDriver(time_to_sleep=1)
        stop_page = stop_page if stop_page != 0 else AutoRiaScraping.get_count_of_the_pages(html=URL)
        print(f'Start page: {start_page}, Stop page: {stop_page}')

        for i in range(start_page, stop_page):
            request = validate_request(url=f'{URL}?page={i}')
            if request is not None:
                urls_list = AutoRiaScraping.get_urls_of_the_cars_list(html=request.text)
                print(f'Page: {i}')

                for url in urls_list:
                    url = url.get('href')

                    try:
                        html_data = AutoRiaScraping.get_html_data(html=driver.get_html(url=url))
                        title = AutoRiaScraping.get_title(html=html_data)
                        price_usd = AutoRiaScraping.get_price_usd(html=html_data)
                        odometer = AutoRiaScraping.get_odometer(html=html_data)
                        username = AutoRiaScraping.get_username(html=html_data)
                        phone_number = AutoRiaScraping.get_phone_number(html=html_data)
                        phone_number = format_phone_number(phone_list=phone_number)
                        image_url = AutoRiaScraping.get_image_url(html=html_data)
                        images_count = AutoRiaScraping.get_images_count(html=html_data)
                        car_number = AutoRiaScraping.get_car_number(html=html_data)
                        car_vin = AutoRiaScraping.get_car_vin(html=html_data)

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

                        db.add_auto_to_auto_ria_table(
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

        driver.driver.quit()
