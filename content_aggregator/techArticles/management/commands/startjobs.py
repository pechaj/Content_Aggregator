# Standard Library
import logging

# Django
from django.core.management.base import BaseCommand
from django.conf import settings

# Third Party
import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# Models
from techArticles.models import Article

logger = logging.getLogger(__name__)

def save_new_episodes(feed):
    """Saves new episodes to the database.

    Checks the episode GUID against the episodes currently stored in the
    database. If not found, then a new `Episode` is added to the database.

    Args:
        feed: requires a feedparser object
    """
    article_title = feed.channel.title

    for item in feed.entries:
        if not Article.objects.filter(guid=item.guid).exists():
            article = Article(
                title = item.title,
                desc = item.description,
                pubDate = parser.parse(item.published),
                link = item.link,
                author = item.author,
                category = item.category,
                guid = item.guid,
            )
            article.save()
def fetch_techcrunch_articles():
    _feed = feedparser.parse("https://techcrunch.com/feed/")
    save_new_episodes(_feed)
    
def fetch_wired_articles():
    _feed = feedparser.parse("https://www.wired.com/feed/tag/ai/latest/rss")
    save_new_episodes(_feed)

def delete_old_job_executions(max_age=604800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
    
class Command(BaseCommand):
    help = "Runs apscheduler."
    
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        scheduler.add_job(
            fetch_techcrunch_articles,
            trigger = "interval",
            minutes = 2,
            id = "TechCrunch",
            max_instances = 1,
            replace_existing = True,
        )
        logger.info("Added job: TechCrunch")
        
        scheduler.add_job(
            fetch_wired_articles,
            trigger = "interval",
            minutes = 2,
            id = "Wired Articles",
            max_instances = 1,
            replace_existing = True,
        )
        logger.info("Added job: Wired Articles")
        
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")