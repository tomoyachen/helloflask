def sayhello(to=None):
    if to:
        return 'Hello, %s!' % to
    return 'Hello!'

if __name__ == '__main__':
    print(sayhello("debug"))