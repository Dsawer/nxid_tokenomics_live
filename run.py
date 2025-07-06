# run.py  –  Streamlit’i başlatan sarıcı
import sys, os
import streamlit.web.cli as stcli

if __name__ == "__main__":
    # exe içindeyken göreceli yolların bozulmaması için
    os.chdir(os.path.dirname(__file__))
    sys.argv = ["streamlit", "run", "main.py", "--global.developmentMode=false"]
    sys.exit(stcli.main())
