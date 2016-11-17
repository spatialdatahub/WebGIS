from django.test import TestCase
from django.shortcuts import reverse

from .base import BaseDatasetTest

from datasets.models import Dataset

from datasets.forms import DatasetForm

from datasets.views import AboutView
from datasets.views import ContactView
from datasets.views import DatasetCreateView
from datasets.views import DatasetDetailView
from datasets.views import DatasetRemoveView
from datasets.views import DatasetUpdateView
from datasets.views import load_dataset
from datasets.views import PortalView

from cryptography.fernet import Fernet
import os



class AboutViewTests(BaseDatasetTest):

    def test_about_url_resolves_to_AboutView(self):
        request = self.factory.get('')
        response = AboutView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_AboutView_uses_correct_template(self):
        response = self.client.get(reverse('datasets:about'))
        self.assertTemplateUsed(response,
            template_name="datasets/about.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_AboutView_url_title_is_correct(self):
        response = self.client.get(reverse('datasets:about'))
        self.assertIn('<title>ZMT | About</title>', response.content.decode('utf-8'))



class ContactViewTests(BaseDatasetTest):

    def test_ContactView_url_resolves_to_ContactView(self):
        request = self.factory.get('')
        response = ContactView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_ContactView_uses_correct_template(self):
        response = self.client.get(reverse('datasets:contact'))
        self.assertTemplateUsed(response,
            template_name="datasets/contact.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_ContactView_url_title_is_correct(self):
        response = self.client.get(reverse('datasets:contact'))
        self.assertIn('<title>ZMT | Contact</title>', response.content.decode('utf-8'))



class DatasetCreateViewTests(BaseDatasetTest):

    def test_DatasetCreateView_redirects_to_login_without_authentication(self):
        response = self.client.get(reverse('datasets:new_dataset'))
        expected_redirect ='/accounts/login/?next=/new_dataset/'
        self.assertRedirects(response, expected_redirect)

    def test_DatasetCreateView_url_resolves_to_DatasetCreateView(self):
        request = self.factory.get('')
        request.user = self.test_user
        response = DatasetCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_DatasetCreateView_uses_correct_template(self):
        self.client.login(username='test_user', password='testuserpassword')
        response = self.client.get(reverse('datasets:new_dataset'))
        self.assertTemplateUsed(response,
            template_name="datasets/new_dataset.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_dataset_DatasetCreateView_url_title_is_correct(self):
        self.client.login(username='test_user', password='testuserpassword')
        response = self.client.get(reverse('datasets:new_dataset'))
        self.assertIn('<title>ZMT | Add Dataset</title>', response.content.decode('utf-8'))

    def test_DatasetCreateView_uses_DatasetForm(self):
        self.client.login(username='test_user', password='testuserpassword')
        response = self.client.get(reverse('datasets:new_dataset'))
        self.assertIsInstance(response.context['form'], DatasetForm)



class DatasetDetailViewTests(BaseDatasetTest):

    def test_DatasetDetailView_url_resolves_to_DatasetDetailView(self):
        request = self.factory.get('')
        response = DatasetDetailView.as_view()(request,
                                               slug=self.ds1.slug,
                                               pk=self.ds1.pk)
        self.assertEqual(response.status_code, 200)

    def test_DatasetDetailView_uses_correct_template(self):
        response = self.client.get(reverse('datasets:dataset_detail',
            kwargs={'slug': self.ds1.slug, 'pk': self.ds1.pk}))
        self.assertTemplateUsed(response,
            template_name="datasets/dataset_detail.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_DatasetDetailView_url_title_is_correct(self):
        response = self.client.get(reverse('datasets:dataset_detail',
            kwargs={'slug': self.ds1.slug, 'pk': self.ds1.pk}))
        self.assertIn('<title>ZMT | %s</title>' % self.ds1.title, response.content.decode('utf-8'))

    def test_dataset_AUTHOR_is_in_the_page(self):
        response = self.client.get(reverse('datasets:dataset_detail',
            kwargs={'slug': self.ds2.slug, 'pk': self.ds2.pk}))
        self.assertIn(self.ds2.author, response.content.decode("utf-8"))

    def test_dataset_TITLE_is_in_the_page(self):
        response = self.client.get(reverse('datasets:dataset_detail',
            kwargs={'slug': self.ds2.slug, 'pk': self.ds2.pk}))
        self.assertIn(self.ds2.title, response.content.decode("utf-8"))

    def test_dataset_DESCRIPTION_is_in_the_page(self):
        response = self.client.get(reverse('datasets:dataset_detail',
            kwargs={'slug': self.ds2.slug, 'pk': self.ds2.pk}))
        self.assertIn(self.ds2.description, response.content.decode("utf-8"))

    def test_password_protected_dataset_does_not_have_user_password_in_final_stage(self):
        response = self.client.get(reverse('datasets:dataset_detail',
            kwargs={'slug': self.ds3.slug, 'pk': self.ds3.pk}))
        self.assertNotIn(self.ds3.dataset_password, response.content.decode("utf-8"))
        self.assertNotIn(self.ds3.dataset_password, response.context)

    def test_that_DatasetDetailView_brings_in_correct_dataset_object(self):
        response = self.client.get(reverse('datasets:dataset_detail',
            kwargs={'slug': self.ds1.slug, 'pk': self.ds1.pk}))
        self.assertEqual(self.ds1, response.context['dataset'])
        self.assertNotEqual(self.ds2, response.context['dataset'])



class DatasetRemoveViewTests(BaseDatasetTest):

    def test_DatasetRemoveView_redirects_to_login_without_authentication(self):
        response = self.client.get(reverse('datasets:dataset_remove',
            kwargs={'slug': self.ds1.slug, 'pk': self.ds1.pk}))
        expected_redirect ='/accounts/login/?next=/{}-{}/remove/'.format(self.ds1.slug, self.ds1.pk)
        self.assertRedirects(response, expected_redirect)

    def test_DatasetRemoveView_url_resolves_to_DatasetRemoveView(self):
        request = self.factory.get('')
        request.user = self.test_user
        response = DatasetRemoveView.as_view()(request,
                                               slug=self.ds1.slug,
                                               pk=self.ds1.pk)
        self.assertEqual(response.status_code, 200)

    def test_DatasetRemoveView_uses_correct_template(self):
        self.client.login(username='test_user', password='testuserpassword')
        response = self.client.get(reverse('datasets:dataset_remove',
            kwargs={'slug': self.ds1.slug, 'pk': self.ds1.pk}))
        self.assertTemplateUsed(response,
            template_name="datasets/dataset_remove.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_DatasetRemoveView_url_title_is_correct(self):
        self.client.login(username='test_user', password='testuserpassword')
        response = self.client.get(reverse('datasets:dataset_remove',
            kwargs={'slug': self.ds1.slug, 'pk': self.ds1.pk}))
        self.assertIn('<title>ZMT | Remove Dataset</title>', response.content.decode('utf-8'))

    def test_that_DatasetRemoveView_brings_in_correct_dataset_object(self):
        self.client.login(username='test_user', password='testuserpassword')
        response = self.client.get(reverse('datasets:dataset_remove',
            kwargs={'slug': self.ds1.slug, 'pk': self.ds1.pk}))
        self.assertEqual(self.ds1, response.context['dataset'])
        self.assertNotEqual(self.ds2, response.context['dataset'])



class DatasetUpdateViewTests(BaseDatasetTest):

    def test_DatasetUpdateView_redirects_to_login_without_authentication(self):
        response = self.client.get(reverse('datasets:dataset_update',
            kwargs={'slug': self.ds1.slug, 'pk': self.ds1.pk}))
        expected_redirect ='/accounts/login/?next=/{}-{}/update/'.format(self.ds1.slug, self.ds1.pk)
        self.assertRedirects(response, expected_redirect)

    def test_DatasetUpdateView_url_resolves_to_DatasetUpdateView(self):
        request = self.factory.get('')
        request.user = self.test_user
        response = DatasetUpdateView.as_view()(request,
                                               slug=self.ds1.slug,
                                               pk=self.ds1.pk)
        self.assertEqual(response.status_code, 200)

    def test_DatasetUpdateView_url_title_is_correct(self):
        self.client.login(username='test_user', password='testuserpassword')
        response = self.client.get(reverse('datasets:dataset_update',
            kwargs={'slug': self.ds1.slug, 'pk': self.ds1.pk}))
        self.assertIn('<title>ZMT | Update %s</title>' % self.ds1.title, response.content.decode('utf-8'))

    def test_DatasetUpdateView_uses_correct_template(self):
        self.client.login(username='test_user', password='testuserpassword')
        response = self.client.get(reverse('datasets:dataset_update',
            kwargs={'slug': self.ds1.slug, 'pk': self.ds1.pk}))
        self.assertTemplateUsed(response, template_name="datasets/dataset_update.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_that_DatasetUpdateView_brings_in_correct_dataset_object(self):
        self.client.login(username='test_user', password='testuserpassword')
        response = self.client.get(reverse('datasets:dataset_update',
            kwargs={'slug': self.ds1.slug, 'pk': self.ds1.pk}))
        self.assertEqual(self.ds1, response.context['dataset'])
        self.assertNotEqual(self.ds2, response.context['dataset'])

    def test_that_DatasetUpdateView_uses_DatasetForm(self):
        self.client.login(username='test_user', password='testuserpassword')
        response = self.client.get(reverse('datasets:dataset_update',
            kwargs={'slug': self.ds1.slug, 'pk': self.ds1.pk}))
        self.assertIsInstance(response.context['form'], DatasetForm)



class LoadDatasetViewTests(BaseDatasetTest):

    """
    The test client returns an HttpResponse object that is actually not the
    same as the HttpRequest response object.
    The only reason to use the test client would be to use the other
    arguements, such as content, context, json, etc.
    """

    def test_load_dataset_returns_status_code_200(self):
        response = self.client.get(reverse('datasets:load_dataset',
            kwargs={'pk': self.ds2.pk}))
        self.assertEqual(200, response.status_code)

    def test_load_dataset_returns_status_code_200_PASSWORD_PROTECTED(self):
        response = self.client.get(reverse('datasets:load_dataset',
            kwargs={'pk': self.ds3.pk}))
        self.assertEqual(200, response.status_code)

    def test_load_dataset_returns_content(self):
        response = self.client.get(reverse('datasets:load_dataset',
            kwargs={'pk': self.ds2.pk}))
        self.assertIn(b'properties', response.content)

    """
    def test_load_dataset_returns_content_PASSWORD_PROTECTED(self):
        test_url = '/load_dataset/{pk}/'.format(pk=self.ds3.pk)

        cryptokey = os.environ['CRYPTOKEY'].encode('UTF-8')
        cryptokey_fernet = Fernet(cryptokey)

        password_bytes = (self.ds3.dataset_password).encode('UTF-8')
        password_decrypted_bytes = cryptokey_fernet.decrypt(password_bytes)
        password_decrypted_string = password_decrypted_bytes.decode('UTF-8')

        user_bytes = (self.ds3.dataset_user).encode('UTF-8')
        user_decrypted_bytes = cryptokey_fernet.decrypt(user_bytes)
        user_decrypted_string = user_decrypted_bytes.decode('UTF-8')

        print('''the methods for encrypting and decrypting work, but i cant get
any content from the page for one reason or another''')
        print(self.ds3.dataset_password)
        print(self.ds3.dataset_user)
        print(password_decrypted_string)
        print(user_decrypted_string)

        response = self.client.get(test_url)
        self.assertIn(b'properties', response.content)
    """



class PortalViewTestsThatRequireData_EMPTY_DATABASE(TestCase):

    def test_that_PortalView_without_datasets_says_none_available(self):
        response = self.client.get(reverse('datasets:portal'))
        self.assertIn('There are no datasets available',
            response.content.decode('utf-8'))

    def test_that_PortalView_brings_in_correct_number_of_dataset_objects(self):
        response = self.client.get(reverse('datasets:portal'))
        self.assertEqual(0, len(response.context['dataset_list']))


class PortalViewTestsThatRequireData(BaseDatasetTest):

    def test_base_url_resolves_to_PortalView(self):
        request = self.factory.get('')
        response = PortalView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_PortalView_uses_correct_template(self):
        response = self.client.get(reverse('datasets:portal'))
        self.assertTemplateUsed(response,
            template_name="datasets/portal.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_PortalView_title_is_correct(self):
        response = self.client.get(reverse('datasets:portal'))
        self.assertIn('<title>ZMT | GIS Portal</title>', response.content.decode('utf-8'))

    def test_that_PortalView_brings_in_correct_number_of_dataset_objects(self):
        response = self.client.get(reverse('datasets:portal'))
        self.assertEqual(3, len(response.context['dataset_list']))

    def test_that_PortalView_brings_in_correct_list_of_dataset_objects(self):
        response = self.client.get(reverse('datasets:portal'))
        object_list = Dataset.objects.all()
        for index, ds in enumerate(object_list):
            self.assertEqual(ds, response.context['dataset_list'][index])

    def test_PortalView_search_function(self):
        """
        This will be refactoed to use an ajax call
        """

        # Use the set up from the tests file in the datasets app
        # then filter them and check
        dataset_list = Dataset.objects.filter(title__contains=('ZMT'))
        self.assertEqual(len(dataset_list), 1)

        # now run it as a get request for "zmt"
        response = self.client.get('/?q=zmt')
        self.assertEqual(response.status_code, 200)
        self.assertIn('ZMT GeoJSON Polygon', response.content.decode('utf-8'))
        self.assertNotIn('Mapbox GeoJson Example', response.content.decode('utf-8'))
