الملفات جاهزة. الخطوات التالية:

1) أنشئ مستودع على GitHub أو استخدم الموجود.
2) انسخ كل الملفات إلى جذر المستودع.
3) فعل GitHub Actions إذا طُلب.
4) ادفع التغييرات: git add . && git commit -m "init" && git push
5) اذهب إلى Railway Dashboard وتأكد أن المشروع مربوط بالمستودع.
6) في Railway تأكد أن متغير PORT مستخدم أو اترك الافتراضي.
7) بعد كل دفع GitHub Actions سيحدث stream.txt تلقائيًا كل 3 ساعات.
8) رابط التطبيق الثابت: https://bein-production-dcf5.up.railway.app/bein

نصائح لتحمّل أكثر من 50 مستخدم:

- زد عدد عمال gunicorn (--workers 2) وعدل حسب الحاجة.
- استخدم CDN أو Cloudflare لتخفيف حركة المرور على Railway.
- ضع Cache TTL أكبر في app.py (CACHE_TTL) إذا كان مقبولًا.
- لو زادت الأحمال، فكّر في VPS أو سرفر وسيط واحد يقوم بالبث إلى CDN.

ملاحظة: الرابط في stream.txt يحتاج تحديثًا عند انتهاء الصلاحية. GitHub Actions سيحاول تحديثه كل 3 ساعات.# Bein
