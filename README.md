Advent of Code solutions
==

I've been doing Advent of Code in Rust for a few seasons over at [advent-of-code-rs](https://github.com/kaaveland/advent-of-code-rs),
but my son has started school this year, and I'm finding less time than before to finish the puzzles early in the day. Since
I've been programming Python for much longer than I've programmed Rust, I've decided to do branch out and do some Python 
now, to improve my times a little.

Setup
--

I use [uv](https://docs.astral.sh/uv/) to run things in this repository, and I do not `pip install`.

- To set up the virtualenv: `uv sync`
- To run tests: `uv run pytest`
- To run the puzzle for a day: `uv run ./aoc.py run 2024 4 # sorry about the run run thing`
- To add a dependency: `uv add requests`
- To format the code: `uvx ruff format .`

The `aoc.py`-utility will ask you for an advent of code session cookie and store it in `~/.aoc_cookie`. The
input files end up in `data/` in the repository root, and they are in `.gitignore`.
