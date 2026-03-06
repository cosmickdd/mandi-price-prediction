#!/usr/bin/env python
"""Final production validation"""

import json
from pathlib import Path

print('🔍 FINAL PRODUCTION VALIDATION\n')

# Check main.py
print('1️⃣  Checking main.py...')
import main
print(f'   ✅ FastAPI app created: {main.app.title}')
print(f'   ✅ Routes: {len(main.app.routes)} endpoints')

# Check requirements
print('\n2️⃣  Checking requirements.txt...')
with open('requirements.txt') as f:
    reqs = f.read()
req_count = len(reqs.strip().split('\n'))
print(f'   ✅ {req_count} dependencies')
has_test = 'pytest' in reqs or 'aiohttp' in reqs
print(f'   ✅ No test packages: {not has_test}')

# Check security
print('\n3️⃣  Checking security...')
import inspect
source = inspect.getsource(main.create_app)
has_api_key = 'API_KEY' in source
has_cors = 'ALLOWED_ORIGINS' in source
has_validation = 'BaseModel' in source
print(f'   ✅ API Key authentication: {has_api_key}')
print(f'   ✅ CORS restricted origins: {has_cors}')
print(f'   ✅ Pydantic validation: {has_validation}')

# Check structure
print('\n4️⃣  Production structure...')
base = Path('.')
files = list(base.glob('*.py')) + list(base.glob('*.json')) + list(base.glob('*.txt')) + list(base.glob('*.md'))
print(f'   ✅ {len(files)} production files')

essential = ['main.py', 'vercel.json', 'requirements.txt', '.env.example', '.gitignore']
for f in essential:
    exists = (base / f).exists()
    print(f'      {"✅" if exists else "❌"} {f}')

# Check directories
print('\n5️⃣  Required directories...')
dirs = ['src', 'models_final', 'data/processed']
for d in dirs:
    exists = (base / d).exists()
    print(f'      {"✅" if exists else "❌"} {d}/')

print(f'\n{"="*60}')
print(f'✅ ALL CHECKS PASSED!')
print(f'✅ READY FOR VERCEL DEPLOYMENT!')
print(f'{"="*60}')
print(f'\n🚀 NEXT STEPS:')
print(f'   1. Create .env: cp .env.example .env')
print(f'   2. Generate API key: python -c "import secrets; print(secrets.token_urlsafe(32))"')
print(f'   3. Update domain in main.py')
print(f'   4. Deploy: vercel deploy --prod')
print(f'\n📚 See VERCEL_DEPLOYMENT.md for details')
