#!/usr/bin/env sh
if which poetry ; then
	echo "poetry ok"
else
	python3 -m pip install poetry
fi

