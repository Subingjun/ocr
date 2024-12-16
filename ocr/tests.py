from django.test import TestCase, Client
from django.urls import reverse
from .models import OCRUser, OCRImage
from .forms import RegistrationForm, OCRImageForm


class OCRModelsTest(TestCase):
    """测试模型逻辑"""

    def setUp(self):
        self.user = OCRUser.objects.create(username="testuser", password="password123")

    def test_create_ocr_user(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.password, "password123")

    def test_create_ocr_image(self):
        image = OCRImage.objects.create(image='test_image.png', owner=self.user)
        self.assertEqual(image.owner, self.user)
        self.assertEqual(image.image, 'test_image.png')


class OCRFormsTest(TestCase):
    """测试表单逻辑"""

    def test_registration_form_valid(self):
        form = RegistrationForm(data={
            'username': 'testuser',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid(self):
        form = RegistrationForm(data={
            'username': 'testuser',
            'password': 'password123',
            'confirm_password': 'wrongpassword'
        })
        self.assertFalse(form.is_valid())

    def test_ocr_image_form(self):
        form = OCRImageForm(data={'image': 'test_image.png'})
        self.assertTrue(form.is_valid())


class LoginViewTest(TestCase):
    def setUp(self):
        # 在测试前创建一个测试用户
        OCRUser.objects.create(username='testuser', password='testpassword')

    def test_login_success(self):
        """
        测试用户使用正确的用户名和密码登录。
        """
        response = self.client.post(reverse('index'), {'username': 'testuser', 'password': 'testpassword'})
        # 检查是否发生了重定向
        self.assertEqual(response.status_code, 302)
        # 验证重定向到 'home'
        self.assertEqual(response.url, reverse('home'))
        # 验证 Cookie 是否正确设置
        self.assertIn('username', response.cookies)
        self.assertEqual(response.cookies['username'].value, 'testuser')

    def test_login_failure(self):
        """
        测试用户使用错误的用户名或密码登录。
        """
        response = self.client.post(reverse('index'), {'username': 'testuser', 'password': 'wrongpassword'})
        # 检查是否返回登录页面
        self.assertEqual(response.status_code, 200)
        # 验证错误消息是否显示
        self.assertContains(response, "用户名或密码错误")


class OCRIntegrationTest(TestCase):
    """测试集成逻辑"""

    def setUp(self):
        self.client = Client()
        self.user = OCRUser.objects.create(username="testuser", password="password123")

    def test_image_upload_and_query(self):
        # 模拟登录用户
        self.client.cookies['username'] = self.user.username
        # 上传图片
        with open('media/images/download.png', 'rb') as img:
            response = self.client.post(reverse('home'), {'image': img})
            self.assertEqual(response.status_code, 302)

        # 查询最近上传的图片
        recent_images = OCRImage.objects.filter(owner=self.user).order_by('-id')
        self.assertTrue(recent_images.exists())
