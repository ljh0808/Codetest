#!/usr/bin/env python
import os
from urllib import parse
from datetime import datetime
import subprocess

HEADER = """# 백준, 프로그래머스 문제 풀이 목록
마지막 업데이트: {}
"""

def get_file_info(file_path):
    try:
        # 파일의 최초 커밋 날짜 가져오기
        git_log = subprocess.check_output(
            ['git', 'log', '--follow', '--format=%ad', '--date=format:%y-%m-%d', file_path],
            encoding='utf-8'
        ).strip().split('\n')
        commit_date = git_log[-1] if git_log else "N/A"
        
        # 파일의 가장 최근 커밋 해시 가져오기
        git_hash = subprocess.check_output(
            ['git', 'log', '-n', '1', '--format=%H', file_path],
            encoding='utf-8'
        ).strip()
        
        # GitHub 저장소 URL 가져오기
        remote_url = subprocess.check_output(
            ['git', 'config', '--get', 'remote.origin.url'],
            encoding='utf-8'
        ).strip()
        
        # GitHub URL 형식 변환
        if remote_url.endswith('.git'):
            remote_url = remote_url[:-4]
        if remote_url.startswith('git@github.com:'):
            remote_url = 'https://github.com/' + remote_url[15:]
            
        commit_url = f"{remote_url}/blob/{git_hash}/{file_path}"
        
        return commit_date, commit_url
    except subprocess.CalledProcessError:
        return "N/A", "#"

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
                content += "| 문제번호 | 푼 날짜 | 소스 코드 |\n"
                content += "| ----- | ----- | ----- |\n"
            directories.append(directory)
            
        # 파일 처리
        for file in files:
            problem_number = category
            if problem_number not in solveds.get(directory, []):
                file_path = os.path.join(root, file).replace('\\', '/')
                if file_path.startswith('./'):
                    file_path = file_path[2:]
                    
                # 커밋 날짜와 링크 가져오기
                commit_date, commit_url = get_file_info(file_path)
                
                content += f"|{problem_number}|{commit_date}|[코드]({commit_url})|\n"
                if directory in solveds:
                    solveds[directory].append(problem_number)
        
    # README.md 파일 쓰기 (utf-8 인코딩 명시)
    with open("README.md", "w", encoding='utf-8') as fd:
        fd.write(content)
    
if __name__ == "__main__":
    main()
