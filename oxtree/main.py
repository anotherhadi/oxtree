####################################################################
#           ______________________________________
#  ________|                0xTree                |_______
#  \       |                                      |      /
#   \      |              @0x68616469             |     /
#   /      |______________________________________|     \
#  /__________)                                (_________\
#
# A Handy Script to view Directory Tree Structure
#
# Github repo : https://github.com/0x68616469/oxtree
#
####################################################################

from oxflags import Flag
import os
import sys

def explore_dir(path="/", dot_file=False, tree=['├───'], last=False, limit_depth=100, current_depth=0):
    if current_depth >= limit_depth:
        return
    
    try:
        dir_list = os.scandir(path)
        if dot_file == True: length = len(os.listdir(path))
        else: length = len([x for x in os.listdir(path) if not x.startswith('.')])        
    except PermissionError:
        print(f"\033[90m[\033[91mx\033[90m] \033[0m Permission Error.")
        return

    j=0
    left = "├───"
    end = "└───"
    space = "│   "
    blank = "    "

    for dir in dir_list:
        if (dir.name.startswith(".") and dot_file == False): continue
        j += 1

        if last == True:    
            temp = tree[len(tree)-2]
            tree[len(tree)-2] = blank
            
        print("\033[90m", end="")
        for i in range(len(tree)):
            if i != len(tree)-1 and tree[i] == left: print(space, end="")
            elif i == len(tree)-1 and length == j: print(end, end="")
            else: print(tree[i], end="")
  
        print("\033[0m", end="")
        if dir.is_dir(): 
            global nb_folder
            nb_folder += 1
            print(f"\033[1m\033[94m {dir.name}\033[0m")
        else: 
            global nb_file
            nb_file += 1
            print(f" {dir.name}\033[0m")
        
        try:
            if dir.is_dir():
                tree.append(left)
                if length == j: explore_dir(path=f"{path}/{dir.name}", dot_file=dot_file, tree=tree, last=True, limit_depth=limit_depth, current_depth=current_depth+1)
                else: explore_dir(path=f"{path}/{dir.name}", dot_file=dot_file, tree=tree, last=False, limit_depth=limit_depth, current_depth=current_depth+1)
                tree.pop(-1)
        except PermissionError:
            print(f"\033[90m[\033[91mx\033[90m] \033[0m Permission Error.")
            return
            
        if last == True: tree[len(tree)-2] = temp

def main():
    flag = Flag(description="A Handy Script to view Directory Tree Structure")

    flag.new(short="-p", full="--path", type="string", default=".", help="Choose the path")
    flag.new(short="-.", full="--dotfiles", type="bool", default=False, help="Show dotfiles")
    flag.new(short="-d", full="--depth", type="int", default=100, help="Limit depth of tree")

    flag.parse()

    path = flag.path
    if path.endswith("/") and path != "/":
        path = path[:-1]
    dot_file = flag.dotfiles
    depth = flag.depth

    global nb_folder
    global nb_file
    nb_folder = 0
    nb_file = 0
    folder = path.split('/')
    print(f"\033[3;1m\033[94m{folder[len(folder)-1]}\033[0m")

    explore_dir(path, dot_file, limit_depth=depth)

    print(f"\n\033[90m({nb_folder} directories, {nb_file} files)\033[0m")

if __name__ == '__main__':
    main()