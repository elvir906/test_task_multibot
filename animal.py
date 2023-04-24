from weather import requests

URL = 'https://api.thecatapi.com/v1/images/search'


def get_new_image():
    """
    Метод для получения рандомных картинки с изображением котиков.
    В случае ошибки, пытается получить изображение пёселей.
    """
    try:
        response = requests.get(URL)
    except Exception as error:
        print(error)
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat
