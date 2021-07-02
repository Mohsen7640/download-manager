import requests

from time import sleep
from tqdm import tqdm
from math import log, floor, pow


def get_requests(url):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        return response

    return None


def is_downloadable(response):
    content_type = response.headers['Content-Type'].lower()
    if ('text' in content_type) or ('html' in content_type):
        return False
    return True


def get_filename(url):
    return url.split('/')[-1]


def change_scale(response, unit_size=1024):
    """
    Change 1024 bit to 1000 bit
    :param response:
    :param unit_size:
    :return:
    """
    total_bit = int(response.headers.get('Content-Length', 0))  # 1024

    # 1 KB ==> 1024 B , 1 KB ==> 1000 B
    if total_bit != 0:
        scale = floor(log(total_bit, unit_size))
        total_bit = (total_bit / pow(unit_size, scale)) * pow(1000, scale)

        return total_bit, scale
    return total_bit, 1


def download_manager(response, url, address=''):
    unit_size = 1024

    total_bit, scale = change_scale(response)

    progress_bar = tqdm(total=total_bit, unit_scale=True, unit='B')

    filename = get_filename(url)
    if not address:
        path = filename
    else:
        path = f'{address}/{filename}'

    with open(file=path, mode='wb') as file_handler:
        for chunk in response.iter_content(unit_size):
            size = (len(chunk) / pow(unit_size, scale)) * pow(1000, scale)
            progress_bar.update(size)
            file_handler.write(chunk)

    progress_bar.close()


if __name__ == '__main__':
    url_page = 'http://212.183.159.230/5MB.zip'
    respond = get_requests(url_page)

    if is_downloadable(response=respond):
        print('The file is downloadable')
        print('Please wait...')
        sleep(3)

        download_manager(
            response=respond,
            url=url_page,
        )

        print('File download completed')
    else:
        print('The file is not downloadable')
