from os import system

if __name__ == '__main__':
    print("Updating...")
    system("git pull")

    import pkdaemon

    try:
        import daemon
        with daemon.DaemonContext():
            pkdaemon.main()
    except ImportError:
        pkdaemon.main()
