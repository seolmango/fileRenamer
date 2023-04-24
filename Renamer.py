import os
import re
import ast
import platform

def print_version_info():
    try:
        os.system("cls")
        print("""\
\x1b[1;36m================================
|<reNamer> - Version 2023/04/24|
|                              |
|            made by Seolmango |
================================\x1b[1;m""")
        print()
        if platform.system() != "Windows":
            print("\x1b[1;31m[주의] 이 프로그램은 윈도우 환경을 가정하고 제작된 프로그램입니다. 정상적으로 작동하지 않을 수 있습니다. \x1b[1;m")
    except Exception as e:
        print("""\
\x1b[1;31m================================
|Error Occured!!               |
================================\x1b[1;m
[details] > """+str(e))
        os.system("pause")
        exit()

def set_work_folder():
    print_version_info()
    print(f"기준 폴더 : {os.getcwd()}")
    folder_path = input("작업할 폴더를 입력하세요. > ")
    if folder_path == "":
        folder_path = os.getcwd()
    try:
        folder_files = os.listdir(folder_path)
    except FileNotFoundError:
        if input(f"폴더 '{folder_path}'가 존재하지 않습니다. 다시 입력하시겠습니까? (Y/N) > ").lower() == "y":
            return set_work_folder()
        else:
            os.system("pause")
            exit()
    else:
        print(f"해당 폴더에 존재하는 파일의 수 : {len(folder_files)}")
        for i in range(0, min(len(folder_files), 20)):
            print(f"{i+1} | {folder_files[i]}")
        if len(folder_files) > 20:
            print(f"...{len(folder_files)-20}개의 파일이 더 존재합니다.")
        if input("이대로 진행하시겠습니까? (Y/N) > ").lower() == "y":
            return folder_path
        else:
            return set_work_folder()

def set_target_files(folder_path):
    print_version_info()
    files = os.listdir(folder_path)
    print("""\
[검색 패턴 문법]
1. 기존 파일 이름에서 찾은 변수를 사용할때는 (?P<변수명>패턴)으로 사용합니다.
2. 패턴은 기본적으로 정규식을 사용합니다.
- [a-z] : a부터 z까지의 문자
- \d{글자수}, \w{글자수}, \s{글자수} : 숫자, 문자, 공백으로 이루어진 글자수만큼의 문자
- 더 많은 패턴은 https://docs.python.org/ko/3/library/re.html 에서 확인하세요.
""")
    pattern_raw = input("패턴을 입력하세요 > ")
    try:
        pattern = re.compile(pattern_raw)
    except Exception:
        print("패턴이 올바르지 않습니다. 다시 입력해주세요.")
        os.system("pause")
        return set_target_files(folder_path)
    else:
        result = []
        try:
            for file in files:
                match_data = re.match(pattern, file)
                if match_data:
                    result.append([file, match_data.groupdict()])
        except Exception:
            print("에러가 발생했습니다. 다시 입력해주세요.")
            os.system("pause")
            return set_target_files(folder_path)
        else:
            print(f"검색 결과 : {len(result)}개의 파일이 검색되었습니다.")
            for i in range(0, min(len(result), 20)):
                print(f"{i+1} | {result[i][0]}")
            if len(result) > 20:
                print(f"...{len(result)-20}개의 파일이 더 존재합니다.")
            if input("이대로 진행하시겠습니까? (Y/N) > ").lower() == "y":
                return result
            else:
                return set_target_files(folder_path)

def set_output_folder(folder_path):
    print_version_info()
    print(f"기준 폴더 : {os.getcwd()}")
    output_folder = input(f"출력할 폴더를 입력하세요. (입력하지 않으시면 {folder_path}로 가정합니다.)> ")
    if output_folder == "" or output_folder == folder_path:
        return folder_path
    else:
        if os.path.exists(output_folder):
            if input(f"폴더 {output_folder}로 파일을 이동하시겠습니까? (Y/N) > ").lower() == "y":
                return output_folder
            else:
                return set_output_folder(folder_path)
        else:
            if input("해당 폴더는 존재하지 않습니다. 해당 폴더를 생성하고 진행하시겠습니까? (Y/N) > ") == "y":
                os.mkdir(output_folder)
                return output_folder
            else:
                return set_output_folder(folder_path)

