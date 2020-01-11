import ast
import re
import shutil
import sys
import urllib.parse
import urllib.request
from pathlib import Path


def download_build(branch_url: str, build: str, reg_exr: re, directory: Path):
    build_url = branch_url + build + "/"
    build_api_url = build_url + "api/python"
    artifacts = ast.literal_eval(urllib.request.urlopen(build_api_url).read().decode("utf-8"))["artifacts"]
    artifacts = filter(lambda it: reg_exr.match(it["fileName"]), artifacts)
    if not artifacts:
        print("No artifact matched in build " + build)
        return
    print("Task for build %s start" % build)
    directory.mkdir(parents=True, exist_ok=True)
    try:
        for artifact in artifacts:
            artifact_url = build_url + "artifact/" + artifact["relativePath"]
            file_name = artifact["fileName"]
            file_path = directory / file_name
            print("Downloading " + artifact_url)
            urllib.request.urlretrieve(artifact_url, str(file_path))
    except BaseException:
        shutil.rmtree(directory)
        raise
    print("Finish task for build " + build)


def main():
    if len(sys.argv) != 4:
        sys.exit("Usage:\npython downloader.py {branchUrl} {matchExr} {outputDir}")
    # parse args
    input_branch_url, input_match_exr, output_dir = sys.argv[1:]
    # parse url
    parsed_input_branch_url = urllib.parse.urlparse(input_branch_url)
    if not parsed_input_branch_url.scheme or not parsed_input_branch_url.netloc or not parsed_input_branch_url.path:
        raise Exception("Invalid url")
    if not parsed_input_branch_url.path.endswith("/"):
        # noinspection PyProtectedMember
        parsed_input_branch_url = parsed_input_branch_url._replace(path=parsed_input_branch_url.path + "/")
    branch_url = urllib.parse.urlunparse(parsed_input_branch_url)
    # parse regExr
    reg_exr = re.compile(input_match_exr)
    # ensure outputDir exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # fetch builds list
    branch_api_url = branch_url + "api/python"
    builds = ast.literal_eval(urllib.request.urlopen(branch_api_url).read().decode("utf-8"))["builds"]
    builds = map(lambda it: str(it["number"]), builds)
    non_exist_builds = filter(lambda it: not (output_path / it).exists(), builds)
    non_exist_builds = list(non_exist_builds)  # for multi times iterate
    if not non_exist_builds:
        sys.exit("Everything up-to-date")
    print("Missing builds: " + ", ".join(str(it) for it in non_exist_builds))

    # download builds
    for build in non_exist_builds:
        download_build(branch_url, build, reg_exr, output_path / build)


if __name__ == '__main__':
    main()
