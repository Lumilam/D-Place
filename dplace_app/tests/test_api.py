__author__ = 'dan'

from dplace_app.models import *
from django.contrib.gis.geos import Polygon, Point
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from django.core.urlresolvers import reverse


class ISOCodeAPITestCase(APITestCase):
    '''
    Tests rest-framework API.  Verifies a single ISO code created can be fetched with
    HTTP 200
    '''
    def setUp(self):
        self.code = ISOCode.objects.create(iso_code='abc',location=Point(5.0,5.0))
    def test_isocode_api(self):
        url = reverse('isocode-list')
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = response.data
        self.assertEqual(response_dict['count'],1)
        self.assertEqual(response_dict['results'][0]['iso_code'],self.code.iso_code)

class FindSocietiesTestCase(APITestCase):
    '''
    Tests the find societies API
    Responses will be serialized SocietyResult objects
    '''
    def setUp(self):
        # make two societies
        iso_code1 = ISOCode.objects.create(iso_code='abc',location=Point(1.0,1.0))
        iso_code2 = ISOCode.objects.create(iso_code='def',location=Point(2.0,2.0))
        iso_code3 = ISOCode.objects.create(iso_code='ghi',location=Point(3.0,3.0))
        # Make languages
        self.language1 = Language.objects.create(name='language1',iso_code=iso_code1)
        self.language2 = Language.objects.create(name='language2',iso_code=iso_code2)
        self.language3 = Language.objects.create(name='language3',iso_code=iso_code3)

        self.society1 = Society.objects.create(ext_id='society1',name='Society1',location=Point(1.0,1.0),source='EA',iso_code=iso_code1,language=self.language1)
        self.society2 = Society.objects.create(ext_id='society2',name='Society2',location=Point(2.0,2.0),source='EA',iso_code=iso_code2,language=self.language2)
        # Society 3 has the same language characteristics as society 1 but different EA Vars
        self.society3 = Society.objects.create(ext_id='society3',name='Society3',location=Point(3.0,3.0),source='EA',iso_code=iso_code3,language=self.language3)

        # make a language class tree
        self.root_language_class = LanguageClass.objects.create(name='root',level=1,parent=None)
        self.parent_language_class_1 = LanguageClass.objects.create(name='parent1',level=2,parent=self.root_language_class)
        self.child_language_class_1a = LanguageClass.objects.create(name='child1',level=3,parent=self.parent_language_class_1)
        self.child_language_class_1b = LanguageClass.objects.create(name='child1',level=3,parent=self.parent_language_class_1)
        self.parent_language_class_2 = LanguageClass.objects.create(name='parent2',level=2,parent=self.root_language_class)
        self.child_language_class_2 = LanguageClass.objects.create(name='child2',level=3,parent=self.parent_language_class_2)

        # make language classifications to link a language to its class tree
        lc1 = LanguageClassification.objects.create(language=self.language1,
                                                    ethnologue_classification='lc1',
                                                    class_family=self.root_language_class,
                                                    class_subfamily=self.parent_language_class_1,
                                                    class_subsubfamily=self.child_language_class_1a)
        lc2 = LanguageClassification.objects.create(language=self.language2,
                                                    ethnologue_classification='lc2',
                                                    class_family=self.root_language_class,
                                                    class_subfamily=self.parent_language_class_2,
                                                    class_subsubfamily=self.child_language_class_2)
        lc3 = LanguageClassification.objects.create(language=self.language3,
                                                    ethnologue_classification='lc3',
                                                    class_family=self.root_language_class,
                                                    class_subfamily=self.parent_language_class_1,
                                                    class_subsubfamily=self.child_language_class_1b)
        # Make an EA Variable, code, and value
        variable = VariableDescription.objects.create(label='EA001',name='Variable 1')
        self.code1 = VariableCodeDescription.objects.create(variable=variable, code='1', description='Code 1')
        self.code2 = VariableCodeDescription.objects.create(variable=variable, code='2', description='Code 2')
        self.code3 = VariableCodeDescription.objects.create(variable=variable, code='3', description='Code 3')
        value1 = VariableCodedValue.objects.create(variable=variable,society=self.society1,coded_value='1',code=self.code1)
        value2 = VariableCodedValue.objects.create(variable=variable,society=self.society2,coded_value='2',code=self.code2)
        # Setup environmentals
        self.environmental1 = Environmental.objects.create(society=self.society1,
                                                           reported_location=Point(0,0),
                                                           actual_location=Point(0,0),
                                                           iso_code=iso_code1)
        self.environmental2 = Environmental.objects.create(society=self.society2,
                                                           reported_location=Point(1,1),
                                                           actual_location=Point(1,1),
                                                           iso_code=iso_code2)

        self.environmental_variable1 = EnvironmentalVariable.objects.create(name='precipitation',
                                                                            units='mm')
        self.environmental_value1 = EnvironmentalValue.objects.create(variable=self.environmental_variable1,
                                                                      value=1.0,
                                                                      environmental=self.environmental1)
        self.environmental_value2 = EnvironmentalValue.objects.create(variable=self.environmental_variable1,
                                                                      value=2.0,
                                                                      environmental=self.environmental2)

        self.url = reverse('find_societies')
    def assertSocietyInResponse(self,society,response):
        response_society_ids = [x['society']['id'] for x in response.data['results']]
        return self.assertIn(society.id, response_society_ids)
    def assertSocietyNotInResponse(self,society,response):
        response_society_ids = [x['society']['id'] for x in response.data['results']]
        return self.assertNotIn(society.id, response_society_ids)
    def test_find_societies_by_language(self):
        # Find the societies that use language1
        language_ids = [self.language1.id]
        data = {'language_filters' : [{'language_ids': language_ids }]}
        response = self.client.post(self.url,data,format='json')
        self.assertSocietyInResponse(self.society1,response)
        self.assertSocietyNotInResponse(self.society2,response)
        self.assertSocietyNotInResponse(self.society3,response)
    def test_find_society_by_var(self):
        data = {'variable_codes': [self.code1.pk]}
        response = self.client.post(self.url,data,format='json')
        self.assertSocietyInResponse(self.society1,response)
        self.assertSocietyNotInResponse(self.society2,response)
    def test_find_societies_by_var(self):
        data = {'variable_codes': [self.code1.pk, self.code2.pk]}
        response = self.client.post(self.url,data,format='json')
        self.assertSocietyInResponse(self.society1,response)
        self.assertSocietyInResponse(self.society2,response)
    def test_find_no_societies(self):
        data = {'variable_codes': [self.code3.pk]}
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(len(response.data['results']),0)
    def test_find_society_by_language_and_var(self):
        # Search for societies with language1 and language 3
        # Coded with variable codes 1 and 2
        # this should return only 1 and not 2 or 3
        # This tests that results should be intersection (AND), not union (OR)
        # Society 3 is not coded for any variables, so it should not appear in the list.
        language_ids = [self.language1.id, self.language3.id]
        data = {'variable_codes': [self.code1.pk, self.code2.pk],
                'language_filters' : [{'language_ids': language_ids }]}
        response = self.client.post(self.url,data,format='json')
        self.assertSocietyInResponse(self.society1,response)
        self.assertSocietyNotInResponse(self.society2,response)
        self.assertSocietyNotInResponse(self.society3,response)
    def test_empty_response(self):
        response = self.client.post(self.url,{},format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']),0)
    def test_find_by_environmental_filter_gt(self):
        data = {'environmental_filters': [{'id': str(self.environmental_variable1.pk),
                                           'operator': 'gt', 'params': ['1.5']}]}
        response = self.client.post(self.url,data,format='json')
        self.assertSocietyNotInResponse(self.society1,response)
        self.assertSocietyInResponse(self.society2,response)
    def test_find_by_environmental_filter_lt(self):
        data = {'environmental_filters': [{'id': str(self.environmental_variable1.pk),
                                           'operator': 'lt', 'params': ['1.5']}]}
        response = self.client.post(self.url,data,format='json')
        self.assertSocietyInResponse(self.society1,response)
        self.assertSocietyNotInResponse(self.society2,response)
    def test_find_by_environmental_filter_inrange(self):
        data = {'environmental_filters': [{'id': str(self.environmental_variable1.pk),
                                           'operator': 'inrange', 'params': ['0.0','1.5']}]}
        response = self.client.post(self.url,data,format='json')
        self.assertSocietyInResponse(self.society1,response)
        self.assertSocietyNotInResponse(self.society2,response)
    def test_find_by_environmental_filter_outrange(self):
        data = {'environmental_filters': [{'id': str(self.environmental_variable1.pk),
                                           'operator': 'outrange', 'params': ['0.0','3.0']}]}
        response = self.client.post(self.url,data,format='json')
        self.assertSocietyNotInResponse(self.society1,response)
        self.assertSocietyNotInResponse(self.society2,response)
