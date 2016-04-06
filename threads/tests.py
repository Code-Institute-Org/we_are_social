from django.test import TestCase
from django.shortcuts import render_to_response
from .models import Subject
import difflib


class SubjectPageTest(TestCase):

    fixtures = ['subjects']

    def test_check_content_is_correct(self):
        subject_page = self.client.get('/forum/')
        self.assertTemplateUsed(subject_page, "forum/forum.html")
        subject_page_template_output = render_to_response("forum/forum.html",
                                                          {'subjects': Subject.objects.all()}).content
        self.assertEquals(subject_page.content, subject_page_template_output)
