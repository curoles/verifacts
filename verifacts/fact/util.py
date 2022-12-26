
def fact_make_output_path(fact_path, strip_path, output_prefix, output_suffix):
    path = fact_path
    if fact_path.startswith(strip_path):
        path = path[len(strip_path):]
    path = path.lstrip('/')
    path = output_prefix / (path + output_suffix)

    path.parent.mkdir(parents=True, exist_ok=True)

    return path
