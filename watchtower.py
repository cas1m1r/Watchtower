import json
import time
import sys
import os


def load_watchlist(path: str):
    wlist = os.path.join(path,'watchlist.json')
    if not os.path.isfile(wlist):
        print(f'[X] cannot find watchlist.json at {path}')
        return create_watchlist(wlist)
    else:
        return json.loads(open(wlist,'r').read())


def create_watchlist(path: str):
    adding = True
    watchlist = {}
    while adding:
        fopt = input('Enter Filepath [Enter Exit to quit]:')
        if fopt == 'quit':
            adding = False
        else:
            watchlist[fopt] = check_file_status(fopt)
    print(f'Creating watchlist')
    open(path, 'w').write(json.dumps(watchlist, indent=2))
    return watchlist


def check_file_status(filepath: str):
    file_info = os.stat(filepath.replace('"',''))
    # TODO: fill this in
    return {'last_accessed': file_info.st_atime,
            'last_modified': file_info.st_mtime,
            'last_changed': file_info.st_ctime}


def check_changed(file, watchlist):
    changed = False
    properties_changed = []
    atime = watchlist[file]['last_accessed']
    mtime = watchlist[file]['last_modified']
    ctime = watchlist[file]['last_changed']
    current_info = os.stat(file.replace('"',''))
    if atime != current_info.st_atime:
        changed = True
        properties_changed.append('accessed')
    if mtime != current_info.st_mtime:
        changed = True
        properties_changed.append('modified')
    if ctime != current_info.st_ctime:
        changed = True
        properties_changed.append('changed')
    return changed, properties_changed

def monitor(watchlist, sendAlert):
    monitoring = True
    while monitoring:
        try:
            for file in watchlist.keys():
                different, affected = check_changed(file, watchlist)
                if different:
                    message = f'[!] {file} has been:\n'
                    for prop in affected:
                        message += f'\t-{prop}\n'
                    print(message)
                    # Send Discord Message
                    if sendAlert:
                        print(f'Sending Discord message')
                        # TODO: Implement
                    # update last changed
                    watchlist[file] = check_file_status(file)
        except KeyboardInterrupt:
            print(f'[-] Shutting down watchtower')
            monitoring = False


def main():
    # TODO Check for discord webhook
    sendAlerts = False
    root_path = 'TripWire'
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
    # Load config
    watchlist = load_watchlist(root_path)
    # continuously watch whether any attribute ever changes in watchlist
    monitor(watchlist, sendAlerts)


if __name__ == '__main__':
    main()
