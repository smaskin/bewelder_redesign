from django.test import TestCase
from django.contrib.auth import get_user_model

from mixer.backend.django import mixer

from orgs.models import Employer, City, Region
from vacancies.models import Vacancy


User = get_user_model()


class RegionModelTestCase(TestCase):
    def setUp(self):
        self.region_1 = Region.objects.create(name='Region 1')

    def test_str_region(self):
        expected = 'Region 1'
        result = str(self.region_1)
        self.assertEqual(expected, result)


class CityModelTestCase(TestCase):
    def setUp(self):
        self.region_1 = Region.objects.create(name='Region 1')
        self.city_1 = City.objects.create(name='City 1', region=self.region_1)

    def test_str_city(self):
        self.assertEqual(str(self.city_1), self.city_1.name_with_region)

    def test_name_with_region(self):
        expected = 'City 1 (Region 1)'
        result = str(self.city_1)
        self.assertEqual(expected, result)


class EmployerModelTestCase(TestCase):
    def setUp(self):
        self.region_1 = Region.objects.create(name='Region 1')
        self.city_1 = City.objects.create(name='City 1', region=self.region_1)
        self.employer_data = {
            'name': 'Employer 1',
            'inn': '123456789012',
            'city': self.city_1,
            'phone': '123',
            'email': 'test@email.local',
            'user': mixer.blend(User),
        }
        self.employer_1 = Employer.objects.create(**self.employer_data)

    def test_str_employer(self):
        self.assertEqual(str(self.employer_1), self.employer_1.name_with_city)

    def test_name_with_city(self):
        expected = 'Employer 1 (City 1)'
        result = self.employer_1.name_with_city
        self.assertEqual(expected, result)

    def test_creation_short_name(self):
        self.assertEqual(self.employer_1.name, self.employer_1.short_name)
        self.employer_data['name'] = 'Employer 2'
        self.employer_data['short_name'] = 'Emp. 2'
        self.employer_data['user'] = mixer.blend(User)
        employer_2 = Employer.objects.create(**self.employer_data)
        self.assertEqual(self.employer_1.name, self.employer_1.short_name)
        self.assertNotEqual(employer_2.name, employer_2.short_name)

    def test_same_name_employers_another_city_creation_succeed(self):
        city_2 = City.objects.create(name='City 2', region=self.region_1)
        self.employer_data['city'] = city_2
        self.employer_data['user'] = mixer.blend(User)
        employer_2 = Employer.objects.create(**self.employer_data)
        self.assertEqual(self.employer_1.name, employer_2.name)
        self.assertEqual(self.employer_1.short_name, employer_2.short_name)
        self.assertEqual(city_2.name, employer_2.city.name)

    def test_get_vacancy_count(self):
        mixer.cycle(2).blend(Vacancy, employer=self.employer_1)
        self.assertEqual(2, self.employer_1.get_vacancy_count())

    def test_get_absolute_url(self):
        result = self.employer_1.get_absolute_url()
        self.assertEqual(result, '/orgs/{}/'.format(self.employer_1.id))
