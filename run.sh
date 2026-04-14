#!/bin/bash
# BBrose Employee Insight Platform - Startup Script
# ═══════════════════════════════════════════════════

echo ""
echo "  ╔══════════════════════════════════════════╗"
echo "  ║   BBrose — Employee Insight Platform     ║"
echo "  ║   A New Digital Generation               ║"
echo "  ╚══════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Please install it first."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install django pillow qrcode reportlab openpyxl --break-system-packages -q 2>/dev/null || \
pip install django pillow qrcode reportlab openpyxl -q 2>/dev/null

# Run migrations
echo "🗄️  Setting up database..."
python3 manage.py makemigrations questionnaire --noinput 2>/dev/null
python3 manage.py migrate --noinput 2>/dev/null

# Create superuser if not exists
echo "👤 Setting up admin user..."
python3 -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bbrose_project.settings')
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='amine').exists():
    User.objects.create_superuser('amine', 'amine@bbrose.com', 'aminehd2004')
    print('   Admin created: amine / aminehd2004')
else:
    print('   Admin already exists: amine / aminehd2004')
" 2>/dev/null

echo ""
echo "  ✅ Ready!"
echo ""
echo "  🌐 App:    http://127.0.0.1:8000/"
echo "  🔧 Admin:  http://127.0.0.1:8000/admin/"
echo "  👤 Login:  amine / aminehd2004"
echo ""
echo "  Press Ctrl+C to stop the server."
echo ""

python3 manage.py runserver 0.0.0.0:8000
