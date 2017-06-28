import requests
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', type=str, default="", help='URL to spam')
parser.add_argument('-c', '--channel', type=str, default="", help='IFTTT Maker channel to ping when the preorder goes live')
args = parser.parse_args()

TRIGGER_STRING = 'data-button-state-id="PRE_ORDER"'
SLEEP_TIME = 30
NUM_PINGS = 1

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}

numPings = 0

print 'Best Buy Watcher started...'
while True:
    r = requests.get(args.url, headers=headers)
    active = r.text.find(TRIGGER_STRING) > -1
    if active:
        requests.post(args.channel)
        numPings += 1
        if numPings == NUM_PINGS:
            exit()
    else:
        numPings = 0
    time.sleep(SLEEP_TIME)
