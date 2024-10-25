#!/usr/bin/env python

import os
from urllib import parse
from datetime import datetime

HEADER = """# 백준, 프로그래머스 문제 풀이 목록
마지막 업데이트: {}

"""

def main():
    content = ""
    content += HEADER.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    directories = []
    solveds = {}  # 문제 플랫폼별로 문제들을 저장하기 위한 딕셔너리
    
    for root, dirs, files in os.walk("."):
        dirs.sort()
        if root == '.':
            for dir in ('.git', '.github'):
                try:
                    dirs.remove(dir)
                except ValueError:
                    pass
            continue
        
        category = os.path.basename(root)
        
        if category == 'images':
            continue
            
        directory = os.path.basename(os.path.dirname(root))
        
        if directory == '.':
            continue
            
        # 새로운 플랫폼(디렉토리) 처리
        if directory not in directories:
            if directory in ["백준", "프로그래머스"]:
                content += f"\n## 📚 {directory}\n"
                solveds[directory] = []  # 새로운 플랫폼의 문제 목록 초기화
                content += "| 문제번호 | 링크 |\n"
                content += "| ----- | ----- |\n"
            directories.append(directory)
            
        # 파일 처리
        for file in files:
            problem_number = category
            if problem_number not in solveds.get(directory, []):
                # 상대 경로로 링크 생성
                relative_path = os.path.join(root, file).replace('\\', '/')
                if relative_path.startswith('./'):
                    relative_path = relative_path[2:]
                content += f"|{problem_number}|[링크]({parse.quote(relative_path)})|\n"
                if directory in solveds:
                    solveds[directory].append(problem_number)
        
    # README.md 파일 쓰기 (utf-8 인코딩 명시)
    with open("README.md", "w", encoding='utf-8') as fd:
        fd.write(content)
    
if __name__ == "__main__":
    main()