def set_output_pattern(result, before_path, after_path):
    print_version_info()
    print("""\
[이름 설정 패턴 문법]
1. 기존 파일 이름에서 찾은 변수를 사용할때는 {변수명}으로 사용합니다.
2. <(파이썬 코드)>는 그 자리에 그 코드의 실행 결과를 넣습니다. 이 코드 안에도 {변수}를 넣을 수 있습니다.
- Counter는 1부터 시작하는 특수한 변수입니다. 변수 Counter는 파일의 순서를 만들 때 사용가능합니다.
""")
    pattern_raw = input("패턴을 입력하세요 > ")
    new_preview = []
    for index, file in enumerate(result):
        new_name = ""
        counter = index+1
        i = 0
        while i < len(pattern_raw):
            if pattern_raw[i] == "{":
                j = i+1
                while pattern_raw[j] != "}":
                    j += 1
                if pattern_raw[i+1:j] not in file[1]:
                    print(f"패턴에 존재하지 않는 변수 {pattern_raw[i+1:j]}가 있습니다.")
                    os.system("pause")
                    return set_output_pattern(result, before_path, after_path)
                new_name += str(file[1][pattern_raw[i+1:j]])
                i = j
            elif pattern_raw[i] == "<":
                j = i+1
                while pattern_raw[j] != ">":
                    j += 1
                code = pattern_raw[i+1:j]
                for i in file[1].keys():
                    code = code.replace("{"+i+"}", str(file[1][i]))
                code = code.replace("{Counter}", str(counter))
                try:
                    code = ast.literal_eval(code)
                except Exception:
                    print(f"파이썬 코드 {code}가 올바르지 않습니다.")
                    os.system("pause")
                    return set_output_pattern(result, before_path, after_path)
                new_name += str(code)
                i = j
            else:
                new_name += pattern_raw[i]
            i += 1
        new_preview.append([file[0], new_name])
    print("파일 이름 변경 미리보기")
    for i in range(0, min(len(new_preview), 20)):
        print(f"{i+1} | {new_preview[i][0]} -> {new_preview[i][1]}")
    if len(new_preview) > 20:
        print(f"...{len(new_preview)-20}개의 파일이 더 존재합니다.")
    if input("이대로 진행하시겠습니까? (Y/N) > ").lower() == "y":
        for file in new_preview:
            os.rename(os.path.join(before_path, file[0]), os.path.join(after_path, file[1]))
        return new_preview
    else:
        return set_output_pattern(result, before_path, after_path)

def main():
    folder_path = set_work_folder()
    target_files = set_target_files(folder_path)
    output_folder = set_output_folder(folder_path)
    data = set_output_pattern(target_files, folder_path, output_folder)
    print_version_info()
    print("지금이 작업을 복구할 수 있는 마지막 기회입니다. 다시 한번 작업이 잘 진행되었는지 확인해주세요.")
    if input("작업을 복구하시겠습니까? (Y/N) > ").lower() == "y":
        try:
            for file in data:
                os.rename(os.path.join(output_folder, file[1]), os.path.join(folder_path, file[0]))
        except Exception:
            print("작업 복구에 실패했습니다.")
            os.system("pause")
        else:
            print("작업이 복구되었습니다.")
    else:
        print("작업이 완료되었습니다.")
    if input("다시 시작하시겠습니까? (Y/N) > ").lower() == "y":
        return 1
    else:
        return 0

if __name__ == "__main__":
    while main() == 1:
        pass
    os.system("pause")
    exit()
    