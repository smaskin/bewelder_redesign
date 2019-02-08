from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from haystack import connections
from mixer.backend.django import mixer

from resumes.models import Resume


class ResumeSearchTestCase(TestCase):
    search_url = reverse('search:search')

    def setUp(self):
        mixer.cycle(5).blend(Resume, position='сварщик')
        mixer.cycle(3).blend(Resume, position='инженер')

        connections.reload('default')
        call_command('rebuild_index', interactive=False, verbosity=0)
        super().setUp()

    def test_search_view(self):
        resp = self.client.get(self.search_url)
        self.assertEqual(resp.status_code, 200)

    def test_search_query(self):
        resp = self.client.get(self.search_url, {'q': 'сварщик'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 5)
        self.assertEqual(resp.context['page'].object_list[0].content_type(), 'resumes.resume')

        resp = self.client.get(self.search_url, {'q': 'инженер'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 3)
        self.assertEqual(resp.context['page'].object_list[0].content_type(), 'resumes.resume')

        resp = self.client.get(self.search_url, {'q': 'директор'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 0)

    def test_realtime_update_search_index(self):
        resp = self.client.get(self.search_url, {'q': 'some position'})
        old_obj_count = len(resp.context['page'].object_list)

        mixer.blend(Resume, position='some position')

        resp = self.client.get(self.search_url, {'q': 'some position'})
        new_obj_count = len(resp.context['page'].object_list)
        self.assertEqual(new_obj_count, old_obj_count + 1)

    def test_search_only_resumes(self):
        resp = self.client.get(self.search_url, {'q': 'инженер', 'models': 'resumes.resume'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 3)
        self.assertEqual(resp.context['page'].object_list[0].content_type(), 'resumes.resume')
