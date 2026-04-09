# Walid Portfolio | Flask Edition

نسخة Python Flask من الموقع الشخصي.

## التقنية
- Python
- Flask
- Jinja2 Templates
- Cloudinary
- Gunicorn

## المميزات
- موقع ثنائي اللغة: عربي / English
- صفحة شخصية احترافية
- زر تحميل السيرة الذاتية
- Photo Gallery
- Admin Dashboard
- رفع الصور وحذفها
- متوافق مع Render Free

## التشغيل محليًا
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

على ويندوز:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## متغيرات البيئة
```env
SECRET_KEY=change-this-secret-key
ADMIN_PASSWORD=change-this-password
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
CLOUDINARY_FOLDER=walid-portfolio-gallery
```

## النشر على Render
1. ارفع المشروع إلى GitHub.
2. من Render اختر New > Blueprint أو New > Web Service.
3. استخدم الخطة Free.
4. أضف Environment Variables.
5. افتح:
```bash
/admin/login
```

## الملفات المهمة
- `app.py`
- `templates/`
- `static/css/style.css`
- `static/js/main.js`
- `data/site_content.json`
- `render.yaml`


## الصور المضافة
تمت إضافة الصور المحلية داخل:
- `static/images/profile-headshot.jpg`
- `static/images/about-photo.jpg`
- `static/images/tech-illustration.jpg`

الاستخدام الحالي:
- صورة البروفايل في قسم الهيدر
- صورة إضافية في قسم About
- صور افتراضية داخل Gallery


## Latest updates
- Added Bibliotheca Alexandrina logo
- Updated role title
- Fixed phone rendering in Arabic
- Light blue theme refresh


## Latest updates
- Default opening language changed to English
- Adjusted image vertical positioning and centering


## Latest updates
- More detailed hero summary
- Name kept on a single line on desktop
- Reduced extra spacing across the page


## Latest updates
- Added new personal photo
- Removed gallery dates and titles
- Made About and Get in touch sections more compact
- Reduced extra whitespace across the homepage


## Latest updates
- Swapped hero sections to show profile card first
- Career timeline now uses two columns on desktop
- Replaced and enlarged the attached logo
- Removed the local default images/gallery notice


## Latest updates
- Removed Cloudinary gallery note completely
