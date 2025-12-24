# HBnB Evolution - UML (Part 1)

## الهدف
هذا المجلد يحتوي على مخططات UML المطلوبة للمشروع بصيغة Mermaid.

## هيكلة الملفات
- part1/diagrams/00_high_level_package.mmd
- part1/diagrams/01_business_logic_class.mmd
- part1/diagrams/02_sequence_user_registration.mmd
- part1/diagrams/03_sequence_place_creation.mmd
- part1/diagrams/04_sequence_review_submission.mmd
- part1/diagrams/05_sequence_fetch_places.mmd

## وصف مختصر لكل مخطط

### 00 High-Level Package Diagram
يبين الطبقات الرئيسية:
- المستخدم
- طبقة العرض
- منطق الأعمال
- طبقة التخزين
ويوضح العلاقات العامة بين الطبقات وتدفق الطلب.

### 01 Business Logic Class Diagram
يبين الكلاسات الأساسية في منطق الأعمال:
User, Place, Review, Amenity
مع الخصائص والعمليات والعلاقات (Ownership / Reviews / Amenities).

### 02 User Registration Sequence
يوضح تدفق تسجيل المستخدم من الواجهة إلى التخزين مع إرسال رسالة تأكيد.

### 03 Place Creation Sequence
يوضح إنشاء مكان جديد.
المتطلب الأساسي: المستخدم مسجل دخول.

### 04 Review Submission Sequence
يوضح إرسال مراجعة وربطها بالمكان.
المتطلب الأساسي: المستخدم مسجل دخول.

### 05 Fetch Places Sequence
يوضح جلب قائمة الأماكن مع تطبيق فلاتر داخل منطق الأعمال ثم الاستعلام من التخزين.

## طريقة المعاينة
استخدم Mermaid Online لفتح أي ملف .mmd ونسخ محتواه لرؤيته.
