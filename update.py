#!/usr/bin/env python
import os
from urllib import parse
from datetime import datetime
import subprocess
import re

HEADER = """# 백준, 프로그래머스 문제 풀이 목록
마지막 업데이트: {}

[![Solved.ac Profile](http://mazassumnida.wtf/api/v2/generate_badge?boj=ljh0808)](https://solved.ac/ljh0808)

## 🚀 문제 풀이 현황
- 총 문제 수: {}개
- 백준: {}개
- 프로그래머스: {}개
"""

def get_commit_url(file_path):
    try:
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
            
        return f"{remote_url}/blob/{git_hash}/{file_path}"
    except subprocess.CalledProcessError:
        return "#"

def get_problem_title(platform, problem_number):
    # 나중에 API를 통해 문제 제목을 가져올 수 있도록 준비
    return ""

def main():
    total_problems = 0
    baekjoon_count = 0
    programmers_count = 0
    
    content = ""
    directories = []
    solveds = {}
    
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
                solveds[directory] = []
                content += "| 문제번호 | 링크 | 소스 코드 |\n"
                content += "| ----- | ----- | ----- |\n"
            directories.append(directory)
            
        # 파일 처리
        for file in files:
            problem_number = category
            if problem_number not in solveds.get(directory, []):
                file_path = os.path.join(root, file).replace('\\', '/')
                if file_path.startswith('./'):
                    file_path = file_path[2:]
                
                # GitHub 소스 코드 링크 생성
                commit_url = get_commit_url(file_path)
                
                # 플랫폼별 문제 링크 생성
                if directory == "백준":
                    problem_link = f"https://www.acmicpc.net/problem/{problem_number}"
                    baekjoon_count += 1
                elif directory == "프로그래머스":
                    problem_link = f"https://school.programmers.co.kr/learn/courses/30/lessons/{problem_number}"
                    programmers_count += 1
                else:
                    problem_link = "#"
                
                content += f"|{problem_number}|[문제]({problem_link})|[코드]({commit_url})|\n"
                if directory in solveds:
                    solveds[directory].append(problem_number)
                total_problems += 1
    
    # 최종 README 내용 생성
    final_content = HEADER.format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_problems,
        baekjoon_count,
        programmers_count
    ) + content
    
    # README.md 파일 쓰기
    with open("README.md", "w", encoding='utf-8') as fd:
        fd.write(final_content)
    
if __name__ == "__main__":
    main()
