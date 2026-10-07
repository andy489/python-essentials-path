import sys
import sysconfig


def build_kind() -> str:
    if sysconfig.get_config_var("Py_GIL_DISABLED"):
        return "free-threaded"
    return "standard"


def narrate(build: str, gil_enabled: bool) -> str:
    if build == "standard":
        return "the GIL is compiled in; switching builds is the only way off"
    if gil_enabled:
        return "the GIL was forced back on for this run"
    return "threads can run CPU-bound code in parallel"


def main() -> None:
    build = build_kind()
    gil_enabled = sys._is_gil_enabled()
    print(f"python {sys.version.split()[0]} at {sys.executable}")
    print(f"build={build} gil_enabled={gil_enabled} -> {narrate(build, gil_enabled)}")


if __name__ == "__main__":
    main()
