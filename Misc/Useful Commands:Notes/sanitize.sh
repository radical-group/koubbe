#!/bin/sh

IFS=$(echo -en "\n\b")

mode=""
mode="echo"


handle_dir(){

    local d="$1"

    if test -d "$d/bin/"
    then
        # remove conda tree
        if test -f "$d/pyvenv.cfg" -a -f "$d/bin/activate"
        then
            echo "remove venv       $d"
            rm -rf "$d"
            return
        fi

        # remove virtualenv?
        if test -d "$d/conda-meta" -a -f "$d/bin/conda"
        then
            echo "remove conda      $d"
            rm -rf "$d"
            return
        fi
    fi

    # remove executable bits for all files in the directory
    find "$d" -maxdepth 0 -type f | xargs -r -n 1 -I'{}' chmod a-x '{}'

    # iterate all other directories
    iterate_dir "$d"
}


handle_bin(){
    # remove all executable binaries
    local f="$1"
    test -x && echo "remove binary exe $f" && rm -f "$f"
    test -x || echo "ignore binary     $f"
}

handle_other(){
    local f="$1"
    test -x || echo "ignore other      $f"
}


iterate_dir(){

    # iterate over dir content, handle each entry based on type

    local d="$1"
    local f
    local t

    echo "iterate dir       $d"

    for f in "$d"/* "$d"/.[^.]*
    do
        # safeguard against failed glob expansion
        if test "$f" = "$d"'/*'     ; then continue; fi
        if test "$f" = "$d"'/.[^.]*'; then continue; fi

        # get file's mime type
        t=$(file -ib "$f" | cut -f 1 -d ';')

        case "$t" in
            application/x-sharedlib)
                handle_bin "$f"
                ;;
            inode/directory)
                handle_dir "$f"
                ;;
            *)
                handle_other "$f"
                ;;
        esac
    done
}

# target dir to handle
d="$1"

# remove sticky bits globally
chmod -R a-st "$d"

# handle specified target tree
iterate_dir "$d"

