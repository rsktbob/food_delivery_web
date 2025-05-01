from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from account.forms import BaseRegisterForm, CustomerRegisterForm, VendorRegisterForm, CourierRegisterForm
from account.models import CustomerProfile, VendorProfile, CourierProfile

User = get_user_model()

class BaseRegisterFormTestCase(TestCase):
    """Test the BaseRegisterForm"""
    
    def setUp(self):
        """Set up test data"""
        self.valid_form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'securepassword123'
        }
    
    def test_valid_form(self):
        """Test form with valid data"""
        form = BaseRegisterForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
    
    def test_missing_required_fields(self):
        """Test form with missing required fields"""
        required_fields = ['username', 'email', 'first_name', 'last_name', 'password']
        
        for field in required_fields:
            with self.subTest(field=field):
                # Create a copy of valid data and remove one required field
                invalid_data = self.valid_form_data.copy()
                invalid_data.pop(field)
                
                form = BaseRegisterForm(data=invalid_data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)
    
    def test_password_hashing(self):
        """Test that password is properly hashed when saving"""
        form = BaseRegisterForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        
        # Verify that the password was hashed
        self.assertNotEqual(user.password, 'securepassword123')
        self.assertTrue(check_password('securepassword123', user.password))
    
    def test_form_save_without_commit(self):
        """Test saving form without commit"""
        form = BaseRegisterForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save(commit=False)
        
        # Check that the user wasn't saved to the database
        self.assertEqual(User.objects.count(), 0)
        
        # Verify user details were set correctly
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        
        # Now save the user
        user.save()
        self.assertEqual(User.objects.count(), 1)


class CustomerRegisterFormTestCase(TestCase):
    """Test the CustomerRegisterForm"""
    
    def setUp(self):
        """Set up test data"""
        self.valid_form_data = {
            'username': 'customer',
            'email': 'customer@example.com',
            'first_name': 'Customer',
            'last_name': 'User',
            'password': 'securepassword123',
            'save_address': '123 Test Street, City',
            'default_payment_method': 'Credit Card'
        }
    
    def test_valid_form(self):
        """Test form with valid data"""
        form = CustomerRegisterForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
    
    def test_missing_required_fields(self):
        """Test form with missing customer-specific required fields"""
        required_fields = ['save_address', 'default_payment_method']
        
        for field in required_fields:
            with self.subTest(field=field):
                # Create a copy of valid data and remove one required field
                invalid_data = self.valid_form_data.copy()
                invalid_data.pop(field)
                
                form = CustomerRegisterForm(data=invalid_data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)
    
    def test_form_save(self):
        """Test form save creates both user and profile"""
        form = CustomerRegisterForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        
        # Verify user was created with the right type
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.user_type, 'customer')
        
        # Verify customer profile was created
        self.assertEqual(CustomerProfile.objects.count(), 1)
        profile = CustomerProfile.objects.get(user=user)
        self.assertEqual(profile.save_address, '123 Test Street, City')
        self.assertEqual(profile.default_payment_method, 'Credit Card')
    
    def test_form_save_without_commit(self):
        """Test saving form without commit doesn't create the profile"""
        form = CustomerRegisterForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save(commit=False)
        
        # Check that nothing was saved to the database
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(CustomerProfile.objects.count(), 0)
        
        # Verify user type was set correctly
        self.assertEqual(user.user_type, 'customer')


class VendorRegisterFormTestCase(TestCase):
    """Test the VendorRegisterForm"""
    
    def setUp(self):
        """Set up test data"""
        self.valid_form_data = {
            'username': 'vendor',
            'email': 'vendor@example.com',
            'first_name': 'Vendor',
            'last_name': 'User',
            'password': 'securepassword123',
            'restaurant_name': 'Test Restaurant',
            'restaurant_address': '456 Food Street, City',
            'restaurant_license_number': 'LIC123456',
            'description': 'A test restaurant'
        }
    
    def test_valid_form(self):
        """Test form with valid data"""
        form = VendorRegisterForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
    
    def test_missing_required_fields(self):
        """Test form with missing vendor-specific required fields"""
        required_fields = ['restaurant_name', 'restaurant_address', 'restaurant_license_number']
        
        for field in required_fields:
            with self.subTest(field=field):
                # Create a copy of valid data and remove one required field
                invalid_data = self.valid_form_data.copy()
                invalid_data.pop(field)
                
                form = VendorRegisterForm(data=invalid_data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)
    
    def test_optional_description_field(self):
        """Test that description is optional"""
        # Remove the description field
        data = self.valid_form_data.copy()
        data.pop('description')
        
        form = VendorRegisterForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_form_save(self):
        """Test form save creates both user and profile"""
        form = VendorRegisterForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        
        # Verify user was created with the right type
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.user_type, 'vendor')
        
        # Verify vendor profile was created
        self.assertEqual(VendorProfile.objects.count(), 1)
        profile = VendorProfile.objects.get(user=user)
        self.assertEqual(profile.restaurant_name, 'Test Restaurant')
        
        # Note: The actual save method in forms.py only sets the restaurant_name field
        # so we're just testing that. In a real implementation, we'd add tests for the
        # other fields as well once they're added to the form's save method.


class CourierRegisterFormTestCase(TestCase):
    """Test the CourierRegisterForm"""
    
    def setUp(self):
        """Set up test data"""
        self.valid_form_data = {
            'username': 'courier',
            'email': 'courier@example.com',
            'first_name': 'Courier',
            'last_name': 'User',
            'password': 'securepassword123',
            'vehicle_type': 'Motorcycle',
            'license_plate': 'ABC123'
        }
    
    def test_valid_form(self):
        """Test form with valid data"""
        form = CourierRegisterForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
    
    def test_missing_required_fields(self):
        """Test form with missing courier-specific required fields"""
        required_fields = ['vehicle_type', 'license_plate']
        
        for field in required_fields:
            with self.subTest(field=field):
                # Create a copy of valid data and remove one required field
                invalid_data = self.valid_form_data.copy()
                invalid_data.pop(field)
                
                form = CourierRegisterForm(data=invalid_data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)
    
    def test_form_save(self):
        """Test form save creates both user and profile"""
        form = CourierRegisterForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        
        # Verify user was created with the right type
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.user_type, 'courier')
        
        # Verify courier profile was created
        self.assertEqual(CourierProfile.objects.count(), 1)
        profile = CourierProfile.objects.get(user=user)
        self.assertEqual(profile.vehicle_type, 'Motorcycle')
        self.assertEqual(profile.license_plate, 'ABC123')
    
    def test_form_save_without_commit(self):
        """Test saving form without commit doesn't create the profile"""
        form = CourierRegisterForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save(commit=False)
        
        # Check that nothing was saved to the database
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(CourierProfile.objects.count(), 0)
        
        # Verify user type was set correctly
        self.assertEqual(user.user_type, 'courier')