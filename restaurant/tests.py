from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from restaurant.context_processors import order_count

class ContextProcessorTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_order_count_empty(self):
        request = self.factory.get('/')
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()
        
        result = order_count(request)
        self.assertEqual(result['order_count'], 0)

        def test_order_count_with_items(self):
        request = self.factory.get('/')
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        
        request.session['order'] = {
            '1': {'quantity': 2},
            '2': {'quantity': 3}
        }
        request.session.save()
        
        result = order_count(request)
        self.assertEqual(result['order_count'], 5)

class CheckoutAccessTest(TestCase):
    def test_checkout_requires_login(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        login_url = reverse('login')
        self.assertIn(login_url, response.url)

class AddToOrderAccessTest(TestCase):
    def test_add_to_order_requires_login(self):
        response = self.client.get(reverse('add_to_order', args=[1]))
        self.assertEqual(response.status_code, 302)
        login_url = reverse('login')
        self.assertIn(login_url, response.url)
