################################################################################
#
# Makefile: Red Hat/RPM package creation
#
# Written by Jorge Morgado jorge (at) morgado (dot) ch, February 2012
# Copyright (c) 2012, Jorge Morgado
# All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
###########################################################################
#
# This software provides a framework to automate RPM package creation.
#
# Targets:
# 
#   all
#   checkspec
#   configure
#   compile
#   install
#   build
#   release
#   clean
#   distclean
#   everything
#
# *** PLEASE REMEMBER ***
#
# You should not create RPM packages as 'root' - this is a bad practice!!
# The recommended way to use this framework is:
#
# 1. Use a non-root account.
# 2. If you have use an RPM macros file (typically ~/.rpmmacros) ensure
#    there is no `%_topdir' directive defined. Trying to change the build
#    directory breaks on some (badly written?) SPEC files. makelib will
#    try to build the packages using ~/rpmbuild (the default).
# 3. Make sure /var/tmp exsits and has mode 1777. If ~/rpmbuild does not
#    exist, makelib will create it as a symlink to /var/tmp/$USER/rpmbuild.
# 4. Create a build environment for the RPM package you want to create.
#    Example for package 'mypkg.rpm':
#
#    mkdir -p mypkg/{sources,install}
#    cd mypkg
#    vi Makefile
#
# 5. If you have an SRPM package you can extract the needed files from it:
#
#    rpm2cpio yourfile.src.rpm | cpio -idmv
#    mv yourfile.spec install/
#    mv yourfile.tar.{bz2,gz} sources/
#    mv yourfile.patch sources/
#    mv yourfile.othersources sources/
#
# 6. Write your Makefile (if needed) and start using the above targets.
#    Example:
#
#    make configure
#    make compile
#    make install
#    make build
#
# 7. If a target fails, you can check get both STDERR and STDOUT in `.log/`
#    directory. If you have no errors, the recommended way to build the
#    package is:
#
#    make everything
#
################################################################################

################################################################################
# Initial variables are assigned just once
################################################################################

