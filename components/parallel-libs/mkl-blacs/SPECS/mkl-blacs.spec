#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

#-ohpc-header-comp-begin-----------------------------

%include %{_sourcedir}/OHPC_macros

# OpenHPC convention: the default assumes the gnu toolchain and openmpi
# MPI family; however, these can be overridden by specifing the
# compiler_family and mpi_family variables via rpmbuild or other
# mechanisms.

%{!?compiler_family: %define compiler_family gnu}
%{!?mpi_family: %define mpi_family openmpi}
%{!?PROJ_DELIM:      %define PROJ_DELIM      %{nil}}

# Compiler dependencies
BuildRequires: lmod%{PROJ_DELIM} coreutils
%if %{compiler_family} == gnu
BuildRequires: gnu-compilers%{PROJ_DELIM}
Requires:      gnu-compilers%{PROJ_DELIM}
# require Intel runtime for MKL
BuildRequires: intel-compilers-devel%{PROJ_DELIM}
Requires:      intel-compilers-devel%{PROJ_DELIM}
%endif
%if %{compiler_family} == intel
BuildRequires: gcc-c++ intel-compilers-devel%{PROJ_DELIM}
Requires:      gcc-c++ intel-compilers-devel%{PROJ_DELIM}
%if 0%{?OHPC_BUILD}
BuildRequires: intel_licenses
%endif
%endif

# MPI dependencies
%if %{mpi_family} == impi
BuildRequires: intel-mpi-devel%{PROJ_DELIM}
Requires:      intel-mpi-devel%{PROJ_DELIM}
%endif
%if %{mpi_family} == mvapich2
BuildRequires: mvapich2-%{compiler_family}%{PROJ_DELIM}
Requires:      mvapich2-%{compiler_family}%{PROJ_DELIM}
%endif
%if %{mpi_family} == openmpi
BuildRequires: openmpi-%{compiler_family}%{PROJ_DELIM}
Requires:      openmpi-%{compiler_family}%{PROJ_DELIM}
%endif

#-ohpc-header-comp-end-------------------------------

# Base package name
%define pname mkl-blacs
%define PNAME %(echo %{pname} | tr [a-z] [A-Z])

Name:           %{pname}-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
Version:        11.3
Release:        0
Summary:        Intel(R) Math Kernel Library Basic Linear Algebra Communication Subprograms
License:        Intel(R) 
Group:          ohpc/parallel-libs
Url:            http://software.intel.com/en-us/intel-mkl
Source:         %{pname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%define debug_package %{nil}

%description
Intel(R) Math Kernel Library Basic Linear Algebra Communication Subprograms for openmpi

%prep
%setup -q -n %{pname}-%{version}

%build

export OHPC_COMPILER_FAMILY=%{compiler_family}
export OHPC_MPI_FAMILY=%{mpi_family}
. %{_sourcedir}/OHPC_setup_compiler
. %{_sourcedir}/OHPC_setup_mpi

# Enable MKL linkage for blas/lapack with gnu builds
%if %{compiler_family} == gnu
module load mkl
%endif

make sointel64 INSTALL_LIBNAME=libmkl_blacs_%{mpi_family}_lp64 INSTALL_DIR=`pwd`

%install

export OHPC_COMPILER_FAMILY=%{compiler_family}
export OHPC_MPI_FAMILY=%{mpi_family}
. %{_sourcedir}/OHPC_setup_compiler
. %{_sourcedir}/OHPC_setup_mpi

# Enable MKL linkage for blas/lapack with gnu builds
%if %{compiler_family} == gnu
module load mkl
%endif

%{__mkdir} -p %{buildroot}$MPI_DIR/lib

install -m644 *so %{buildroot}$MPI_DIR/lib/.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{OHPC_HOME}

%changelog

