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
    return any(filename.endswith(ext) for ext in ['.py', '.java', '.cpp', '.c', '.js', '.kt'])

def get_boj_problem_info(file_path):
    problem_number = os.path.basename(os.path.dirname(file_path))
    try:
        url = f"https://solved.ac/api/v3/problem/show?problemId={problem_number}"
        response = requests.get(url, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            data = response.json()
            return {
                'number': problem_number,
                'title': data.get('titleKo', 'Unknown Title'),
                'link': f"https://www.acmicpc.net/problem/{problem_number}"
            }
    except Exception as e:
        print(f"Error fetching BOJ problem {problem_number}: {e}")
    return None

def get_programmers_problem_info(file_path):
    problem_dir = os.path.basename(os.path.dirname(file_path))
    problem_number = ''
    problem_title = ''
    
    # Extract problem number and title from directory name
    # Expected format: "12345_문제제목" or "문제제목_12345"
    parts = problem_dir.split('_')
    for part in parts:
        if part.isdigit():
            problem_number = part
        else:
            problem_title = part
    
    if problem_number:
        return {
            'number': problem_number,
            'title': problem_title,
            'link': f"https://school.programmers.co.kr/learn/courses/30/lessons/{problem_number}"
        }
    return None

def process_solutions():
    platform_problems = {"백준": [], "프로그래머스": []}
    counts = {"백준": 0, "프로그래머스": 0}

    for root, _, files in os.walk("."):
        if any(skip in root for skip in ['.git', '.github', 'images']):
            continue
        
        if "백준" in root:
            platform = "백준"
        elif "프로그래머스" in root:
            platform = "프로그래머스"
        else:
            continue

        for file in files:
            if not is_solution_file(file):
                continue

            file_path = os.path.join(root, file).replace('\\', '/')
            if file_path.startswith('./'):
                file_path = file_path[2:]
            
            problem_info = None
            if platform == "백준":
                problem_info = get_boj_problem_info(file_path)
                sleep(0.5)  # API 호출 제한 방지
            else:
                problem_info = get_programmers_problem_info(file_path)

            if problem_info:
                commit_url = get_commit_url(file_path)
                platform_problems[platform].append(
                    f"|{problem_info['title']}|{problem_info['number']}|[문제]({problem_info['link']})|[코드]({commit_url})|\n"
                )
                counts[platform] += 1

    return platform_problems, counts

def main():
    platform_problems, counts = process_solutions()
    total_problems = sum(counts.values())
    
    content = HEADER.format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_problems,
        counts["백준"],
        counts["프로그래머스"]
    )

    for platform, problems in platform_problems.items():
        content += f"\n## 📚 {platform}\n"
        content += "| 제목 | 문제번호 | 링크 | 소스 코드 |\n"
        content += "| ----- | ----- | ----- | ----- |\n"
        content += ''.join(sorted(problems, key=lambda x: x.split('|')[2]))  # 문제번호 기준 정렬

    with open("README.md", "w", encoding='utf-8') as fd:
        fd.write(content)

if __name__ == "__main__":
    main()
