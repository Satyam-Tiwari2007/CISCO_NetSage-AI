# NetSage AI — Rule Checker

The rule checker is deterministic and independent of the AI model.

## Checks implemented
1. Duplicate IPv4 addresses
2. Subnet mask / expected-network mismatch
3. Default gateway mismatch
4. Interface operational status
5. VLAN existence
6. Route existence

## Design principle
The checker does not decide the final diagnosis. It produces objective evidence
that can support or challenge an AI diagnosis. A human reviewer remains the
final decision-maker.

## Demonstration
Run:

    python rule_checker.py

The reproducible demonstration intentionally contains errors so that the
checker produces warnings/errors that can later be shown in the project demo.
