import streamlit as st

st.set_page_config(layout="wide", page_title="Sun Pyramids Tours - تصفية المرشدين")

html_code = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
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
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 10;
        }

        .logo-container img {
            height: 45px;
        }

        /* المحتوى الرئيسي */
        .main-container {
            display: flex;
            margin-top: 70px;
            height: calc(100vh - 70px);
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
            font-weight: 500;
            color: #1b4d2e;
            transition: 0.2s;
        }

        .nav-item:hover {
            background-color: #f0f7f2;
            border-color: #1b4d2e;
        }

        /* مساحة العرض */
        .content-area {
            flex: 1;
            padding: 30px;
            overflow-y: auto;
            margin-right: 280px;
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

        /* نافذة الباسورد */
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
    </style>
</head>
<body>

    <header>
        <div class="logo-container">
            <img src="https://via.placeholder.com/150x45?text=Sun+Pyramids+Tours" alt="Sun Pyramids Tours">
        </div>
    </header>

    <div class="main-container">
        <sidebar id="sidebar">
            <div class="sidebar-header">
                <div class="sidebar-title"><span>🧭</span> القائمة الرئيسية</div>
                <button class="toggle-btn" onclick="toggleSidebar()">◀</button>
            </div>

            <div class="nav-section-title">اختر الصفحة</div>

            <div class="nav-item" onclick="switchPage('filterPage', false)">
                <span>⚪ نموذج تصفية المرشد</span>
            </div>
            <div class="nav-item" onclick="switchPage('managePage', true)">
                <span>🔒 إدارة التصفيات</span>
            </div>
            <div class="nav-item" onclick="switchPage('archivePage', true)">
                <span>🔒 الأرشيف</span>
            </div>
        </sidebar>

        <button id="showSidebarBtn" onclick="toggleSidebar()" style="position: fixed; right: 15px; top: 85px; z-index: 4; display: none; background: #1b4d2e; color: white; border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer;">
            ▶ إظهار القائمة
        </button>

        <div class="content-area" id="contentArea">
            <div id="filterPage" class="page-content active">
                <h2>نموذج تصفية المرشد</h2>
                <p>هنا يتم عرض نموذج تصفية وإدخال بيانات المرشدين السياحيين والمصاريف.</p>
            </div>

            <div id="managePage" class="page-content">
                <h2>إدارة التصفيات</h2>
                <p>هنا يتم إدارة ومراجعة التصفيات المسجلة.</p>
            </div>

            <div id="archivePage" class="page-content">
                <h2>الأرشيف</h2>
                <p>هنا يتم عرض الأرشيف والسجلات القديمة.</p>
            </div>
        </div>
    </div>

    <div class="password-modal" id="passwordModal">
        <div class="password-box">
            <h3>يرجى إدخال كلمة المرور</h3>
            <input type="password" id="passInput" placeholder="كلمة المرور">
            <div id="errorMsg" style="color:red; font-size:12px; display:none; margin-bottom:10px;">كلمة المرور غير صحيحة!</div>
            <button onclick="verifyPassword()">دخول</button>
            <button onclick="cancelPassword()" style="background: #ccc; color: #333; margin-right: 5px;">إلغاء</button>
        </div>
    </div>

    <script>
        let targetPageId = '';
        const correctPassword = "159753";

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

        function switchPage(pageId, requiresPassword) {
            if (requiresPassword) {
                targetPageId = pageId;
                document.getElementById('passwordModal').style.display = 'flex';
                document.getElementById('passInput').value = '';
                document.getElementById('errorMsg').style.display = 'none';
                document.getElementById('passInput').focus();
            } else {
                executePageSwitch(pageId);
            }
        }

        function executePageSwitch(pageId) {
            document.querySelectorAll('.page-content').forEach(page => {
                page.classList.remove('active');
            });
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
            executePageSwitch('filterPage');
        }
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=750, scrolling=True)
