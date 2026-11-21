import sys
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from .data import ROOT,prepare

def main():
    if hasattr(sys.stdout,"reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    prepare()
    notebook=nbformat.read(ROOT/"notebooks/02_analysis.ipynb",as_version=4)
    ExecutePreprocessor(timeout=180,kernel_name="python3").preprocess(
        notebook,{"metadata":{"path":str(ROOT)}})
    out=ROOT/"notebooks/executed"
    out.mkdir(parents=True,exist_ok=True)
    nbformat.write(notebook,out/"02_analysis.ipynb")
    print("Notebook hoàn tất")

if __name__=="__main__":
    main()


