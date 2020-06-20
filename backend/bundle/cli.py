#!/usr/bin/env python
import click
from .cli_helper import *


@click.group()
def main():
    """
    The main function of the CLI
    @return: None
    """
    pass


if __name__ == '__main__':
    main()
