#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Example Google style docstrings.
"""

import sys
import os
import re
import json
import http.client
import base64

import requests
import redis


DB = redis.StrictRedis(host='localhost', port=6379)

AUTH = ('spetz911', os.environ['GITHUB_AUTH'])

ORGS = ['google']

REPOS = [
    ('apache/httpcomponents-client', '4.6.x'),
    ('google/guice', 'master'),
]

def to_native_string(string, encoding='ascii'):
    if isinstance(string, str):
        out = string
    else:
        out = string.decode(encoding)

    return out

def call_api(url):
    "doscstr"
    username, password = AUTH
    authstr = 'Basic ' + to_native_string(
        base64.b64encode(b':'.join((username, password))).strip()
    )
    conn = http.client.HTTPSConnection("www.python.org")
    conn.request("GET", "/", headers={"Authorization": authstr})

    cached = DB.get(url)
    if cached:
        return json.loads(cached)
    else:
        response = requests.get(url, auth=AUTH)
        DB.set(url, response.text)
        return response.json()


BLACK_LIST = [
    "/test/com/",
    "/test/org/",
    "/src/examples/",
    "/package-info.java",
    "/package-info.java",
    "/src/main/java-deprecated/",
    "examples/src/",
    "lib/build/"
]


def process_one_file(full_name, file_node, branch=None):
    """     ....   """
    if not file_node.endswith(".java"):
        return
    if "/src/test/java/" in file_node:
        return
    for tmp in BLACK_LIST:
        if tmp in file_node:
            return
    # otherwise
    search = re.compile(
        r"[-_\w/]*/src/main/java/([\w/]*).java$").search(file_node)
    search = search or re.compile(
        r"[-_\w/]*/src/(org/[\w/]*).java$").search(file_node)
    search = search or re.compile(
        r"[-_\w/]*/src/(com/[\w/]*).java$").search(file_node)
    if not search:
        print("can not extract package name:", file_node)
        exit(1)
    package_name = search and search.groups()[0].replace("/", ".")

    # DB.set(class_package, full_name)
    # repo_url = "https://github.com/" + repo['full_name']
    # url = "/".join([repo_url, "blob", repo['default_branch'], file_node])

    url = f"https://github.com/{full_name}/blob/{branch}/{file_node}"
    tmp = DB.get(package_name)
    tmp = tmp and tmp.decode()
    if not tmp:
        DB.set(package_name, url)
        # print(package_name)
        # print(url)
        # print("================")
    elif tmp != url:
        print('error:', file=sys.stderr)
        print(tmp, file=sys.stderr)
        print(url, file=sys.stderr)
        print('----------', file=sys.stderr)
    else:
        pass


def process_one_repo(repo):
    "doscstr"
    data2 = call_api(repo['branches_url']
                     .format_map({'/branch': '/' + repo['default_branch']}))
    tree = call_api(repo['trees_url']
                    .format_map({'/sha': '/' + data2['commit']['sha']}) +
                    "?recursive=1")
    for file_node in tree['tree']:
        process_one_file(repo, file_node['path'])


def process_one_org():
    "doscstr"
    for org in ORGS:
        url = f"https://api.github.com/orgs/{org}/repos"
        response = call_api(url)
        for item in response[:3]:
            process_one_repo(item)


def process_given_repo(full_name, branch):
    "doscstr"
    sha = call_api(
        f"https://api.github.com/repos/{full_name}/branches/{branch}")['commit']['sha']
    # print("sha =", sha)
    tree = call_api(
        f"https://api.github.com/repos/{full_name}/git/trees/{sha}?recursive=1")
    # print("tree =", tree)
    for file_node in tree['tree']:
        process_one_file(full_name, file_node['path'], branch)


def main():
    "doscstr"
    for full_name, branch in REPOS:
        process_given_repo(full_name, branch)


if __name__ == '__main__':
    main()
