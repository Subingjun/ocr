import os
from django.shortcuts import render, redirect, get_object_or_404
from ocr.forms import LoginForm, RegistrationForm, OCRImageForm, ChangePasswordForm
from ocr.login import login_view
from ocr.models import OCRUser, OCRImage
from ocr.ocr_api import ocr


# Create your views here.
def index(request):
    if request.method == 'POST':
        username = login_view(request)
        if username is not None:
            response = redirect('home')  # 登录成功后跳转页面
            response.set_cookie('username', username, max_age=3600)  # 将用户名存入 Cookie，有效期为1小时
            return response
        form = LoginForm()
        return render(request, 'index.html', {'form': form, 'msg': "用户名或密码错误"})
    else:
        form = LoginForm()
        return render(request, 'index.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # 创建用户
            user = OCRUser.objects.create(username=username, password=password)
            user.save()
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    username = request.COOKIES.get('username')
    if username is None:
        return redirect('index')
    if request.method == 'POST':
        # 获取用户名对应的用户实例
        try:
            user = OCRUser.objects.get(username=username)
        except OCRUser.DoesNotExist:
            return redirect('index')  # 若用户不存在则重定向到登录页面
        form = OCRImageForm(request.POST, request.FILES)
        if form.is_valid():
            # 创建 OCRImage 实例，并将当前用户设置为 owner
            ocr_image = form.save(commit=False)
            ocr_image.owner = user
            ocr_image.save()
            image_path = ocr_image.image.path  # 使用 image.path 获取服务器上的文件路径
            # 调用 ocr() 函数进行识别
            recognition_result = ocr(image_path)  # 传入图片路径
            ocr_image.recognition_result = recognition_result
            ocr_image.save()
            return redirect('recent_images')  # 上传成功后跳转到主页
    else:
        form = OCRImageForm()
    return render(request, 'home.html', {'form': form, 'username': username})


def recent_images_view(request):
    username = request.COOKIES.get('username')
    # 检查用户名是否在 Cookie 中
    if username is None:
        return redirect('index')

    # 获取用户名对应的用户实例
    try:
        user = OCRUser.objects.get(username=username)
    except OCRUser.DoesNotExist:
        return redirect('index')

    # 按 id 降序排序并获取最近的 5 张图片
    recent_images = OCRImage.objects.filter(owner=user).order_by('-id')

    return render(request, 'recent_images.html', {'recent_images': recent_images, 'username': username})


def delete_image(request, image_id):
    username = request.COOKIES.get('username')
    # 检查用户名是否在 Cookie 中
    if username is None:
        return redirect('index')

    # 获取用户名对应的用户实例
    try:
        user = OCRUser.objects.get(username=username)
    except OCRUser.DoesNotExist:
        return redirect('index')
    if request.method == 'POST':
        image = get_object_or_404(OCRImage, id=image_id)
        if image.owner == user:  # 确保用户是图像的拥有者
            # 获取图片文件的绝对路径
            image_file_path = image.image.path

            # 删除数据库记录
            image.delete()

            # 删除本地文件
            if os.path.exists(image_file_path):
                os.remove(image_file_path)
            return redirect('recent_images')  # 删除后重定向到主页
    return redirect('recent_images')  # 非法请求重定向


def change_password_view(request):
    username = request.COOKIES.get('username')
    # 检查用户名是否在 Cookie 中
    if username is None:
        return redirect('index')

    # 获取用户名对应的用户实例
    try:
        user = OCRUser.objects.get(username=username)
    except OCRUser.DoesNotExist:
        return redirect('index')

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            print(old_password)
            if not old_password == user.password:  # 使用check_password手动验证密码
                form.add_error('old_password', '旧密码错误')
            else:
                # 如果密码正确，更新密码
                user.password = new_password  # 使用make_password加密新密码
                user.save()  # 保存更新后的密码
                return redirect('home')  # 密码更新成功后跳转到主页
    else:
        form = ChangePasswordForm()

    return render(request, 'change_pass.html', {'form': form})
