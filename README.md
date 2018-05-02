# Naive-Quasigroup-Pseudo-Random-Generator
A naive quasigroup pseudo random generator based on "A Quasigroup Based Random Number Generator for Resource Constrained Environments" paper


## Usage

`PRNGQG` is a python class, to use just simply import.
Usage example shown below :

```
  import PRNGQG

  N = 256 # Number order
  s1 = 130 # First Seed
  s2 = 250 # Second Seed
  iteration_limit = 100 # Iteration Limit
  random_number = PRNGQG(N).Generate(s1, s2, iteration_limit)
```
