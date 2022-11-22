import subprocess


def get_servers(config):
    with open(config) as f:
        lines = f.read().splitlines()
    return lines


def run_command_on_servers(command, config):
    hosts = get_servers(config)

    processes = []
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


def main():
    run_command_on_servers("run", "/Users/i.zykov/Desktop/servers.cfg")


if __name__ == "__main__":
    main()

# servers.cfg:
# ---------------------
# i.zykov@host1.ru
# i.zykov@host2.ru
# i.zykov@host3.ru
