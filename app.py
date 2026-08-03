<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sun Pyramids Tours - تصفية المرشدين</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
        }

        body {
            background-color: #f4f7f6;
            color: #333;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }

        /* الهيدر العلوي */
        header {
            background-color: #ffffff;
            border-bottom: 2px solid #e0e0e0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 20px;
            height: 70px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            z-index: 10;
        }

        .logo-container {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .logo-container img {
            height: 50px;
        }

        /* المحتوى الرئيسي */
        .main-container {
            display: flex;
            flex: 1;
            position: relative;
            overflow: hidden;
        }

        /* الشريط الجانبي */
        sidebar {
            width: 280px;
            background-color: #e8f0eb;
            border-left: 1px solid #d0ded3;
            display: flex;
            flex-direction: column;
            padding: 20px;
            transition: transform 0.3s ease;
            position: absolute;
            height: 100%;
            right: 0;
            z-index: 5;
            box-shadow: -2px 0 5px rgba(0,0,0,0.05);
        }

        sidebar.hidden {
            transform: translateX(100%);
        }

        .sidebar-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #ffffff;
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #c8dcd0;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        .sidebar-title {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: bold;
            color: #1b4d2e;
        }

        /* زر السهم لإخفاء/إظهار الشريط */
        .toggle-btn {
            background-color: #1b4d2e;
            color: white;
            border: none;
            width: 32px;
            height: 32px;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
        }

        .toggle-btn:hover {
            background-color: #12351f;
        }

        .nav-section-title {
            font-size: 14px;
            color: #1b4d2e;
            margin-bottom: 12px;
            font-weight: bold;
        }

        .nav-item {
            background: #ffffff;
            border: 1px solid #c8dcd0;
            padding: 12px 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.2s;
            font-weight: 500;
            color: #1b4d2e;
        }

        .nav-item:hover {
            background-color: #f0f7f2;
            border-color: #1b4d2e;
        }

        .nav-item input[type="radio"] {
            accent-color: #1b4d2e;
        }

        /* مساحة العرض الرئيسية */
        .content-area {
            flex: 1;
            padding: 30px;
            overflow-y: auto;
            margin-right: 280px; /* نفس عرض الشريط الجانبي */
            transition: margin-right 0.3s ease;
        }

        .content-area.expanded {
            margin-right: 0;
        }

        .page-content {
            display: none;
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            min-height: 400px;
        }

        .page-content.active {
            display: block;
        }

        h2 {
            color: #1b4d2e;
            margin-bottom: 20px;
        }

        /* نافذة إدخال الباسورد */
        .password-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            justify-content: center;
            align-items: center;
            z-index: 100;
        }

        .password-box {
            background: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            width: 320px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .password-box h3 {
            margin-bottom: 15px;
            color: #1b4d2e;
        }

        .password-box input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 6px;
            margin-bottom: 15px;
            text-align: center;
            font-size: 16px;
        }

        .password-box button {
            background-color: #1b4d2e;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }

        .password-box button:hover {
            background-color: #12351f;
        }

        .error-msg {
            color: red;
            font-size: 12px;
            margin-top: -10px;
            margin-bottom: 10px;
            display: none;
        }
    </style>
</head>
<body>

    <!-- الهيدر العلوي (تمت إزالة كلمة القائمة تماماً وبقاء اللوجو) -->
    <header>
        <div class="logo-container">
            <!-- ضع رابط أو اسم اللوجو الخاص بك هنا -->
            <img src="https://via.placeholder.com/150x50?text=Sun+Pyramids" alt="Sun Pyramids Tours">
        </div>
    </header>

    <!-- المحتوى الرئيسي -->
    <div class="main-container">
        
        <!-- الشريط الجانبي -->
        <sidebar id="sidebar">
            <div class="sidebar-header">
                <div class="sidebar-title">
                    <span>🧭</span> القائمة الرئيسية
                </div>
                <!-- زر السهم لإخفاء الشريط -->
                <button class="toggle-btn" onclick="toggleSidebar()" title="إخفاء القائمة">◀</button>
            </div>

            <div class="nav-section-title">اختر الصفحة</div>

            <label class="nav-item">
                <input type="radio" name="pageNav" checked onclick="switchPage('filterPage', false)">
                <span>نموذج تصفية المرشد</span>
            </label>

            <label class="nav-item">
                <input type="radio" name="pageNav" onclick="switchPage('managePage', true)">
                <span>إدارة التصفيات</span>
            </label>

            <label class="nav-item">
                <input type="radio" name="pageNav" onclick="switchPage('archivePage', true)">
                <span>الأرشيف</span>
            </label>
        </sidebar>

        <!-- زر إظهار الشريط الجانبي في حال كان مخفياً (اختياري يظهر ع الشاشة) -->
        <button id="showSidebarBtn" onclick="toggleSidebar()" style="position: absolute; right: 15px; top: 15px; z-index: 4; display: none; background: #1b4d2e; color: white; border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer;">
            ▶ إظهار القائمة
        </button>

        <!-- مساحة العرض -->
        <div class="content-area" id="contentArea">
            
            <!-- صفحة نموذج تصفية المرشد -->
            <div id="filterPage" class="page-content active">
                <h2>نموذج تصفية المرشد</h2>
                <p>هنا يتم عرض نموذج تصفية وإدخال بيانات المرشدين السياحيين والمصاريف.</p>
            </div>

            <!-- صفحة إدارة التصفيات -->
            <div id="managePage" class="page-content">
                <h2>إدارة التصفيات</h2>
                <p>هنا يتم إدارة ومراجعة التصفيات المسجلة.</p>
            </div>

            <!-- صفحة الأرشيف -->
            <div id="archivePage" class="page-content">
                <h2>الأرشيف</h2>
                <p>هنا يتم عرض الأرشيف والسجلات القديمة.</p>
            </div>

        </div>
    </div>

    <!-- نافذة طلب الباسورد للإدارة والأرشيف -->
    <div class="password-modal" id="passwordModal">
        <div class="password-box">
            <h3>يرجى إدخال كلمة المرور</h3>
            <input type="password" id="passInput" placeholder="كلمة المرور">
            <div class="error-msg" id="errorMsg">كلمة المرور غير صحيحة!</div>
            <br>
            <button onclick="verifyPassword()">دخول</button>
            <button onclick="cancelPassword()" style="background: #ccc; color: #333; margin-right: 5px;">إلغاء</button>
        </div>
    </div>

    <script>
        let targetPageId = '';
        let targetRadio = null;
        const correctPassword = "123"; // يمكنك تغيير الباسورد من هنا بسهولة

        // دالة إخفاء وإظهار الشريط الجانبي
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const contentArea = document.getElementById('contentArea');
            const showBtn = document.getElementById('showSidebarBtn');

            sidebar.classList.toggle('hidden');
            contentArea.classList.toggle('expanded');

            if (sidebar.classList.contains('hidden')) {
                showBtn.style.display = 'block';
            } else {
                showBtn.style.display = 'none';
            }
        }

        // التنقل بين الصفحات مع التحقق من الباسورد للصفحات المحمية
        function switchPage(pageId, requiresPassword) {
            const radios = document.querySelectorAll('input[name="pageNav"]');
            
            if (requiresPassword) {
                targetPageId = pageId;
                // حفظ الراديو الحالي لنفترض لو أخطأ في الباسورد نرجع الراديو لصفحة التصفية
                document.getElementById('passwordModal').style.display = 'flex';
                document.getElementById('passInput').value = '';
                document.getElementById('errorMsg').style.display = 'none';
                document.getElementById('passInput').focus();
            } else {
                executePageSwitch(pageId);
            }
        }

        function executePageSwitch(pageId) {
            // إخفاء كل الصفحات
            document.querySelectorAll('.page-content').forEach(page => {
                page.classList.remove('active');
            });
            // إظهار الصفحة المطلوبة
            document.getElementById(pageId).classList.add('active');
        }

        function verifyPassword() {
            const inputVal = document.getElementById('passInput').value;
            if (inputVal === correctPassword) {
                document.getElementById('passwordModal').style.display = 'none';
                executePageSwitch(targetPageId);
            } else {
                document.getElementById('errorMsg').style.display = 'block';
            }
        }

        function cancelPassword() {
            document.getElementById('passwordModal').style.display = 'none';
            // إعادة تفعيل زر "نموذج تصفية المرشد" إذا ألغى الباسورد
            const radios = document.querySelectorAll('input[name="pageNav"]');
            radios[0].checked = true;
            executePageSwitch('filterPage');
        }

        // السماح بالدخول عبر مفتاح Enter
        document.getElementById('passInput').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                verifyPassword();
            }
        });
    </script>
</body>
</html>
