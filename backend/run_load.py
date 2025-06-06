"""Command-line script for loading channel data from JSON file or PDB database."""

from app.channels.data import load
import argparse


def non_negative_int(value: int) -> int:
    """Returns non negative value, if possible.

    Args:
        value: argument to check
    Returns:
        unchanged argument
    """
    value = int(value)
    if value < 0:
        raise argparse.ArgumentTypeError("Negative values are not allowed.")
    return value


def usage_msg():
    """Returns usage message for the script used by argparse."""
    return "run_load.py [-h] (-f FILE | [-s START] [-p {remote,mirror}])"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the load function with a start value", usage=usage_msg()
    )

    file_group = parser.add_argument_group("File input options")
    pdb_group = parser.add_argument_group("PDB fetch options")

    pdb_group.add_argument(
        "-s",
        "--start",
        required=False,
        default=None,
        type=non_negative_int,
        help="Starting ID",
    )

    pdb_group.add_argument(
        "-p",
        "--pdb",
        choices=["remote", "mirror"],
        help="Fetch file entries from remote or mirror of PDB database.",
    )

    file_group.add_argument(
        "-f", "--file", help="Loads channels from JSON file passed as a path."
    )

    parser.add_argument(
        "-e",
        "--skip_existing",
        action="store_true",
        default=False,
        help="Should loading script ignore existing structures or add channels to them too.",
    )

    args = parser.parse_args()

    if all(x is None for x in [args.file, args.pdb, args.start]):
        parser.error("Set source databse or source file to start data loader.")

    if args.file and (args.pdb or args.start):
        parser.error("Can not combine file path argument with fetch related arguments.")

    if args.file:
        load.load_from_file(args.file, skip_existing=args.skip_existing)
    else:
        load.load_from_pdb(
            start=args.start, fetch_source=args.pdb, skip_existing=args.skip_existing
        )
