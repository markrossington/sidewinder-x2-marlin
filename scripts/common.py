import sys
import os


class Common:
    @staticmethod
    def work_top_level():
        repository_root = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
        print(f"[Info] Setting working directory to {repository_root}")
        os.chdir(repository_root)
