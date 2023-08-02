# MLTL2LTLf

A simple Python script to convert from [Mission-Time Linear Temporal Logic](https://link.springer.com/chapter/10.1007/978-3-030-25543-5_1) (MLTL) to [Linear Temporal Logic on Finite Traces](https://dl.acm.org/doi/10.5555/2540128.2540252) (LTLf), based on the Lark parser.
For the LTLf part, it follows the grammar specified by [Marco Favorito](https://github.com/marcofavorito/tl-grammars/blob/main/content/04.ltlf.md).
For MLTL formulae, additionally bounded operators are allowed:
- `a U_[a,b] b`
- `G_[a,b] a`
- `F_[a,b] a`
- `a U_<=a b`
- `G_<=a a`
- `F_<=a a`

## Installation

After cloning this repository, install it via calling `pip install .` from this directory.

## Usage

After installation, the `mltl2ltlf` binary will be available from the command line.
It takes exactly one input string, for example:

`mltl2ltlf "G_<=2 a"`

and computes the LTLf formula for the given MLTL formula:

`(a&(X[!](a&(X[!]a))))`.

## Tests

You can execute the tests by `python -m unittest test.test_mltl2ltlf`.
The unittests in `test/test_mltl2ltlf.py` also contains some example formulae.

## Limitations

Currently, large bounds lead to degradation in performance.
This is due to Lark's reconstruct method, which performs quite inefficiently.
