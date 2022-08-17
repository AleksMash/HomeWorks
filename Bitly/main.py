import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['BITLINK_TOKEN']

parser = argparse.ArgumentParser(description='Returns clicks count for the given URL (short link)')
parser.add_argument('bitlink', help='URL (short link)')
args = parser.parse_args()

def shorten_link(token, url):
    headers = {
      'Authorization': f'Bearer {token}'
    }
    long_url = {"long_url": url}
    end_point = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(end_point, headers=headers, json=long_url)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, unschemed_link):
    headers = {
      'Authorization': f'Bearer {token}'
    }
    end_point = f'https://api-ssl.bitly.com/v4/'\
                f'bitlinks/{unschemed_link}/clicks/summary'
    response = requests.get(end_point, headers=headers)
    response.raise_for_status()
    json_data = response.json()
    return json_data['total_clicks']


def is_bitlink(token, unschemed_link):
    headers = {
      'Authorization': f'Bearer {token}'
    }
    end_point = f'https://api-ssl.bitly.com/v4/bitlinks/{unschemed_link}'
    response = requests.get(end_point, headers=headers)
    return response.ok


if __name__ == '__main__':
    #url = input('Input URL please : ').strip()
    url = args.bitlink
    parsed_bitlink = urlparse(url)
    unschemed_link = f'{parsed_bitlink.netloc}{parsed_bitlink.path}'
    if is_bitlink(TOKEN, unschemed_link):
        try:
            clicks_count = count_clicks(TOKEN, unschemed_link)
        except requests.exceptions.HTTPError as err:
            print('\nAn error occurred while processing url:\n\n', err)
        else:
            print(f'\nThe given URL a bitlink.'
            f'Total clicks count is {clicks_count}')
    else:
        try:
            bit_link = shorten_link(TOKEN, url)
        except requests.exceptions.HTTPError as err:
            print('\nAn error ocurred while processing url:\n\n', err)
        else:
            print(f'\nThe given URL is not a bitlink.'
            f'\nGenereted bitlink for it is: {bit_link}')
