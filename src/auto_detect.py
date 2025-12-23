# START BLOCK 1
from shared_imports import os, glob, Counter

def detect_mode_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        return 'Raw Text Chunks'
    elif ext == '.js':
        return 'JavaScript Code Segments'
    elif ext == '.json':
        return 'JSON Code Segments'
    else:
        return 'Raw Text Chunks'

def detect_mode_from_dir(dir_path, status_callback=None):
    files = glob.glob(os.path.join(dir_path, '*.*'))
    if files:
        exts = [os.path.splitext(f)[1].lower() for f in files]
        ext_counts = Counter(exts)
        common_ext = ext_counts.most_common(1)[0][0] if ext_counts else None
        if common_ext == '.txt':
            mode = 'Raw Text Chunks'
        elif common_ext == '.js':
            mode = 'JavaScript Code Segments'
        elif common_ext == '.json':
            mode = 'JSON Code Segments'
        else:
            mode = 'Raw Text Chunks'
            if status_callback:
                status_callback("Auto-detect: Unknown files, defaulting to Raw Text")
        return mode
    else:
        if status_callback:
            status_callback("Auto-detect: No files found, defaulting to Raw Text")
        return 'Raw Text Chunks'

# END BLOCK 1
