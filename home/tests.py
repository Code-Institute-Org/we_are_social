from django.test import TestCase
from home.views import get_index
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from accounts.models import User


class HomePageTest(TestCase):

    def setUp(self):
        #print dir(User)
        super(HomePageTest, self).setUp()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('letmein')
        self.user.save()
        self.login = self.client.login(username='testuser',
                                       password='letmein')
        self.assertEqual(self.login, True)

    def test_home_page(self):
        home_page = resolve('/')
        self.assertEqual(home_page.func, get_index)

    def test_check_content_is_correct(self):
        home_page = self.client.get('/')
        self.assertTemplateUsed(home_page, "index.html")
        home_page_template_output = render_to_response("index.html", {'user': self.user}).content
        self.assertEquals(home_page.content, home_page_template_output)
