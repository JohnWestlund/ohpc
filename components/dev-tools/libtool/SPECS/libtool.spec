#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%include %{_sourcedir}/OHPC_macros

%define pname libtool
%{!?PROJ_DELIM:%define PROJ_DELIM %{nil}}

Summary:   The GNU Portable Library Tool
Name:      %{pname}%{PROJ_DELIM}
Version:   2.4.6
Release:   1
License:   GPLv2+ and LGPLv2+ and GFDL
Group:     ohpc/dev-tools
URL:       http://www.gnu.org/software/libtool/
DocDir:    %{OHPC_PUB}/doc/contrib
Source0:   https://ftp.gnu.org/gnu/libtool/%{pname}-%{version}.tar.gz
Source1:   OHPC_macros
BuildRoot: %{_tmppath}/%{pname}-%{version}-%{release}-root

#!BuildIgnore: post-build-checks rpmlint-Factory

%define debug_package %{nil}
%define install_path %{OHPC_PUB}/autotools

Requires:      autoconf%{PROJ_DELIM} >= 2.69
Requires:      automake%{PROJ_DELIM} >= 1.14.1
BuildRequires: autoconf%{PROJ_DELIM} >= 2.69
BuildRequires: automake%{PROJ_DELIM} >= 1.14.1

%description
GNU Libtool is a set of shell scripts which automatically configure UNIX and
UNIX-like systems to generically build shared libraries. Libtool provides a
consistent, portable interface which simplifies the process of using shared
libraries.

If you are developing programs which will use shared libraries, but do not use
the rest of the GNU Autotools (such as GNU Autoconf and GNU Automake), you
should install the libtool package.

The libtool package also includes all files needed to integrate the GNU
Portable Library Tool (libtool) and the GNU Libtool Dynamic Module Loader
(ltdl) into a package built using the GNU Autotools (including GNU Autoconf
and GNU Automake).

%prep

%setup -n libtool-%{version}

%build
export PATH=%{install_path}/bin:$PATH
./configure --prefix=%{install_path}

%install
make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT install

# remove share/info/dir to avoid conflict with other package installs
rm -f $RPM_BUILD_ROOT/%{install_path}/share/info/dir


# modulefile

%{__mkdir_p} %{buildroot}/%{OHPC_MODULES}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/autotools
#%Module1.0#####################################################################

proc ModulesHelp { } {
puts stderr "This module loads the autotools collection to provide recent"
puts stderr "versions of autoconf, automake, and libtool."
puts stderr " "
}

module-whatis "Name: GNU Autotools"
module-whatis "Version: 1.0"
module-whatis "Category: utility, developer support"
module-whatis "Keywords: System, Utility"
module-whatis "Description: Developer utilities"

prepend-path    PATH            %{install_path}/bin
prepend-path    MANPATH         %{install_path}/share/man
EOF

%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{OHPC_PUB}
%dir %{OHPC_MODULES}
%{OHPC_PUB}
%{OHPC_MODULES}/autotools
%doc AUTHORS
%doc ChangeLog
%doc COPYING
%doc NEWS
%doc README
%doc THANKS
%doc TODO



%changelog
* Mon Sep 15 2014  <karl.w.schulz@intel.com> - 
- Initial build.

