from nspctl.lib.output import turquoise, green, yellow


def nspctl_help():
    print(yellow("nspctl:") + " management tool for systemd-nspawn containers")
    print(yellow("Usage:"))
    print(
        "   "
        + turquoise("nspctl")
        + " [ "
        + green("arguments")
        + " ] [ "
        + green("options")
        + " ] [ "
        + turquoise("container name")
        + " | "
        + turquoise("URL")
        + " | "
        + turquoise("distribution")
        + " ] [ ... ]"
    )
    print(
        "   "
        + turquoise("nspctl")
        + " [ "
        + green("info")
        + " ] [ "
        + turquoise("container name")
        + " ] "
    )
    print(
        "   "
        + turquoise("nspctl")
        + " [ "
        + green("list")
        + " ] [ "
        + green("--all")
        + " | "
        + green("--running")
        + " | "
        + green("--stopped")
        + " ] "
    )
    print(
        "   "
        + turquoise("nspctl")
        + " [ "
        + green("start")
        + " | "
        + green("stop")
        + " | "
        + green("reboot")
        + " ] [ "
        + turquoise("container name")
        + " ] "
    )
    print(
        "   "
        + turquoise("nspctl")
        + " [ "
        + green("enable")
        + " | "
        + green("disable")
        + " ] [ "
        + turquoise("container name")
        + " ] "
    )
    print(
        "   "
        + turquoise("nspctl")
        + " [ "
        + green("shell")
        + " ] [ "
        + turquoise("container name")
        + " ] "
    )
    print(
        "   "
        + turquoise("nspctl")
        + " [ "
        + green("remove")
        + " ] [ "
        + turquoise("container name")
        + " ] "
    )
    print(
        "   "
        + turquoise("nspctl")
        + " [ "
        + green("copy-to")
        + " ] [ "
        + turquoise("container name")
        + " ] [ "
        + green("Host Path")
        + " ] [ "
        + green("Container Path")
        + " ] "
    )
    print(yellow("Container Operations:"))
    print(
        "   "
        + turquoise("nspctl")
        + " [ "
        + green("pull-raw")
        + " | "
        + green("pull-tar")
        + " | "
        + green("pull-docker")
        + " ] [ "
        + turquoise("URL")
        + " ] [ "
        + turquoise("container name")
        + " ] "
    )
    print(
        "   "
        + turquoise("nspctl")
        + " [ "
        + green("bootstrap")
        + " ] [ "
        + turquoise("debian")
        + " | "
        + turquoise("ubuntu")
        + " | "
        + turquoise("arch")
        + " ] [ "
        + turquoise("--version")
        + " ] [ "
        + green("container name")
        + " ] "
    )
    print()
    print("   For more help: https://github.com/mofm/nspctl")