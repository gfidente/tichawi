from django.core.management.base import BaseCommand
from django.utils import timezone
from planet.models import Category, Feed, Article

import feedparser
import logging

# needed to convert 9tuple or int into datetime
from calendar import timegm
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
success_states = [200, 203, 300, 301, 302, 307]
feed_required = ["id", "title", "updated_parsed", "link"]
article_required = ["id", "title", "updated_parsed", "link"]


class Command(BaseCommand):
    help = "Updates articles from feeds"

    def handle(self, *args, **options):
        now = timezone.now()
        for feed in Feed.objects.all():
            ### feed data population
            logger.info("working on %s", feed.url)

            parsed_feed = feedparser.parse(feed.url)
            if parsed_feed.status not in success_states:
                logger.warning("skipping, invalid reponse status %s", parsed_feed.status)
                continue

            if not set(parsed_feed.feed.keys()).issuperset(set(feed_required)):
                logger.warning("skipping, required data unavailable")
                continue

            feed_update_time = datetime.fromtimestamp(timegm(parsed_feed.feed.updated_parsed), timezone.utc)
            last_update_time = feed.last_update_time
            if feed_update_time <= last_update_time:
                logger.info("skipping, does not seem to have been updated after our last visit")
                continue

            if "image" in parsed_feed.feed.keys():
                feed.img_url = parsed_feed.feed.image.href
            feed.source_url = parsed_feed.feed.link
            feed.fid = parsed_feed.feed.id
            feed.title = parsed_feed.feed.title
            feed.last_update_time = now
            feed.save()

            ### articles data population
            added = 0
            skipped = 0
            for entry in parsed_feed.entries:
                logger.debug("inspecting article %s", entry.link)

                if not set(entry.keys()).issuperset(set(article_required)):
                    logger.warning("skipping, required data unavailable")
                    skipped += 1
                    continue

                entry_update_time = datetime.fromtimestamp(timegm(entry.updated_parsed), timezone.utc)

                if entry_update_time <= last_update_time:
                    logger.info("skipping, does not seem to have been updated after our last visit")
                    skipped += 1
                    continue

                entry_content = ""
                if "content" in entry.keys() and len(entry.content) > 0:
                    for content in entry.content:
                        entry_content += content.value
                elif "summary" in entry.keys():
                    entry_content = entry.summary
                else:
                    logger.info("skipping, content and summary seem to be missing")
                    skipped += 1
                    continue
                entry_content = entry_content.encode("ascii", "ignore")

                article = Article()
                try:
                    article = Article.objects.get(aid=entry.id)
                except Article.DoesNotExist:
                    logger.debug("inserting new article %s", entry.link)

                article.feed_id = feed.id
                article.url = entry.link
                article.pub_time = entry_update_time
                article.aid = entry.id
                article.title = entry.title
                article.last_update_time = now
                article.content = entry_content
                article.summary = entry.summary
                if not article.score:
                    article.score = 110
                    article.score_update_time = now
                article.save()
                added += 1

            logger.info("found %s articles, skipped %s, added %s", len(parsed_feed.entries), skipped, added)

        ### cleanup old entries
        ago = datetime.today()-timedelta(days=30)
        aremoved = 0
        for article in Article.objects.filter(score=100, score_update_time__lt=ago):
            logger.warning("removing article %s", article.link)
            article.delete()
            aremoved += 1
        logger.info("deleted %s articles", aremoved)
