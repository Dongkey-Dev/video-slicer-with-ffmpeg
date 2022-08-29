import os
import platform
from pathlib import Path

from simple_term_menu import TerminalMenu

Windows = "Windows"
macOS = "macOS"
MV_BACK = f"--Move Back Dir..--"


def get_desktop_path():
    os_platform = platform.platform().split('-')[0]
    if os_platform == Windows:
        DESKTOP_PATH = os.path.join(os.environ["HOMEPATH"], "Desktop")
    elif os_platform == macOS:
        DESKTOP_PATH = f"/users/{os.getlogin()}/Desktop"
    return DESKTOP_PATH


def is_vid(path):
    if ".mp4" in path:
        return True
    return False


def move_dir(cur, selected):
    if selected == MV_BACK:
        return Path(cur).parent
    else:
        return os.path.join(cur, selected)


def execute_edit(cur, selected):
    start = input(f"Enter video start time seocnd want to slice.\n")
    during = input(f"Enter the duration of the video second.\n")
    output = input(f"Enter output video name. (exclude file format. ex .mp4)\n")
    output += '.' + selected.split('.')[-1]
    output = os.path.join(cur, output)
    edit_vid_name = os.path.join(cur, selected)
    os.system(f"ffmpeg -ss {start} -t {during} -i '{edit_vid_name}' '{output}'")
    

def main():
    cur = get_desktop_path()
    while True:
        dirlist = [filename for filename in os.listdir(cur) if os.path.isdir(os.path.join(cur, filename))]
        vidlist = [el for el in os.listdir(cur) if ".mp4" in el]
        terminal_menu_show = ["Directory : " + el for el in dirlist]
        terminal_menu = dirlist.copy()
        terminal_menu_show.extend(["Video : " + el for el in vidlist])
        terminal_menu.extend(vidlist)
        terminal_menu_show.append(MV_BACK)
        terminal_menu.append(MV_BACK)
        idx = TerminalMenu(terminal_menu_show, title= "Select Directory or Video.").show()
        selected_path = os.path.join(cur, terminal_menu[idx])
        if is_vid(selected_path):
            execute_edit(cur, selected_path)
        else:
            cur = move_dir(cur, terminal_menu[idx])
    

if __name__=="__main__":
    main()        
