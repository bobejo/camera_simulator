# camera_simulator

A versatile simulator for industrial and consumer cameras, designed to make it easy to develop and test camera integrations without needing physical hardware.

## Supported Camera Types

| Type | Status |
|---|---|
| GigE Vision |  Under development |
| UVC |  Planned |

## Requirements

- Python 3.10 - 3.14

## Installation

##
Clone the repository and enter the project directory:

```sh
git clone https://github.com/bobejo/genicam_simulator
uv pip install camera_simulator
```

## Development

Install [Hatch](https://hatch.pypa.io) if you haven't already:

```sh
uv tool install hatch
```


### Running tests

```sh
hatch test
```

### Formatting and linting
Run ruff
```sh
hatch fmt
```
### Run type check
Run the type checking using ´ty´
```sh
hatch run types:check
```

### Install pre-commit
Install the pre-commit that runs the checks when commiting.
```sh
pre-commit install
```
## GigE Vision

The GigE Vision implementation is based on the [GenICam standard](https://www.emva.org/wp-content/uploads/GenICam_Standard_v2_0.pdf) published by EMVA.
## UVC

See [linux implementation](https://github.com/torvalds/linux/blob/master/drivers/usb/gadget/function/f_uvc.c) and [Microsoft implementation guide](https://learn.microsoft.com/en-us/windows-hardware/drivers/stream/uvc-camera-implementation-guide)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.