# START BLOCK 1
from shared_imports import os, glob, Counter

def detect_mode_from_file(file_path, status_callback=None):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        mode = 'Raw Text Chunks'
    elif ext == '.js':
        mode = 'JavaScript Code Segments'
    elif ext == '.json':
        mode = 'JSON Code Segments'
    else:
        mode = 'Raw Text Chunks'
        if status_callback:
            status_callback("Auto-detected mode: " + mode + " (unknown extension)")
        return mode
    if status_callback:
        status_callback("Auto-detected mode: " + mode)
    return mode

def detect_mode_from_dir(dir_path, status_callback=None):
    files = glob.glob(os.path.join(dir_path, '*.*'))
    if files:
        exts = [os.path.splitext(f)[1].lower() for f in files]
        relevant_exts = {'.txt': 'Raw Text Chunks', '.js': 'JavaScript Code Segments', '.json': 'JSON Code Segments'}
        ext_counts = Counter(e for e in exts if e in relevant_exts)
        if not ext_counts:
            mode = 'Raw Text Chunks'
            if status_callback:
                status_callback("Auto-detected mode: " + mode + " (no relevant files found)")
            return mode
        common_ext = ext_counts.most_common(1)[0][0]
        mode = relevant_exts[common_ext]
        if status_callback:
            status_callback("Auto-detected mode: " + mode)
        return mode
    else:
        mode = 'Raw Text Chunks'
        if status_callback:
            status_callback("Auto-detected mode: " + mode + " (no files found)")
        return mode

# END BLOCK 1
