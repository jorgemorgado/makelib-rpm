# makelib-rpm

## Description

This software provides a framework to automate RPM package creation.

## Installation

You can use the makelib-rpm to build its own RPM package. Although, for this
to work, you need to manually copy the `sources/Makefile` into the right place.
Example:

```bash
# Clone this repository
git clone https://github.com/jorgemorgado/makelib-rpm

# Manually install the framework
mkdir -p /usr/local/makelib && \
  cp makelib-rpm/sources/Makefile /usr/local/makelib

# Build makelib RPM package
cd makelib-rpm
make everything
```

Assuming everything works as expected, you should now have an RPM package
in the `RPMS` directory. You can then install the package using
`yum localinstall ...`

## Usage

Please refer to the usage information in the `sources/Makefile`. The following
targets are available:

* all
* checkspec
* configure
* compile
* install
* build
* release [REPONAME=name]
* clean
* distclean
* everything

Each target automates one specific task in the RPM package creation. Specific
actions can be included in the `./Makefile` from the targets `configure` to
`build`.

## Package release

The `release` target is a special case that typically requires the release
scripts and sudo file to be installed on your repository server. The repository
server must then be defined in the `./Makefile` (see `REPOHOST`).

A package can be released to a specific repository using the `REPONAME` option (default `REPONAME` is `_`):

```bash
make release REPONAME=name
```

Tipically you should install the `makelib` package on your build host, and the `makelib-release` package on your repository host. The release target will then work as follows:

```code
+----------- Build host ---------- | --------- Repo host ----------+
| make release --> release_remote --> release_local --> index_repo |
+------------------------------------------------------------------+
```

## License

This repository is released under the [GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.en.html)
