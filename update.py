#!/usr/bin/env python
import os
from urllib import parse
from datetime import datetime
import subprocess
import re
import requests
import json
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

def get_boj_problem_title(problem_number):
    try:
        url = f"https://solved.ac/api/v3/problem/show?problemId={problem_number}"
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('titleKo', '')  # 한글 제목 반환
        return ""
    except Exception:
        return ""

def get_programmers_problem_title(problem_number):
    # 프로그래머스 문제 폴더 또는 파일 이름에서 제목 추출
    try:
        # "./프로그래머스/{problem_number}*" 형태로 파일을 탐색
        for root, dirs, files in os.walk("./프로그래머스"):
            # 파일명이나 폴더명에서 해당 문제 번호가 포함된 경우 찾기
            if str(problem_number) in root or any(str(problem_number) in file for file in files):
                # 문제번호 이후의 파일명이나 폴더명을 제목으로 간주
                for file in files:
                    if file.startswith(str(problem_number)):
                        # 문제번호 이후의 부분을 제목으로 간주하여 추출
                        title = file.replace(str(problem_number), '').replace('_', ' ').replace('-', ' ').strip()
                        return title
        return f"Programmers 문제 {problem_number}"  # 제목을 못 찾을 경우 기본 제목 반환
    except Exception:
        return f"Programmers 문제 {problem_number}"  # 예외 시 기본 제목 반환

def is_solution_file(filename):
    extensions = ['.py', '.java', '.cpp', '.c', '.js', '.kt']
    return any(filename.endswith(ext) for ext in extensions)

def get_problem_number_from_path(path):
    numbers = re.findall(r'\d+', path)
    return numbers[-1] if numbers else None

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
                
            problem_number = get_problem_number_from_path(root)
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
                problem_title = get_programmers_problem_title(problem_number)
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
