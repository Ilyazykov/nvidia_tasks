import argparse
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


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--command', type=str, default="run")
    parser.add_argument('--config', type=str, default="/Users/i.zykov/Desktop/servers.cfg")

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    run_command_on_servers(args.command, args.config)


if __name__ == "__main__":
    main()

# servers.cfg:
# ---------------------
# i.zykov@host1.ru
# i.zykov@host2.ru
# i.zykov@host3.ru
