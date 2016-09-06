#!/bin/bash
./fittails_mc.py tails tritrig_pass6_vertcuts.root acceptance/acceptance_data.root
./fittails_mc.py tails_mres tritrig_pass6_vertcuts.root acceptance/acceptance_data.root -m
./fittails_mc.py tails_postfix tritrig_postfix_vertcuts.root acceptance/acceptance_data.root
./fittails_mc.py tails_postfix_mres tritrig_postfix_vertcuts.root acceptance/acceptance_data.root -m
