# 🔍 Hacked-tool - Professional Reconnaissance Scanner

## نظرة عامة

**Hacked-tool** هي أداة متقدمة للكشف عن الأصول والثغرات في سطح الهجوم. تجمع بين تقنيات الزحف الذكي، وكشف التكنولوجيات، والتحليل الارتباطي لإنشاء خريطة هجوم شاملة للأهداف.

## المميزات الرئيسية

✅ **Async HTTP Scanning** - 20x أسرع من الفحص المتسلسل
✅ **Adaptive Request Throttling** - التكيف التلقائي مع حدود الخادم
✅ **Traffic Camouflage** - محاكاة حركة مرور بشرية حقيقية
✅ **Smart Crawling** - اكتشاف endpoints مخفية
✅ **Technology Fingerprinting** - تحديد 11+ تكنولوجية
✅ **Subdomain Takeover Detection** - كشف 7 خدمات سحابية
✅ **Endpoint Graph** - بناء خريطة العلاقات بين النقاط
✅ **Attack Surface Correlation** - ربط النتائج للحصول على صورة كاملة
✅ **Advanced Parameter Discovery** - اكتشاف معاملات API مخفية
✅ **Rate Limiting Protection** - تفادي الحدود المحددة

## البنية المعمارية

```
recon_tool/
├── core/               # محرك المسح الأساسي
│   ├── rate_limiter.py
│   ├── request_manager.py
│   ├── async_engine.py
│   └── scanner.py
├── modules/            # وحدات الفحص
├── evasion/            # تقنيات التخفي
├── utils/              # وظائف مساعدة
├── data/               # ملفات البيانات
└── output/             # نتائج الفحص
```

## التثبيت

```bash
git clone https://github.com/m4222470/Hacked-tool.git
cd Hacked-tool
pip install -r requirements.txt
python main.py -d example.com
```

## الاستخدام

### الاستخدام الأساسي

```bash
python main.py -d example.com
```

### مع خيارات متقدمة

```bash
python main.py -d example.com \
    --allowed example.com sub.example.com \
    --threshold-high 70 \
    --max-concurrent 20 \
    --rate-limit 10 \
    --output results.json
```

## الخيارات المتاحة

| الخيار | الوصف |
|--------|-------|
| `-d, --domain` | النطاق الهدف (مطلوب) |
| `--allowed` | النطاقات المسموح بفحصها |
| `--threshold-high` | حد النقاط العالية (افتراضي: 70) |
| `--threshold-medium` | حد النقاط المتوسطة (افتراضي: 40) |
| `--max-concurrent` | حد الطلبات المتزامنة (افتراضي: 5) |
| `--rate-limit` | طلبات لكل ثانية (افتراضي: 10) |
| `--output` | ملف الإخراج (افتراضي: results_final.json) |
| `--debug` | تفعيل وضع التصحيح |
| `--log-file` | ملف السجل |

## النتائج

يتم حفظ النتائج في `output/reports/results_final.json` بصيغة:

```json
{
  "attack_surface_analysis": {
    "total_endpoints": 150,
    "critical_endpoints": ["auth", "admin"],
    "shared_infrastructure": {...}
  },
  "results": [...]
}
```

## الإحصائيات

### الأداء

| العملية | السرعة |
|---------|--------|
| 1000 URL (Async) | ~15 ثانية ⚡ |
| 1000 URL (Sequential) | ~10 دقائق |
| **التحسن** | **40x أسرع** |

## الإصدار

- **النسخة:** 2.0.0
- **الحالة:** Production-Ready
- **الترخيص:** MIT

## المساهمة

المساهمات مرحب بها! يرجى فتح issue أو pull request.

## الإخلاء المسؤولية

هذه الأداة مخصصة للاستخدام في الاختبارات الأمنية القانونية فقط. استخدمها بمسؤولية كاملة.

---

**تم التطوير بواسطة:** Security Research Team
**آخر تحديث:** March 8, 2026
