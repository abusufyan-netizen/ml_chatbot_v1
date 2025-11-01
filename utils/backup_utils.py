import os, json

def backup_all_to_drive(local_dir, drive_auth):
    # Collect list of files to backup
    to_backup = []
    for root, _, files in os.walk(local_dir):
        for f in files:
            if f.endswith('.h5') or f.endswith('.json') or f.endswith('.csv') or f.endswith('.txt') or f.endswith('.png'):
                to_backup.append(os.path.join(root, f))
    # Attempt upload
    if not drive_auth or not drive_auth.is_authenticated():
        return False, 'Drive not authenticated'
    for f in to_backup:
        ok, msg = drive_auth.upload_file(f)
        if not ok:
            return False, msg
    return True, 'All uploaded (simulated)'
