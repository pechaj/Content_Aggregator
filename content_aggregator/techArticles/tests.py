from django.test import TestCase
from django.utils import timezone
from .models import Article
from django.urls.base import reverse

# Create your tests here.
class ArticlesTests(TestCase):
    def setUp(self):
        self.Article = Article.objects.create(
            title = "First flying car!",
            desc = "It is indeed not flying",
            pubDate = timezone.now(),
            link = "https:////seznam.cz",
            author = "Bezos Jeffos",
            category = "Aviation",
            guid = "2126faf-5125dsag21229"
        )
        
    def test_show_contents(self):
        self.assertEqual(self.Article.desc, "It is indeed not flying")
        self.assertEqual(self.Article.author, "Bezos Jeffos")
        self.assertEqual(
            self.Article.guid,"2126faf-5125dsag21229"
        )
        
    def test_show_str_representation(self):
        self.assertEqual(
            str(self.Article),"First flying car! : Bezos Jeffos"
        )
        
    def test_home_pages_status_code(self):
        response = self.client.get("//")
        self.assertEqual(response.status_code, 200)
        
    def test_home_pages_uses_correct_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response,"homepage.html")
        
    def test_homepage_list_contents(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, "First flying car!")