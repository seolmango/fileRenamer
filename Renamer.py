import os
import re
import ast

# 에러 정의
class NotSetedVariableError(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

# 함수 정의
def print_version():
    print("""\
\x1b[1;36m================================
|<reNamer> - Version 2023/04/23|
|                              |
|            made by Seolmango |
================================\x1b[1;m""")
    print()
    return None

def set_folder_path():
    print_version()
    FOLDERPATH = input(f"폴더 경로를 입력하세요(기준은 {os.getcwd()}): ")
    if FOLDERPATH == "":
        FOLDERPATH = os.getcwd()
    FOLDERFILES = os.listdir(FOLDERPATH)
    if len(FOLDERFILES) == 0:
        print("폴더에 파일이 없습니다.")
        exit()
    elif len(FOLDERFILES) <= 20:
        print(f"폴더에 있는 파일의 수: {len(FOLDERFILES)}")
        for index, name in enumerate(FOLDERFILES):
            print(f"{index+1}. {name}")
    else:
        print(f"폴더에 있는 파일의 수: {len(FOLDERFILES)}")
        for index, name in enumerate(FOLDERFILES[:20]):
            print(f"{index+1}. {name}")
        print("...")
        print(f"{len(FOLDERFILES)-20}개의 파일이 더 있습니다.")
    if input("이 폴더가 맞습니까? (Y/N): ").lower() == "y":
        os.system("cls")
        return FOLDERPATH
    else:
        return set_folder_path()

def set_search_pattern(file_path):
    print_version()
    files = os.listdir(file_path)
    print("""\
[검색 패턴 문법]
1. 기존 파일 이름에서 찾은 변수를 사용할때는 (?P<변수명>패턴)으로 사용합니다.
2. 패턴은 기본적으로 정규식을 사용합니다.
- [a-z] : a부터 z까지의 문자
- \d{글자수}, \w{글자수}, \s{글자수} : 숫자, 문자, 공백으로 이루어진 글자수만큼의 문자
- 더 많은 패턴은 https://docs.python.org/ko/3/library/re.html 에서 확인하세요.
""")
    PATTERN = input("패턴을 입력하세요: ")
    PATTERN = re.compile(PATTERN)
    result = pattern_search(files, PATTERN)
    if len(result) == 0:
        print("패턴에 일치하는 파일이 없습니다.")
        if input("다시 입력하시겠습니까? (Y/N): ").lower() == "y":
            os.system("cls")
            return set_search_pattern(file_path)
        else:
            exit()
    elif len(result) <= 20:
        print(f"패턴에 일치하는 파일의 수: {len(result)}")
        for index, name in enumerate(result):
            print(f"{index+1}. {name[0]} | {name[1]}")
    else:
        print(f"패턴에 일치하는 파일의 수: {len(result)}")
        for index, name in enumerate(result[:20]):
            print(f"{index+1}. {name[0]} | {name[1]}")
        print("...")
        print(f"{len(result)-20}개의 파일이 더 있습니다.")
    if input("이 패턴이 맞습니까? (Y/N): ").lower() == "y":
        os.system("cls")
        return result

def set_new_folder_path():
    print_version()
    NEWFOLDERPATH = input(f"새로운 폴더 경로를 입력하세요(기준은 {os.getcwd()}): ")
    if NEWFOLDERPATH == "":
        NEWFOLDERPATH = os.getcwd()
    if os.path.exists(NEWFOLDERPATH):
        print("이미 존재하는 폴더입니다.")
        if input("이 폴더에 파일을 이동하시겠습니까? (Y/N): ").lower() == "y":
            os.system("cls")
            return NEWFOLDERPATH
        else:
            return set_new_folder_path()
    else:
        os.mkdir(NEWFOLDERPATH)
        os.system("cls")
        return NEWFOLDERPATH

def set_rename_pattern(files):
    print_version()
    print("""\
[이름 설정 패턴 문법]
1. 기존 파일 이름에서 찾은 변수를 사용할때는 {변수명}으로 사용합니다.
2. <(파이썬 코드)>는 그 자리에 그 코드의 실행 결과를 넣습니다. 이 코드 안에도 변수를 넣을 수 있습니다.
- Counter는 1부터 시작하는 특수한 변수입니다. 변수 Counter는 파일의 순서를 만들 때 사용가능합니다.
""")
    NEWPATTERN = input("새로운 패턴을 입력하세요: ")
    new_preview = []
    for index, file in enumerate(files):
        try:
            new_preview.append([file, rename_pattern(NEWPATTERN, file[1], index,file[0])])
        except NotSetedVariableError as e:
            print(e)
    if len(new_preview) == 0:
        print("패턴에 일치하는 파일이 없습니다.")
        if input("다시 입력하시겠습니까? (Y/N): ").lower() == "y":
            os.system("cls")
            return set_rename_pattern(files, NEWPATTERN)
        else:
            exit()
    elif len(new_preview) <= 20:
        print(f"패턴에 일치하는 파일의 수: {len(new_preview)}")
        for index, name in enumerate(new_preview):
            print(f"{index+1}. {name[0]} => {name[1]}")
    else:
        print(f"패턴에 일치하는 파일의 수: {len(new_preview)}")
        for index, name in enumerate(new_preview[:20]):
            print(f"{index+1}. {name[0]} => {name[1]}")
        print("...")
        print(f"{len(new_preview)-20}개의 파일이 더 있습니다.")
    print("\033[31m" + "주의! 한번 실행된 작업은 되돌릴 수 없습니다" + "\033[0m")
    if input("이 패턴이 맞습니까? (Y/N): ").lower() == "y":
        os.system("cls")
        return new_preview
    else:
        os.system("cls")
        return set_rename_pattern(files)
    
def pattern_search(files, pattern):
    result = []
    for file in files:
        match = re.match(pattern, file)
        if match:
            result.append([file,match.groupdict()])
    return result

def rename_pattern(pattern, vars, index,name):
    vars["Counter"] = index+1
    new_word = ""
    if pattern == "":
        return name
    i = 0
    while i < len(pattern):
        if pattern[i] == "{":
            j = i+1
            while pattern[j] != "}":
                j += 1
            if pattern[i+1:j] not in vars:
                raise NotSetedVariableError(f"기존 파일 이름에서 {pattern[i+1:j]}을(를) 찾을 수 없습니다.")
            new_word += str(vars[pattern[i+1:j]])
            i = j
        elif pattern[i] == "<":
            j = i+1
            while pattern[j] != ">":
                j += 1
            code = pattern[i+1:j]
            for i in vars.keys():
                code = code.replace(f"{i}", str(vars[i]))
            code = code.replace(" ", "")
            code = ast.literal_eval(code)
            new_word += str(code)
            i = j
        else:
            new_word += pattern[i]
        i += 1
    return new_word

if __name__ == "__main__":
    FOLDERPATH = set_folder_path()
    result = set_search_pattern(FOLDERPATH)
    NEWFOLDERPATH = set_new_folder_path()
    new_preview = set_rename_pattern(result)
    for old, new in new_preview:
        os.rename(os.path.join(FOLDERPATH, old[0]), os.path.join(NEWFOLDERPATH, new))
    print("작업이 완료되었습니다.")