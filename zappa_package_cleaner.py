import os
from re import fullmatch
from shutil import unpack_archive
from subprocess import DEVNULL, call
from tempfile import TemporaryDirectory


def main(zappa):
    stage_settings = zappa.zappa_settings.get(zappa.api_stage, {})
    regex_excludes = stage_settings.get("regex_excludes", None)
    if not regex_excludes:
        raise Exception(f"No regex_excludes provided for stage: {zappa.api_stage}")

    full_zip_path = os.path.join(os.getcwd(), zappa.zip_path)
    temp_path = TemporaryDirectory().name
    unpack_archive(full_zip_path, temp_path)
    for root, _dirs, files in os.walk(temp_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            filepath_strip = filepath[len(temp_path) :]
            for exclude_regex in regex_excludes:
                if fullmatch(exclude_regex, filepath_strip) is not None:
                    try:
                        os.remove(filepath)
                    except FileNotFoundError:
                        pass

    os.remove(full_zip_path)
    call(f"zip -9 -r {full_zip_path} *", cwd=temp_path, shell=True, stdout=DEVNULL)
