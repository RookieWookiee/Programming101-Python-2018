import os
import sys


def du(path):
    size = os.path.getsize(path)

    for root, files, dirs in os.walk(path):
        for d in dirs:
            size += os.path.getsize(root + '/' + d)
        for f in files:
            size += os.path.getsize(root + '/' + f)

    return size

def main():
    size = du(sys.argv[1])

    count = 0
    suffixes = ['', 'K', 'M', 'G']
    while size > 1000:
        size /= 1000
        count += 1 

    size = '{0:.1f} {1}'.format(size, suffixes[count])
    print('{0} size is: {1}'.format(sys.argv[1], size))

if __name__ == '__main__':
    main()
