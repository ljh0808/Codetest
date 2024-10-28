#!/usr/bin/env python
import os
from datetime import datetime
import subprocess
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

def main():
    total_problems = 0
    baekjoon_count = 0
    programmers_count = 0
    content = ""

    platform_problems = {"백준": [], "프로그래머스": []}

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

            file_path = os.path.join(root, file).replace('\\', '/')
            if file_path.startswith('./'):
                file_path = file_path[2:]
            
            commit_url = get_commit_url(file_path)

            if platform == "백준":
                problem_number = os.path.basename(os.path.dirname(file_path))
                problem_title = get_boj_problem_title(problem_number)
                problem_link = f"https://www.acmicpc.net/problem/{problem_number}"
                baekjoon_count += 1
                platform_problems[platform].append(
                    f"|{problem_number}|{problem_title}|[문제]({problem_link})|[코드]({commit_url})|\n"
                )
                sleep(0.5)  # API 호출 제한 방지
            
            else:  # 프로그래머스
                # 파일명에서 확장자를 제외한 문제 번호 추출
                problem_number = os.path.splitext(os.path.basename(file_path))[0]
                problem_title = os.path.basename(os.path.dirname(file_path))
                # 프로그래머스 문제 링크 형식으로 수정
                problem_link = f"https://school.programmers.co.kr/learn/courses/30/lessons/{problem_number}"
                programmers_count += 1
                platform_problems[platform].append(
                    f"|{problem_number}|{problem_title}|[문제]({problem_link})|[코드]({commit_url})|\n"
                )

            total_problems += 1

    # 백준과 프로그래머스 표를 content에 추가
    for platform, problems in platform_problems.items():
        content += f"\n## 📚 {platform}\n"
        content += "| 문제번호 | 제목 | 링크 | 소스 코드 |\n"
        content += "| ----- | ----- | ----- | ----- |\n"
        content += ''.join(sorted(problems))  # 문제 번호순으로 정렬

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
