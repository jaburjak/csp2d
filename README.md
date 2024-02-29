# Two-Dimensional Cutting Stock Problem

The Two-Dimensional Cutting Stock Problem (2D CSP) deals with planning the cutting of rectangular pieces from given panels.

## Quick start

Clone this project, install required packages and compile the native implementation:

```sh
$ git clone git@github.com:jaburjak/csp2d.git
$ cd csp2d/
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
(env) $ doit
```

## Usage

To solve your Two-Dimensional Cutting Stock Problem, run the `opcut` module:

```sh
(env) $ cd src_py/
(env) $ python -m opcut calculate --input-format yaml --output result.json << EOF
cut_width: 1
min_initial_usage: false
panels:
    panel1:
        width: 100
        height: 100
items:
    item1:
        width: 10
        height: 10
        can_rotate: false
EOF
```

Output:

```jsonc
{
    "params": {
        "cut_width": 1,
        "min_initial_usage": false,
        "panels": {
            "panel1": {
                "width": 100,
                "height": 100
            }
        },
        "items": {
            "item1": {
                "width": 10,
                "height": 10,
                "can_rotate": false
            }
        }
    },
    "used": [
        {
            "panel": "panel1",
            "item": "item1",
            "x": 0.0,
            "y": 0.0,
            "rotate": false
        }
    ],
    "unused": [
        {
            "panel": "panel1",
            "width": 89.0,
            "height": 10.0,
            "x": 11.0,
            "y": 0.0
        },
        {
            "panel": "panel1",
            "width": 100.0,
            "height": 89.0,
            "x": 0.0,
            "y": 11.0
        }
    ]
}
```

## Acknowledgements

This project is a fork of [Bozo Kopic’s CSP solver](https://github.com/bozokopic/opcut) with nothing added, and everything except for the CLI interface removed.
