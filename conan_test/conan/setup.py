#!/usr/bin/env python3

"""
✅ Python 3.6 이상 필요
✅ Conan (pip install conan) 설치 필요

사용법:
python setup.py
"""

import subprocess
import os
import sys

# 내 프로젝트의 .vcxproj 파일 경로
VCXPROJ_FILE = 'conan_test.vcxproj'

DEBUG_IMPORT = '<Import Condition="\'$(Configuration)\' == \'Debug\'" Project="conan\\conanbuild\\debug\\conandeps.props" />'
RELEASE_IMPORT = '<Import Condition="\'$(Configuration)\' == \'Release\'" Project="conan\\conanbuild\\release\\conandeps.props" />'

# conan 으로 library 설치
def run_conan_install():
    print('📦 Running Conan install...')
    subprocess.run(['conan', 'install', '.', '--profile:host=./profile_debug', '--profile:build=./profile_debug', '--output-folder=conanbuild/debug', '--build=missing'], check=True)
    subprocess.run(['conan', 'install', '.', '--profile:host=./profile_release', '--profile:build=./profile_release', '--output-folder=conanbuild/release', '--build=missing'], check=True)
    print('✅ Conan install completed.\n\n')
    
# 프로젝트와 conan으로 설치한 library 연결
def modify_vcxproj():
    print('📦 start .vcxproj modified with Conan imports.')

    os.chdir('..') # root 프로젝트로 디렉토리 변경
    with open(VCXPROJ_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 중복 여부 체크
    has_debug = any(DEBUG_IMPORT in line for line in lines)
    has_release = any(RELEASE_IMPORT in line for line in lines)
    if has_debug or has_release:
        print('ℹ️  Conan imports already exist in .vcxproj, skipping modification.')
        return

    new_lines = []
    for line in lines:
        if '<Import Project="$(VCTargetsPath)\\Microsoft.Cpp.Default.props"' in line:
            new_lines.append(f'{DEBUG_IMPORT}\n')
            new_lines.append(f'{RELEASE_IMPORT}\n')
        new_lines.append(line)
    
    with open(VCXPROJ_FILE, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print('✅ end .vcxproj modified with Conan imports.')

def main():
    try:
        run_conan_install()
        modify_vcxproj()
        print('🎉 Setup complete.')
    except subprocess.CalledProcessError as e:
        print(f'❌ Error running command: {e.cmd}')
        sys.exit(1)
    except Exception as e:
        print(f'❌ Unexpected error: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()
