#!/usr/bin/env python

import pathlib
import importlib
import time
from concurrent.futures import ProcessPoolExecutor

import attr
import typer
import requests

COOKIE_PATH = pathlib.Path.home() / ".aoc_cookie"
UAGENT_PATH = pathlib.Path.home() / ".aoc_uagent"
HERE = pathlib.Path(__file__).parent
cli = typer.Typer(no_args_is_help=True)


def get_cookie() -> str:
    try:
        with open(COOKIE_PATH) as inf:
            return inf.read().strip()
    except IOError:
        cookie = input("Enter your advent of code session cookie").strip()
        if len(cookie) < 100:
            raise ValueError("Not a valid session cookie, it's over 100 bytes")
        with open(COOKIE_PATH, "w") as out:
            out.write(cookie)
        return cookie


def get_user_agent() -> str:
    try:
        with open(UAGENT_PATH) as inf:
            return inf.read().strip()
    except IOError:
        uagent = input("Enter an email account that can be used to contact you").strip()
        with open(UAGENT_PATH, "w") as out:
            out.write(uagent)
        return uagent


def get_client() -> requests.Session:
    session = requests.Session()
    cookie = get_cookie()
    session.headers.update(
        {"Cookie": f"session={cookie}", "User-Agent": get_user_agent()}
    )
    return session


def download_day(client: requests.Session, year: int, day: int) -> str:
    response = client.get(f"https://adventofcode.com/{year}/day/{day}/input")
    response.raise_for_status()
    return response.text.strip()


def data_path(year: int, day: int) -> pathlib.Path:
    return HERE / "data" / str(year) / f"{day:02d}" / "input"


@cli.command("dl-data")
def get_data(year: int, day: int) -> str:
    path = data_path(year, day)
    try:
        with open(path) as inf:
            return inf.read().strip()
    except IOError:
        with get_client() as client:
            data = download_day(client, year, day)
        path.parent.mkdir(exist_ok=True, parents=True)
        with open(path, "w") as out:
            out.write(data)
        return data


@attr.s
class Result:
    output: str = attr.ib()
    duration: float = attr.ib()


class NotImplementModule:
    @staticmethod
    def main(_inp: str) -> str:
        return "Not implemented yet"


def run_one(year: int, day: int) -> Result:
    data = get_data(year, day)
    try:
        mod = importlib.import_module(f"y{year}.day_{day:02d}")
    except ImportError:
        mod = NotImplementModule
    start = time.time()
    result = mod.main(data)
    duration = 1000 * (time.time() - start)
    return Result(result, duration)


@cli.command("run")
def run(year: int, day: int):
    result = run_one(year, day)
    print(f"{year}-{day:02d} result in {result.duration:.3f}ms:\n{result.output}")


def _run(yearday: (int, int)):
    year, day = yearday
    return year, day, run_one(year, day)


@cli.command("runall")
def run(year: int):
    start = time.time()

    with ProcessPoolExecutor() as pool:
        results = pool.map(_run, [(year, day) for day in range(1, 26)])
    total = 1000 * (time.time() - start)
    for year, day, result in results:
        print(f"{year}-{day:02d} result in {result.duration:.3f}ms:\n{result.output}")
    print(f"Total duration: {total:.3f}ms")


if __name__ == "__main__":
    cli()
