import requests
import argparse
import time
import yaml

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--watchlist', type=str, default="", help='path to watchlist YAML file')
parser.add_argument('-k', '--makerkey', type=str, default="", help='IFTTT Maker key to trigger when any preorder goes live')
args = parser.parse_args()

watchlist = {}

SLEEP_TIME = 3

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
iftt_maker_url = 'https://maker.ifttt.com/trigger/'
iftt_maker_url_suffix = '/with/key/'

print 'Loading: \' ' + args.watchlist +'\''
with open(args.watchlist, 'r') as stream:
    try:
        watchlist = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit()

if len(watchlist) == 0:
    print 'No websites to watch. Exiting'
    exit()

active_watchlist = watchlist.copy()

print 'Preorder watcher started...'
while True:
    if len(active_watchlist) == 0:
        print 'All websites triggered. Exiting'
        exit()

    for website, metadata in watchlist.iteritems():
        if website not in active_watchlist.keys():
            continue
        url = metadata["url"]
        trigger = metadata["trigger"]

        try:
            print "requesting " + url   # FIXME
            r = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            continue    # ignore all exceptions

        trigger_found = r.text.find(trigger) > -1
        print "trigger_found " + str(trigger_found)   # FIXME

        if trigger_found:
            ifttt_notify_url = iftt_maker_url + website + iftt_maker_url_suffix + args.makerkey
            requests.post(args.channel)
            # Remove the website from the watchlist so we don't alert again
            active_watchlist.pop('website', None)

    time.sleep(SLEEP_TIME)
