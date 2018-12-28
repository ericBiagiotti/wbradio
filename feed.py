#!/usr/bin/env python

from feedgen.feed import FeedGenerator
from datetime import datetime
from datetime import timedelta
import boto
import http
import requests

URL = 'https://s3.amazonaws.com/ebiagiotti/wickedbites.rss'

def main():
    now = datetime.now()
    today_day_of_week = now.weekday()
    most_recent_sunday = now - timedelta(days=today_day_of_week+1)  # sunday is day 6

    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.id(URL)
    fg.title('Wicked Bites Radio')
    fg.category(term='Food')
    fg.language('en')
    fg.logo('http://www.nedine.com/wp-content/themes/wickedbites/images/logo.png')
    fg.link(href='http://www.nedine.com', rel='alternate')
    fg.link(href=URL, rel='self')
    fg.description('The Pat Whitley Restaurant Show')
    fg.podcast.itunes_category('Food')
    fg.podcast.itunes_summary('Pat Whitley Restaurant Show')
    fg.podcast.itunes_explicit('no')
    fg.podcast.itunes_new_feed_url(URL)
    fg.podcast.itunes_category('Arts', 'Food')
    fg.podcast.itunes_owner('Eric Biagiotti', 'eric.biagiotti@gmail.com')

    for i in range(10):
        datestamp = (most_recent_sunday - timedelta(weeks=i))
        url = 'http://www.nedine.com/Radio/Shows/%s.mp3' % datestamp.strftime('%m%d%y')

        r = requests.head(url)
        if r.status_code == 200:
            entry = fg.add_entry(order='append')
            entry.id(url)
            entry.title(datestamp.strftime('%m/%d/%Y'))
            entry.pubDate(datestamp.strftime('%Y-%m-%d 00:00:00 UTC'))
            entry.description(datestamp.strftime('Wicked Bites Radio show for %A, %B %e %Y'))
            entry.podcast.itunes_summary(datestamp.strftime('Wicked Bites Radio show for %A, %B %e %Y'))
            entry.enclosure(url, r.headers.get('Content-Length', 0), 'audio/mpeg')

    fg.rss_file('wickedbites.rss')
    
    s3_connection = boto.connect_s3()
    bucket = s3_connection.get_bucket('ebiagiotti')
    key = boto.s3.key.Key(bucket, 'wickedbites.rss')
    key.set_contents_from_filename('wickedbites.rss', policy='public-read')
    
if __name__ == '__main__':
    main()
