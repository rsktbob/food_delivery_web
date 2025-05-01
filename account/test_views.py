
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from unittest.mock import patch, MagicMock

from account.views import RegisterView, CustomLoginView
from account.forms import CustomerRegisterForm, VendorRegisterForm, CourierRegisterForm

User = get_user_model()

class RegisterViewTestCase(TestCase):
    """Test the RegisterView directly"""
    
    def setUp(self):
        """Set up test data and factory"""
        self.factory = RequestFactory()
        self.view = RegisterView()
        
        # Mock the redirect function to avoid URL reverse issues
        self.redirect_patcher = patch('account.views.redirect')
        self.mock_redirect = self.redirect_patcher.start()
        self.mock_redirect.return_value = HttpResponse(status=302)
        
        # Mock the render function to avoid template rendering issues
        self.render_patcher = patch('account.views.render')
        self.mock_render = self.render_patcher.start()
        self.mock_render.return_value = HttpResponse(status=200)
    
    def tearDown(self):
        """Clean up patches"""
        self.redirect_patcher.stop()
        self.render_patcher.stop()
    
    def _get_request_with_session(self, url, method='get', data=None):
        """Helper method to create request with session and messages"""
        if method.lower() == 'post':
            request = self.factory.post(url, data=data)
        else:
            request = self.factory.get(url)
        
        # Add session
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        
        # Add messages
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        return request
    
    def test_get_register_view(self):
        """Test get method renders correct template"""
        request = self._get_request_with_session('/register/')
        response = self.view.get(request)
        
        self.assertEqual(response.status_code, 200)
        self.mock_render.assert_called_once_with(request, 'account/register.html')
    
    @patch('account.forms.CustomerRegisterForm.is_valid')
    @patch('account.forms.CustomerRegisterForm.save')
    def test_post_customer_registration_success(self, mock_save, mock_is_valid):
        """Test successful customer registration"""
        mock_is_valid.return_value = True
        
        request = self._get_request_with_session('/register/customer/', method='post', data={
            'username': 'testcustomer',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        
        response = self.view.post(request, user_type='customer')
        
        # Check if form was validated and saved
        mock_is_valid.assert_called_once()
        mock_save.assert_called_once()
        
        # Check redirect to login page
        self.assertEqual(response.status_code, 302)
        self.mock_redirect.assert_called_once_with('login')
    
    @patch('account.forms.VendorRegisterForm.is_valid')
    @patch('account.forms.VendorRegisterForm.save')
    def test_post_vendor_registration_success(self, mock_save, mock_is_valid):
        """Test successful vendor registration"""
        mock_is_valid.return_value = True
        
        request = self._get_request_with_session('/register/vendor/', method='post', data={
            'username': 'testvendor',
            'email': 'vendor@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'restaurant_name': 'Test Restaurant'
        })
        
        response = self.view.post(request, user_type='vendor')
        
        # Check if form was validated and saved
        mock_is_valid.assert_called_once()
        mock_save.assert_called_once()
        
        # Check redirect to login page
        self.assertEqual(response.status_code, 302)
        self.mock_redirect.assert_called_once_with('login')
    
    @patch('account.forms.CourierRegisterForm.is_valid')
    @patch('account.forms.CourierRegisterForm.save')
    def test_post_courier_registration_success(self, mock_save, mock_is_valid):
        """Test successful courier registration"""
        mock_is_valid.return_value = True
        
        request = self._get_request_with_session('/register/courier/', method='post', data={
            'username': 'testcourier',
            'email': 'courier@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'vehicle_type': 'Scooter'
        })
        
        response = self.view.post(request, user_type='courier')
        
        # Check if form was validated and saved
        mock_is_valid.assert_called_once()
        mock_save.assert_called_once()
        
        # Check redirect to login page
        self.assertEqual(response.status_code, 302)
        self.mock_redirect.assert_called_once_with('login')
    
    def test_post_registration_form_invalid(self):
        """Test registration with invalid form data"""
        # Create a mock form with errors
        mock_form = MagicMock()
        mock_form.is_valid.return_value = False
        mock_form.errors.items.return_value = [('username', ['Username already exists'])]
        
        # Patch the form class to return our mock
        with patch('account.views.CustomerRegisterForm', return_value=mock_form):
            request = self._get_request_with_session('/register/customer/', method='post', data={
                'username': 'existinguser',
                'email': 'test@example.com'
            })
            
            response = self.view.post(request, user_type='customer')
            
            # Check if form validation was called
            mock_form.is_valid.assert_called_once()
            
            # Check if the same template is rendered with form errors
            self.assertEqual(response.status_code, 200)
            self.mock_render.assert_called_once()
    
    def test_post_invalid_user_type(self):
        """Test registration with invalid user type"""
        request = self._get_request_with_session('/register/invalid/', method='post', data={})
        
        response = self.view.post(request, user_type='invalid')
        
        # Check redirect to register page
        self.assertEqual(response.status_code, 302)
        self.mock_redirect.assert_called_once_with('register')


class CustomLoginViewTestCase(TestCase):
    """Test the CustomLoginView directly"""
    
    def setUp(self):
        """Set up test data"""
        self.factory = RequestFactory()
        
        # Mock the redirect function to avoid URL reverse issues
        self.redirect_patcher = patch('account.views.redirect')
        self.mock_redirect = self.redirect_patcher.start()
        self.mock_redirect.side_effect = lambda url: HttpResponse(status=302, headers={'Location': url})
        
        # Mock the logout function
        self.logout_patcher = patch('account.views.logout')
        self.mock_logout = self.logout_patcher.start()
        
        # Create test users
        self.customer_user = User.objects.create_user(
            username='testcustomer', email='customer@test.com',
            password='password123', user_type='customer'
        )
        self.vendor_user = User.objects.create_user(
            username='testvendor', email='vendor@test.com',
            password='password123', user_type='vendor'
        )
        self.courier_user = User.objects.create_user(
            username='testcourier', email='courier@test.com',
            password='password123', user_type='courier'
        )
        self.invalid_user = User.objects.create_user(
            username='testinvalid', email='invalid@test.com',
            password='password123', user_type=''
        )
    
    def tearDown(self):
        """Clean up patches"""
        self.redirect_patcher.stop()
        self.logout_patcher.stop()
    
    def _get_request_with_session_and_user(self, url, user):
        """Helper method to create request with session, messages and logged in user"""
        request = self.factory.get(url)
        
        # Add session
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        
        # Add messages
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        # Set user
        request.user = user
        
        return request
    
    def test_form_valid_customer_redirect(self):
        """Test form_valid redirects customer to customer dashboard"""
        request = self._get_request_with_session_and_user('/login/', self.customer_user)
        
        # Create a mock form
        form = MagicMock()
        
        # Create the view instance and set the request
        view = CustomLoginView()
        view.request = request
        
        # Mock the parent form_valid method by patching only in this method's scope
        with patch('django.contrib.auth.views.LoginView.form_valid', return_value=HttpResponse()):
            response = view.form_valid(form)
            
            # Check redirect to customer dashboard
            self.assertEqual(response.status_code, 302)
            self.mock_redirect.assert_called_once_with('customer_dashboard')
    
    def test_form_valid_vendor_redirect(self):
        """Test form_valid redirects vendor to vendor dashboard"""
        request = self._get_request_with_session_and_user('/login/', self.vendor_user)
        
        # Create a mock form
        form = MagicMock()
        
        # Create the view instance and set the request
        view = CustomLoginView()
        view.request = request
        
        # Mock the parent form_valid method
        with patch('django.contrib.auth.views.LoginView.form_valid', return_value=HttpResponse()):
            response = view.form_valid(form)
            
            # Check redirect to vendor dashboard
            self.assertEqual(response.status_code, 302)
            self.mock_redirect.assert_called_once_with('vendor_dashboard')
    
    def test_form_valid_courier_redirect(self):
        """Test form_valid redirects courier to courier dashboard"""
        request = self._get_request_with_session_and_user('/login/', self.courier_user)
        
        # Create a mock form
        form = MagicMock()
        
        # Create the view instance and set the request
        view = CustomLoginView()
        view.request = request
        
        # Mock the parent form_valid method
        with patch('django.contrib.auth.views.LoginView.form_valid', return_value=HttpResponse()):
            response = view.form_valid(form)
            
            # Check redirect to courier dashboard
            self.assertEqual(response.status_code, 302)
            self.mock_redirect.assert_called_once_with('courier_dashboard')
    
    def test_form_valid_invalid_user_type(self):
        """Test form_valid with invalid user type logs out and redirects to login"""
        request = self._get_request_with_session_and_user('/login/', self.invalid_user)
        
        # Create a mock form
        form = MagicMock()
        
        # Create the view instance and set the request
        view = CustomLoginView()
        view.request = request
        
        # Mock the parent form_valid method
        with patch('django.contrib.auth.views.LoginView.form_valid', return_value=HttpResponse()):
            response = view.form_valid(form)
            
            # Check if logout was called
            self.mock_logout.assert_called_once_with(request)
            
            # Check redirect to login page
            self.assertEqual(response.status_code, 302)
            self.mock_redirect.assert_called_once_with('login')
    
    def test_form_invalid(self):
        """Test form_invalid method adds error message"""
        request = self._get_request_with_session_and_user('/login/', None)
        
        # Create a mock form
        form = MagicMock()
        
        # Create the view instance and set the request
        view = CustomLoginView()
        view.request = request
        
        # Mock parent's form_invalid to return a response
        mock_response = HttpResponse()
        
        # Mock the parent form_invalid method
        with patch('django.contrib.auth.views.LoginView.form_invalid', return_value=mock_response):
            result = view.form_invalid(form)
            
            # Check if error message was added
            messages = [m.message for m in request._messages]
            self.assertIn('Login failed. Please check your username and password.', 
                          [str(m) for m in messages])
            
            # Check if parent's response was returned
            self.assertEqual(result, mock_response)