import subprocess


def getServers(config):
    with open(config) as f:
        lines = f.read().splitlines()
    return lines


def runCommandOnServers(command, config):
    hosts = getServers(config)

    processes = []
    i = 3
    for host in hosts:
        ssh_command = f"ssh {host} {command}"
        
        p = subprocess.Popen(ssh_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        processes.append(p)

        p.wait()

    for p in processes:
        out, _ = p.communicate()
        print(out)


runCommandOnServers("run", "/Users/i.zykov/Desktop/servers.cfg")

# servers.cfg:
# ---------------------
# i.zykov@host1.ru
# i.zykov@host2.ru
# i.zykov@host3.ru