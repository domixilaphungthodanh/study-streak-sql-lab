"""Portable stdlib bootstrap; launch modules directly, never Jupyter .exe wrappers."""
import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import venv

ROOT=Path(__file__).resolve().parent

def environment_directory(root=ROOT):
    # Jedi/Jupyter include deeply nested files; avoid Windows MAX_PATH failures.
    if sys.platform=='win32':
        cache=Path(os.environ.get('LOCALAPPDATA',str(Path.home()/'AppData/Local')))/'StudyStreakSqlLab/venvs'
        key=hashlib.sha256(str(root.resolve()).casefold().encode('utf-8')).hexdigest()[:12]
        return cache/key
    return root/'.venv'

ENV=environment_directory()

for stream in (sys.stdout,sys.stderr):
    if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')

def environment_python():return ENV/('Scripts/python.exe' if sys.platform=='win32' else 'bin/python')

def run(command):
    env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PIP_PROGRESS_BAR='off')
    subprocess.run([str(value) for value in command],cwd=ROOT,env=env,check=True)

def digest(notebook):
    requirements=ROOT/'requirements.txt'
    return hashlib.sha256(requirements.read_bytes()+str(sys.version_info[:2]).encode()).hexdigest()

def prepare_environment(notebook=False):
    if sys.version_info[:2] != (3,12):
        raise RuntimeError("Cần Python 3.12")
    python=environment_python()
    if not python.is_file():
        print('Dang tao moi truong Python rieng:',ENV,flush=True)
        venv.EnvBuilder(with_pip=True).create(ENV)
    marker=ENV/('lab_notebook.sha256' if notebook else 'lab_app.sha256')
    ready=marker.is_file() and marker.read_text().strip()==digest(notebook)
    imports='import pandas,matplotlib'+(',notebook,nbconvert,ipykernel' if notebook else '')
    if ready:ready=subprocess.run([str(python),'-c',imports],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
    if not ready:
        print('Lan dau can Internet cai thu vien; khong can Git hoac Administrator.',flush=True)
        run([python,'-m','pip','install','-r',ROOT/'requirements.txt'])
        marker.write_text(digest(notebook)+'\n')
        if notebook:(ENV/'lab_app.sha256').write_text(digest(False)+'\n')
    return python

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--notebook",action="store_true")
    parser.add_argument("--setup-only",action="store_true")
    args=parser.parse_args(argv)
    python=prepare_environment(args.notebook)
    run([python,"-c","from streak_lab.data import prepare; prepare()"])
    if not args.setup_only:
        if args.notebook:
            run([python,"-m","notebook","--notebook-dir",ROOT,ROOT/"notebooks/02_analysis.ipynb"])
        else:
            run([python,"-c","from streak_lab.analysis import export; export(); print('outputs')"])
    return 0

if __name__=="__main__":
    raise SystemExit(main())

