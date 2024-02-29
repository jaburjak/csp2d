from pathlib import Path
import argparse
import asyncio
import contextlib
import logging.config
import sys
import typing

from hat import aio
from hat import json

from opcut import common
import opcut.calculate


params_schema_id: str = 'opcut://opcut.yaml#/definitions/params'
result_schema_id: str = 'opcut://opcut.yaml#/definitions/result'


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='cutting stock problem optimizer',
        epilog='For more options, run "%(prog)s <action> --help"')
    subparsers = parser.add_subparsers(dest='action',
                                       required=True)

    def enum_values(enum_cls):
        return ', '.join(str(i.value) for i in enum_cls)

    calculate = subparsers.add_parser(
        'calculate',
        help='Outputs the optimal stock cuts as a text file.')
    calculate.add_argument(
        '--method', metavar='METHOD', type=common.Method,
        default=common.Method.FORWARD_GREEDY_NATIVE,
        help=f"calculate method ({enum_values(common.Method)})")
    calculate.add_argument(
        '--input-format', metavar='FORMAT', type=json.Format, default=None,
        help=f"input params format ({enum_values(json.Format)})")
    calculate.add_argument(
        '--output-format', metavar='FORMAT', type=json.Format, default=None,
        help=f"output result format ({enum_values(json.Format)})")
    calculate.add_argument(
        '--output', metavar='PATH', type=Path, default=Path('-'),
        help=f"output result file path or - for stdout ({result_schema_id})")
    calculate.add_argument(
        'params', type=Path, default=Path('-'), nargs='?',
        help=f"input params file path or - for stdin ({params_schema_id})")

    return parser


def main():
    parser = create_argument_parser()
    args = parser.parse_args()

    if args.action == 'calculate':
        calculate(method=args.method,
                  input_format=args.input_format,
                  output_format=args.output_format,
                  result_path=args.output,
                  params_path=args.params)

    else:
        raise ValueError('unsupported action')


def calculate(method: common.Method,
              input_format: typing.Optional[json.Format],
              output_format: typing.Optional[json.Format],
              result_path: Path,
              params_path: Path):
    if input_format is None and params_path == Path('-'):
        input_format = json.Format.JSON

    if output_format is None and result_path == Path('-'):
        output_format = json.Format.JSON

    params_json = (json.decode_stream(sys.stdin, input_format)
                   if params_path == Path('-')
                   else json.decode_file(params_path, input_format))

    common.json_schema_repo.validate(params_schema_id, params_json)
    params = common.params_from_json(params_json)

    try:
        result = opcut.calculate.calculate(method=method,
                                           params=params)

    except common.UnresolvableError:
        sys.exit(42)

    result_json = common.result_to_json(result)

    if result_path == Path('-'):
        json.encode_stream(result_json, sys.stdout, output_format)
    else:
        json.encode_file(result_json, result_path, output_format)


if __name__ == '__main__':
    sys.argv[0] = 'opcut'
    sys.exit(main())
