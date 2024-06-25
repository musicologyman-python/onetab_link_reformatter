from collections.abc import Iterable
from functools import partial
import io
import operator
from typing import Callable

import pyperclip
from toolz import curried
from toolz.functoolz import (compose_left, 
                             curry, 
                             pipe)

def clean_url_tuple(url_tuple: [str, str]) -> [str, str]:
    description, url = url_tuple
    return (description.strip(), url.strip())

parse_urls: Callable[[str], Iterable[[str, str]]] = \
        compose_left(
            operator.methodcaller('splitlines'), 
            curried.map(operator.methodcaller('split', '|', maxsplit=1)), 
            curried.map(tuple),
            curried.map(clean_url_tuple))

def main():
    urls = pipe(pyperclip.paste(), 
                parse_urls)

    with io.StringIO() as sp:
        prints = partial(print, file=sp)
        for url, description in urls:
            prints(f'[{description}]({url})')
        results = sp.getvalue()

        print("The following text will be copied to the clipboard:")
        print(results)
        pyperclip.copy(results)
    
if __name__ == '__main__':
    main()
