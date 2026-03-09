# ⚡ البدء السريع - Hacked-tool v2.0.0

## 🚀 في 60 ثانية فقط

### 1️⃣ التثبيت (10 ثوان)
```bash
pip install -r requirements_new.txt
```

### 2️⃣ التشغيل (10 ثوان)
```bash
python main.py -d example.com
```

### 3️⃣ عرض النتائج (10 ثوان)
```bash
cat results.json | python -m json.tool
```

---

## 📋 الأوامر الأساسية

### الفحص البسيط
```bash
python main.py -d target.com
```

### الفحص المتقدم
```bash
python main.py -d target.com \
    --max-concurrent 20 \
    --rate-limit 10 \
    --threshold-high 75 \
    --output results.json \
    --debug
```

### الفحص السريع (أقل دقة، أسرع)
```bash
python main.py -d target.com \
    --max-concurrent 50 \
    --rate-limit 50
```

### الفحص الحذر (أبطأ، أكثر احتياطاً)
```bash
python main.py -d target.com \
    --max-concurrent 2 \
    --rate-limit 2
```

---

## 🎯 استخدامات شائعة

### الفحص الأساسي
```bash
python main.py -d example.com
```

### مع نطاقات متعددة
```bash
python main.py -d example.com \
    --allowed example.com,api.example.com,admin.example.com
```

### حفظ النتائج
```bash
python main.py -d example.com \
    --output results.json
```

### وضع التصحيح
```bash
python main.py -d example.com --debug
```

### معايير مخصصة
```bash
python main.py -d example.com \
    --threshold-high 80 \
    --threshold-medium 50
```

---

## 📊 فهم النتائج

```json
{
  "assets": [
    {
      "domain": "example.com",
      "score": 85,           ← درجة الخطورة (0-100)
      "severity": "HIGH",    ← مستوى الخطورة
      "technologies": [      ← التكنولوجيات المكتشفة
        "WordPress",
        "Apache"
      ],
      "endpoints": [         ← النقاط المكتشفة
        {
          "url": "https://example.com/admin",
          "status": 403,
          "score": 75
        }
      ]
    }
  ]
}
```

---

## 🔧 التخصيص

### تغيير الإعدادات الافتراضية

**الملف:** `config.py`

```python
# غيّر هذه الثوابت:
DEFAULT_REQUEST_DELAY = 1      # التأخير
MAX_THREADS = 10               # عدد الخيوط
TIMEOUT = 10                   # مهلة الطلب
DEFAULT_SCORE_THRESHOLD_HIGH = 70  # العتبة العالية
```

### إضافة تكنولوجية جديدة

**الملف:** `data/fingerprints.json`

```json
{
  "my_tech": {
    "headers": ["X-My-Header"],
    "patterns": ["my_pattern"],
    "score": 50
  }
}
```

---

## 🐛 حل المشاكل الشائعة

### المشكلة: الأداة بطيئة جداً
```bash
# زيادة الطلبات المتزامنة
python main.py -d example.com --max-concurrent 20 --rate-limit 50
```

### المشكلة: يتم حظر الطلبات
```bash
# تقليل معدل الطلبات
python main.py -d example.com --rate-limit 2 --max-concurrent 2
```

### المشكلة: ModuleNotFoundError
```bash
# إعادة تثبيت المكتبات
pip install -r requirements_new.txt --force-reinstall
```

### المشكلة: SSL certificate error
```bash
# البرنامج يتعامل معها تلقائياً
# يعطي درجات أقل للأخطاء الأمنية
# لا تحتاج لفعل شيء
```

---

## 💡 نصائح سريعة

✅ **ابدأ بـ Domain واحد**
```bash
python main.py -d example.com
```

✅ **استخدم --debug للمزيد من المعلومات**
```bash
python main.py -d example.com --debug
```

✅ **احفظ النتائج في ملف**
```bash
python main.py -d example.com --output results.json
```

✅ **استخدم معايير مناسبة لخادمك**
- خادم قوي: `--max-concurrent 20 --rate-limit 50`
- خادم عادي: `--max-concurrent 10 --rate-limit 10`
- خادم حساس: `--max-concurrent 2 --rate-limit 2`

---

## 📞 الحصول على المساعدة

### الأوامر المفيدة

```bash
# عرض الخيارات المتاحة
python main.py --help

# عرض الإصدار
python main.py --version

# اختبار الاتصال
python -c "import requests; print('OK')"
```

### الملفات المرجعية

- 📖 **README.md** - التوثيق الفني
- 👤 **USER_GUIDE.md** - دليل المستخدم
- 🏗️ **ARCHITECTURE.html** - الهيكل المعماري
- 📑 **INDEX.md** - الفهرس الكامل

---

## 🎓 أمثلة عملية

### مثال 1: فحص بسيط
```bash
python main.py -d google.com
```

### مثال 2: فحص مع حفظ
```bash
python main.py -d github.com \
    --output github_results.json
```

### مثال 3: فحص متعمق
```bash
python main.py -d stackoverflow.com \
    --allowed stackoverflow.com,meta.stackoverflow.com \
    --max-concurrent 20 \
    --threshold-high 75 \
    --output detailed.json \
    --debug
```

### مثال 4: فحص حذر
```bash
python main.py -d sensitive.com \
    --max-concurrent 1 \
    --rate-limit 1 \
    --threshold-high 80
```

---

## 📈 الأداء المتوقع

| الحالة | الوقت | الملاحظات |
|--------|-------|---------|
| 100 URLs | 2-3 ثواني | سريع جداً |
| 1000 URLs | 15-20 ثانية | معقول |
| 5000 URLs | 75-100 ثانية | بطيء قليلاً |

---

## ✅ قائمة التحقق

- [ ] ثبّت المكتبات
- [ ] اختبرت التشغيل الأول
- [ ] فهمت الخيارات الأساسية
- [ ] جرّبت مثالاً حقيقياً
- [ ] فهمت النتائج
- [ ] حفظت النتائج في ملف

---

## 🚀 الخطوات التالية

### المستخدمون الجدد
1. 📖 اقرأ [USER_GUIDE.md](USER_GUIDE.md)
2. 🏗️ افتح [ARCHITECTURE.html](ARCHITECTURE.html)
3. 📑 راجع [API_REFERENCE.md](API_REFERENCE.md)

### المطورون
1. 🛠️ اقرأ [DEVELOPERS.md](DEVELOPERS.md)
2. 🗺️ اتبع [COMPLETION_ROADMAP.md](COMPLETION_ROADMAP.md)
3. 💻 ابدأ المساهمة

---

## 🎉 أنت جاهز!

الآن أنت مستعد لاستخدام Hacked-tool. ابدأ الفحص الآن!

```bash
python main.py -d example.com
```

---

**آخر تحديث:** 8 مارس 2025 | **الإصدار:** v2.0.0-beta

🔗 **روابط مهمة:**
- [README.md](README.md) - التوثيق الكامل
- [USER_GUIDE.md](USER_GUIDE.md) - دليل مفصل
- [INDEX.md](INDEX.md) - الفهرس الشامل
