#!/usr/bin/env python
import os
from datetime import datetime
import subprocess
import re
import requests
from time import sleep

HEADER = """# 백준, 프로그래머스 문제 풀이 목록

마지막 업데이트: {}

[![Solved.ac Profile](http://mazassumnida.wtf/api/v2/generate_badge?boj=200732)](https://solved.ac/200732)

## 🚀 문제 풀이 현황
- 총 맞춘 문제 수: {}개
- 백준: {}개
- 프로그래머스: {}개
"""

def get_commit_url(file_path):
    try:
        git_hash = subprocess.check_output(
            ['git', 'log', '-n', '1', '--format=%H', '--', file_path],
            encoding='utf-8'
        ).strip()
        
        remote_url = subprocess.check_output(
            ['git', 'config', '--get', 'remote.origin.url'],
            encoding='utf-8'
        ).strip()
        
        if remote_url.endswith('.git'):
            remote_url = remote_url[:-4]
        if remote_url.startswith('git@github.com:'):
            remote_url = 'https://github.com/' + remote_url[15:]
        
        return f"{remote_url}/blob/{git_hash}/{file_path}"
    except subprocess.CalledProcessError:
        return "#"

def is_solution_file(filename):
    extensions = ['.py', '.java', '.cpp', '.c', '.js', '.kt']
    return any(filename.endswith(ext) for ext in extensions)

def get_problem_number_from_path(path, platform):
    if platform == "백준":
        # 백준 경로에서 문제 번호 추출 (예: Codetest/백준/Bronze/1000/Main.java)
        parts = path.split(os.sep)
        for part in parts:
            if part.isdigit():  # 숫자로만 이루어진 폴더명을 문제 번호로 간주
                return part
    else:  # 프로그래머스
        numbers = re.findall(r'\d+', path)
        return numbers[-1] if numbers else None
    return None

def get_boj_problem_title(problem_number):
    try:
        url = f"https://solved.ac/api/v3/problem/show?problemId={problem_number}"
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('titleKo', 'Unknown Title')
    except Exception as e:
        print(f"Error fetching title for problem {problem_number}: {e}")
    return "Unknown Title"

def get_programmers_title_from_path(path):
    # Codetest/프로그래머스/레벨/문제 제목 형태에서 마지막 항목을 제목으로 간주
    return os.path.basename(path)

def main():
    total_problems = 0
    baekjoon_count = 0
    programmers_count = 0
    
    content = ""
    platform_problems = {"백준": set(), "프로그래머스": set()}
    
    for platform in ["백준", "프로그래머스"]:
        content += f"\n## 📚 {platform}\n"
        content += "| 문제번호 | 제목 | 링크 | 소스 코드 |\n"
        content += "| ----- | ----- | ----- | ----- |\n"
    
    for root, dirs, files in os.walk("."):
        if '.git' in root or '.github' in root or 'images' in root:
            continue
            
        platform = None
        if "백준" in root:
            platform = "백준"
        elif "프로그래머스" in root:
            platform = "프로그래머스"
            
        if not platform:
            continue
            
        for file in files:
            if not is_solution_file(file):
                continue
                
            problem_number = get_problem_number_from_path(root, platform)
            if not problem_number or problem_number in platform_problems[platform]:
                continue
                
            platform_problems[platform].add(problem_number)
            
            file_path = os.path.join(root, file).replace('\\', '/')
            if file_path.startswith('./'):
                file_path = file_path[2:]
            
            commit_url = get_commit_url(file_path)
            
            # 문제 제목 가져오기
            if platform == "백준":
                problem_title = get_boj_problem_title(problem_number)
                problem_link = f"https://www.acmicpc.net/problem/{problem_number}"
                baekjoon_count += 1
                sleep(0.5)  # API 호출 제한 방지
            else:  # 프로그래머스
                problem_title = get_programmers_title_from_path(root)  # 경로에서 문제 제목 추출
                problem_link = f"https://school.programmers.co.kr/learn/courses/30/lessons/{problem_number}"
                programmers_count += 1
            
            # 해당 플랫폼의 섹션을 찾아서 내용 추가
            problem_line = f"|{problem_number}|{problem_title}|[문제]({problem_link})|[코드]({commit_url})|\n"
            content = content.replace(
                f"## 📚 {platform}\n| 문제번호 | 제목 | 링크 | 소스 코드 |\n| ----- | ----- | ----- | ----- |\n",
                f"## 📚 {platform}\n| 문제번호 | 제목 | 링크 | 소스 코드 |\n| ----- | ----- | ----- | ----- |\n{problem_line}"
            )
            
            total_problems += 1
    
    final_content = HEADER.format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_problems,
        baekjoon_count,
        programmers_count
    ) + content
    
    with open("README.md", "w", encoding='utf-8') as fd:
        fd.write(final_content)

if __name__ == "__main__":
    main()