SHELL        := /bin/bash
BOLD         := \033[1m
BOLDX        := \033[0m

# find the name of the SPEC file; if not found, return /dev/null so the
# next shell commands below (mostly grep) don't fail silently
SPEC         := \
	$(strip $(shell \
	  pwd=`pwd`; \
	  self=`basename $$pwd`; \
	  file=`find install -name "$${self}.spec"`; \
	  if [ "$$file" ]; then \
	    echo $$file; \
	  else \
	    echo /dev/null; \
	  fi; ))

SUMMARY      := $(strip $(shell grep -i ^SUMMARY: $(SPEC) | cut -d: -f2))
LICENSE      := $(strip $(shell grep -i ^LICENSE: $(SPEC) | cut -d: -f2))
NAMEORIG     := $(strip $(shell grep -i ^NAME: $(SPEC) | cut -d: -f2))
VERSIONORIG  := $(strip $(shell grep -i ^VERSION: $(SPEC) | cut -d: -f2 | head -1))
RELEASE      := $(strip $(shell grep -i ^RELEASE: $(SPEC) | cut -d: -f2))
SOURCE       := $(strip $(shell grep -i ^SOURCE $(SPEC) | cut -d: -f2))
PREFIX       := $(strip $(shell grep -i ^PREFIX: $(SPEC) | cut -d: -f2))
GROUP        := $(strip $(shell grep -i ^GROUP: $(SPEC) | cut -d: -f2))
URL          := $(strip $(shell grep -i ^URL: $(SPEC) | cut -d: -f2))
DISTRIBUTION := $(strip $(shell grep -i ^DISTRIBUTION: $(SPEC) | cut -d: -f2))
VENDOR       := $(strip $(shell grep -i ^VENDOR: $(SPEC) | cut -d: -f2))

PACKAGER     := $(strip $(shell grep -i PACKAGER: $(SPEC) | cut -d: -f2))

SYS          := $(strip $(shell cat /etc/redhat-release))
SYSLIB       := /usr/local/makelib
DISTNAME     := REDHAT

TMPDIR       := $(shell echo "/tmp/makelib-$$$$")
RHEL_MAJOR   := $(shell rhel=`cut -d: -f5 /etc/system-release-cpe`; echo $${rhel:0:1})

# take architecture if defined; if not, use `uname -i`
ARCHITECTURE := \
	$(strip $(shell \
	  arch=`grep -i BUILDARCH: $(SPEC) | cut -d: -f2`; \
	  if [ "$$arch" ]; then \
	    echo $$arch; \
	  else \
	    uname -i; \
	  fi; ))

# truncate the summary to max. 55 chars
DESCSHORT    := $(shell echo '$(SUMMARY)' | cut -c1-55)

################################################################################
# Functions for the build target
################################################################################

# expands variables in a string (add more as needed)
func_expand_vars = \
	$(strip $(shell \
	  echo "$(1)" | \
	  sed -e 's/%(echo \([^:]*\))/\1/' | \
	  sed -e 's/%{name}/$(NAME)/' | \
	  sed -e 's/%{version}/$(VERSION)/' ))

# translates a directive into its defined value
func_get_defined = \
	$(strip $(shell \
          if ( echo "$(2)" | grep "^%{.*}$$" >/dev/null ); then \
            res=`echo $(2) | sed -e 's/^%{\(.*\)}$$/\1/'`; \
            grep "%define $$res" $(1) | rev | cut -d' ' -f1 | rev; \
          else \
            echo $(2); \
	  fi; ))

# package name is usually a defined directive (although this is useless,
# as those are implicitely defined from corresponding tags)
NAME    = $(call func_get_defined,$(SPEC),$(NAMEORIG))
# same for version
VERSION = $(call func_get_defined,$(SPEC),$(VERSIONORIG))

################################################################################
# The default target prints basic package information and a list of possible
# make targets. The list contains all targets of both files Makefile and
# Makefile.rpm that do not contain any punctuation characters. Comments on the
# same line separated by a hash (#) sign are also printed.
################################################################################
.PHONY: all
all: check.sane my.all

my.all:
	@printf "\n"; \
	 printf " Package:       [\033[1m%s\033[0m]\n" "$(NAME)"; \
	 printf " Version:       [\033[1m%s\033[0m]\n" "$(VERSION)"; \
	 printf " Summary:       [\033[1m%s...\033[0m]\n" "$(DESCSHORT)"; \
	 printf " Target System: [\033[1m$(DISTNAME)\033[0m]\n"; \
	 printf " Target Arch:   [\033[1m%s\033[0m]\n\n" "$(ARCHITECTURE)"; \
	 printf "\n Choose target from:\n"
	@lasttarget="`if [ -f .target ]; then cat .target; fi`"; \
	 if [ -z "$$lasttarget" ]; then lasttarget="configure"; fi; \
	 cat Makefile | egrep '^[a-zA-Z0-9]*:' | \
	 egrep -v '^all' | sed -e 's/:[^#]*//' | \
	 awk -F# '{if($$1==hit){printf("%s ->",b);}else{printf("%s   ",bx)}; \
	   printf(" %-10s %s\n",$$1,$$2)}' b="$(BOLD)" bx="$(BOLDX)" hit=$$lasttarget | \
	 awk '{if(/./){if(a>0){print}else{a=1;print "\n"$$0}}}'; \
	 printf "\n"; \
	 cat $(SYSLIB)/Makefile.rpm | egrep '^[a-zA-Z0-9]*:' | \
	 egrep -v '^all' | sed -e 's/:[^#]*//' | \
	 awk -F# '{if($$1==hit){printf("%s ->",b);}else{printf("%s   ",bx)}; \
	 printf(" %-10s %s\n",$$1,$$2)}' b="$(BOLD)" bx="$(BOLDX)" hit=$$lasttarget; \
	 printf "\n"

################################################################################
# The checkspec target tests the spec file
################################################################################
.PHONY: checkspec pre.checkspec post.checkspec my.checkspec
checkspec: check.sane pre.checkspec my.checkspec post.checkspec # syntax check the spec file

pre.checkspec:
	@printf "=== target \`checkspec' for $(SYS)-$(ARCHITECTURE) ===\n"

# don't execute any build stages - this is just to test the spec file
post.checkspec:
	@rpmbuild --quiet --nobuild $(SPEC)
	@printf "Spec file '$(SPEC)' seems to be okay\n"
	@printf "=== \`checkspec' done ===\n"

################################################################################
# The configure target prepares the source for compilation
################################################################################
.PHONY: configure pre.configure post.configure my.configure
configure: check.sane pre.configure my.configure post.configure # configure source for compilation

pre.configure:
	@printf "=== target \`configure' for $(SYS)-$(ARCHITECTURE) ===\n"
	@mkdir -p .log;
	@if find "sources" -mindepth 1 -print -quit | grep -q .; then \
	   cp -rf sources/* ~/rpmbuild/SOURCES/; \
	 fi;
	@cp $(SPEC) ~/rpmbuild/SPECS;

# do the prep stage and update the new target on success
post.configure:
	@rpmbuild -bp $(CONFIGURE_ARGS) $(SPEC) 2> \
	   .log/configure-err.log | tee .log/configure-out.log
	@printf "compile\n" > .target;
	@printf "=== \`configure' done ===\n"

################################################################################
# The compile target compiles the source
################################################################################
.PHONY: compile pre.compile post.compile my.compile
compile: check.sane pre.compile my.compile post.compile # compile sources

pre.compile:
	@printf "=== target \`compile' for $(SYS)-$(ARCHITECTURE) ===\n"
	@mkdir -p .log;

# do the build stage
post.compile:
	@rpmbuild --short-circuit -bc $(COMPILE_ARGS) $(SPEC) 2> \
	   .log/compile-err.log | tee .log/compile-out.log
	@printf "install\n" > .target
	@printf "=== \`compile' done ===\n"

################################################################################
# The install target installs the package files
################################################################################
.PHONY: install pre.install post.install my.install
install: check.sane pre.install my.install post.install # install objects in the build directory

pre.install:
	@printf "=== target \`install' for $(SYS)-$(ARCHITECTURE) ===\n"
	@mkdir -p .log;

# do the install stage
post.install:
	@rpmbuild --short-circuit -bi $(INSTALL_ARGS) $(SPEC) 2> \
	   .log/install-err.log | tee .log/install-out.log
	@printf "build\n" > .target
	@printf "=== \`install' done ===\n"

################################################################################
# The build target builds the package
################################################################################
.PHONY: build pre.build post.build my.build
build: check.sane pre.build my.build post.build # build package

pre.build:
	@printf "=== target \`build' for $(SYS)-$(ARCHITECTURE) ===\n"
	@mkdir -p .log;

# do the build (all) stage
post.build:
	@rpmbuild -ba $(BUILD_ARGS) $(SPEC) 2> \
	   .log/build-err.log | tee .log/build-out.log
	@( cp -rf ~/rpmbuild/SRPMS . ) && rm -rf ~/rpmbuild/SRPMS;
	@( cp -rf ~/rpmbuild/RPMS . ) && rm -rf ~/rpmbuild/RPMS;
	@printf "release\n" > .target
	@printf "=== \`build' done ===\n"

################################################################################
# The release target copies the built package to the Ubuntu repository
################################################################################
.PHONY: release pre.release post.release
release: check.sane pre.release post.release # publish package into repository

pre.release:
	@printf "=== target \`release' for $(SYS)-$(ARCHITECTURE) ===\n"
	@if [ "$(REPOHOST)" ]; then \
	   ssh -q $(REPOHOST) mkdir $(TMPDIR); \
	   scp -q -r SRPMS RPMS $(REPOHOST):$(TMPDIR); \
	   ssh -q -tt $(REPOHOST) sudo /usr/local/makelib/release "$(TMPDIR)" rhel $(RHEL_MAJOR); \
	 else \
	   printf "You need to define a REPOHOST to release the package(s)\n"; \
	   exit 1; \
	 fi;

post.release:
	@printf "distclean\n" > .target
	@printf "=== \`release' done ===\n"

################################################################################
# The clean target removes the package
################################################################################
.PHONY: clean
clean: # remove packages
	@printf "+++ removing old package and log files +++\n"
	@( rpmbuild --clean $(SPEC) >/dev/null 2>&1 ) || exit 0
	@( rpmbuild --rmsource $(SPEC) >/dev/null 2>&1 ) || exit 0
	@rm -rf ./SRPMS ./RPMS ./.log
	@rm -f .target

################################################################################
# The distclean target removes the package and all compiled objects
################################################################################
.PHONY: distclean my.distclean
distclean: clean my.distclean # remove package and all compiled objects
	@printf "+++ removing all files +++\n"
	@rm -rf ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

################################################################################
# Do the whole package build cycle
################################################################################
.PHONY: everything
everything: clean configure build # do it all! (clean, configure, build)

################################################################################
# Do some checks
################################################################################
.PHONY: check.sane
check.sane:
	@if [ ! -d ~/rpmbuild ]; then \
	   mkdir -p /var/tmp/$$USER/rpmbuild; \
	   ln -s /var/tmp/$$USER/rpmbuild ~/; \
	 fi;
	@mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS};
ifeq ($(SPEC),)
	$(error Spec file not found under ./install)
endif
#ifneq ($(NAME).spec,$(notdir $(SPEC)))
#	$(error The spec file must be named $(NAME).spec)
#endif
ifndef SPEC
	$(error The spec file is missing)
endif
ifndef SUMMARY
	$(error The SUMMARY is missing)
endif
ifndef VERSION
	$(error The VERSION is missing)
endif
ifndef SOURCE
	$(error The SOURCE is missing)
endif
ifndef GROUP
	$(error The GROUP is missing)
endif
