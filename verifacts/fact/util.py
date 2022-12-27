import os
from pathlib import Path

def strip_root(path, root):
    short = path
    if path.startswith(root):
        short = path[len(root):]
    return short

def fact_make_output_path(fact_path, strip_path, output_prefix, output_suffix):
    path = fact_path
    if fact_path.startswith(strip_path):
        path = path[len(strip_path):]
    path = path.lstrip('/')
    path = output_prefix / (path + output_suffix)

    path.parent.mkdir(parents=True, exist_ok=True)

    return path

def facts_relpath(from_path, to_path):
    return os.path.relpath(to_path, from_path)

def sig2path(sig, root):
    path_str = strip_root(sig, root)
    path = path_str.split("#", 1)
    path[1] = path[1].rstrip('#')
    path.append(Path(path[0]) / (path[1] + '.md'))
    return path

def sig_path2path(sig, fpath, root):
    path = [strip_root(fpath, root), sig.strip('#')]
    path.append(Path(path[0]) / (path[1] + '.md'))
    return path
