import sys

# Pour importer ton code dans src/
sys.path.append("src")

from energydoc_talk_ai.ui.streamlit.app import main

if __name__ == "__main__":
    main()