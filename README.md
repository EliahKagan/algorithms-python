<!-- SPDX-License-Identifier: 0BSD -->

# algorithms-python (algorithms-suggestions)

This is one of three partial implementations of the
[**algorithms-suggestions**](https://github.com/EliahKagan/algorithms-suggestions)
exercises. The others are [**Pool**](https://github.com/EliahKagan/Pool) and
[**Search**](https://github.com/EliahKagan/Search).

This was an experiment in doing some of those exercise ideas in Python (even
though they were brainstormed with C++ in mind).

*If you found this by searching, you might be looking for
[**palgoviz**](https://github.com/EliahKagan/palgoviz) instead.*

## License

[0BSD](https://spdx.org/licenses/0BSD.html). See [**`LICENSE`**](LICENSE).

## Getting started

These steps, which assume you have a working `pipenv` command, create or update
the virtual environment and run the tests:

```sh
pipenv install -d
pipenv run pytest --doctest-modules
```

## Suggested usage

You might:

- Look at the implementations in detail to see how they work, ***or***

- Don't look at them (at least not in detail), remove function and class bodies
  (except docstrings), and rework them as problems/exercises. (Then, once tests
  are passing, run `git diff` to compare your solutions with the originals.)

## Future directions

Development is not continuing on this project much, but it's possible some
parts of it, especially the material in `sll.py`, might make its way into
[palgoviz](https://github.com/EliahKagan/palgoviz).
