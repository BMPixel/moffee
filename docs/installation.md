# Installation Guide for Moffee

## Prerequisites

- Python 3.10 or higher

## Installing pipx (optional)

For a basic installation of `pipx`, you can use pip:

```bash
pip install pipx
```

For more detailed installation instructions or if you encounter any issues, please refer to the [official pipx documentation](https://pypa.github.io/pipx/installation/).

## Installing Moffee

Moffee is a Python package and is recommended to be installed using `pipx`:

```bash
pipx install moffee
```

Alternatively, if you prefer to use pip directly:

```bash
pip install moffee
```

## Verifying the Installation

To verify that Moffee has been installed correctly, you can run:

```bash
moffee --version
```

This should display the version number of Moffee installed on your system.

## Usage

Once installed, you can use Moffee to preview slides in a live web server or export them to HTML:

### Preview slides in a live web server

```bash
moffee live example.md
```

This command will launch a local server and open your default web browser to display the slides.

### Export slides to HTML

```bash
moffee make example.md -o output_html/
```

This command will generate HTML files in the specified `output_html/` directory.

For more advanced usage and configuration options, refer to the Moffee documentation or run `moffee --help`.
