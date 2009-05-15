# pkg/libsmbios.spec.  Generated from libsmbios.spec.in by configure.

# these are all substituted by autoconf
%define major 2
%define minor 2
%define micro 16
%define extra %{nil}
%define lang_dom  libsmbios-2.2
%define release_version %{major}.%{minor}.%{micro}%{extra}

%define release_name libsmbios
%define other_name   libsmbios2

# suse naming conventions
%if 0%{?suse_version}
%define release_name libsmbios2
%define other_name   libsmbios
%endif

# required by suse build system
# norootforbuild

%{!?build_python:   %define build_python 1}
%{?_with_python:    %define build_python 1}
%{?_without_python: %define build_python 0}

%{!?run_unit_tests:     %define run_unit_tests 1}
%{?_without_unit_tests: %define run_unit_tests 0}
%{?_with_unit_tests:    %define run_unit_tests 1}

# some distros already have fdupes macro. If not, we just set it to something innocuous
%{?!fdupes: %define fdupes /usr/sbin/hardlink -c -v}

%define pkgconfig_BR pkgconfig
%define ctypes_BR python-ctypes
%define cppunit_BR cppunit-devel
%define fdupes_BR hardlink
%define valgrind_BR valgrind
# Some variable definitions so that we can be compatible between SUSE Build service and Fedora build system
# SUSE: fedora_version  suse_version rhel_version centos_version sles_version
# Fedora: fedora dist fc8 fc9

# suse/sles
%if 0%{?suse_version}
%if 0%{?suse_version} < 1000
    %define valgrind_BR %{nil}
%endif
%if 0%{?suse_version} >= 1020
    # suse never added python-ctypes provides to python 2.5 :(
    %define ctypes_BR %{nil}
%endif
%if 0%{?suse_version} > 1020
    %define fdupes_BR fdupes
%else
    %define fdupes_BR %{nil}
    %define fdupes echo fdupes disabled
%endif
%endif

# rhel
%if 0%{?rhel_version}
%if 0%{?rhel_version} < 500
    %define fdupes echo fdupes disabled
    %define fdupes_BR %{nil}
    # dont yet have rhel4 cppunit
    %define cppunit_BR %{nil}
%endif
%if 0%{?rhel_version} < 400
    # dont yet have rhel3 valgrind
    %define valgrind_BR %{nil}
    # no python-ctypes for python <= 2.2
    %define build_python 0
%endif
%endif

%define python_devel_BR %{nil}
%define cond_disable_python --disable-python
%if %{build_python}
    %define cond_disable_python %{nil}
    %define python_devel_BR python-devel
    # per fedora and suse python packaging guidelines
    # suse: will define py_sitedir for us
    # fedora: use the !? code below to define when it isnt already
    %{!?py_sitedir: %define py_sitedir %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

%if !%{run_unit_tests}
    %define valgrind_BR %{nil}
    %define cppunit_BR %{nil}
%endif

Name: %{release_name}
Version: %{release_version}
Release: 2.1%{?releasesuffix}%{?dist}
License: GPLv2+ or OSL 2.1
Summary: Libsmbios C/C++ shared libraries
Group: System Environment/Libraries
Source: http://linux.dell.com/libsmbios/download/libsmbios/libsmbios-%{version}/libsmbios-%{version}.tar.bz2
URL: http://linux.dell.com/libsmbios/main
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: strace libxml2-devel gcc-c++ gettext doxygen %{valgrind_BR} %{cppunit_BR} %{fdupes_BR} %{pkgconfig_BR} %{python_devel_BR}
# uncomment for official fedora
Obsoletes: libsmbios-libs < 2.0.0
Provides: libsmbios-libs = 0:%{version}-%{release}
Obsoletes: %{other_name} <= 0:%{version}-%{release}
Provides: %{other_name}  0:%{version}-%{release}

# libsmbios only ever makes sense on intel compatible arches
# no DMI tables on ppc, s390, etc.
ExclusiveArch: x86_64 ia64 %{ix86}

%description
Libsmbios is a library and utilities that can be used by client programs to get
information from standard BIOS tables, such as the SMBIOS table.

This package provides the C-based libsmbios library, with a C interface.

This package also has a C++-based library, with a C++ interface. It is not
actively maintained, but provided for backwards compatibility. New programs
should use the libsmbios C interface.


%package -n python-smbios
Summary: Python interface to Libsmbios C library
Group: System Environment/Libraries
Requires: %{release_name} = 0:%{version}-%{release}
Requires: python %{ctypes_BR} redhat-rpm-config

%description -n python-smbios
This package provides a Python interface to libsmbios

%package -n smbios-utils
Summary: meta-package that pulls in all smbios utilities (binary executables and python scripts)
Group: Applications/System
Requires: smbios-utils-bin
%if %{build_python}
Requires: smbios-utils-python
%endif
Obsoletes: libsmbios-bin < 0:2.0.0
Provides: libsmbios-bin = %{version}-%{release}
Obsoletes: libsmbios-unsupported-bin < 0:2.0.0
Provides: libsmbios-unsupported-bin = %{version}-%{release}

%description -n smbios-utils
This is a meta-package that pulls in the binary libsmbios executables as well
as the python executables.

%package -n smbios-utils-bin
Summary: Binary utilities that use libsmbios
Group: Applications/System
Requires: %{release_name} = 0:%{version}-%{release}

%description -n smbios-utils-bin
Get BIOS information, such as System product name, product id, service tag and
asset tag.

%package -n smbios-utils-python
Summary: Python executables that use libsmbios
Group: Applications/System
Requires: python-smbios = %{version}-%{release}

%description -n smbios-utils-python
Get BIOS information, such as System product name, product id, service tag and
asset tag. Set service and asset tags on Dell machines. Manipulate wireless
cards/bluetooth on Dell laptops. Set BIOS password on select Dell systems.
Update BIOS on select Dell systems. Set LCD brightness on select Dell laptops.

# name the devel package libsmbios-devel regardless of package name, per suse/fedora convention
%package -n libsmbios-devel
Summary: Development headers and archives
Group: Development/Libraries
Requires: %{release_name} = 0:%{version}-%{release}
Provides: libsmbios2-devel = %{version}-%{release}
Obsoletes: libsmbios2-devel < %{version}-%{release}

%description -n libsmbios-devel
Libsmbios is a library and utilities that can be used by client programs to get
information from standard BIOS tables, such as the SMBIOS table.

This package contains the headers and .a files necessary to compile new client
programs against libsmbios.


%prep
%setup -q -n libsmbios-%{version}
find . -type d -exec chmod -f 755 {} \;
find doc src -type f -exec chmod -f 644 {} \;
chmod 755 src/cppunit/*.sh

%build
# this line lets us build an RPM directly from a git tarball
# and retains any customized version information we might have
[ -e ./configure ] || \
    RELEASE_MAJOR=%{major}  \
    RELEASE_MINOR=%{minor}  \
    RELEASE_MICRO=%{micro}  \
    RELEASE_EXTRA=%{extra}  \
    ./autogen.sh --no-configure

mkdir _build
cd _build
echo '../configure "$@"' > configure
chmod +x ./configure

%configure \
    --disable-static    \
    %{cond_disable_python} \
    CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
mkdir -p out/libsmbios_c
mkdir -p out/libsmbios_c++
make -e %{?_smp_mflags} 2>&1 | tee build.log

echo \%doc _build/build.log > buildlogs.txt

%check
runtest() {
    mkdir _$1$2
%if 0%{?run_unit_tests}
    pushd _$1$2
    ../configure
    make -e $1 CFLAGS="$CFLAGS -DDEBUG_OUTPUT_ALL" 2>&1 | tee $1$2.log
    #make -e $1 2>&1 | tee $1$2.log
    popd
    echo \%doc _$1$2/$1$2.log >> _build/buildlogs.txt
%endif
}

if [ -d /usr/include/cppunit ]; then
   # run this first since it is slightly faster than valgrind
    VALGRIND="strace -f" runtest check strace > /dev/null || echo FAILED strace check
fi

if [ -e /usr/bin/valgrind -a -d /usr/include/cppunit ]; then
    runtest valgrind > /dev/null || echo FAILED valgrind check
fi

if [ -d /usr/include/cppunit ]; then
    runtest check > /dev/null || echo FAILED check
fi

if [ ! -d /usr/include/cppunit ]; then
    echo "Unit tests skipped due to missing cppunit."
fi

%install
rm -rf %{buildroot}
mkdir %{buildroot}

cd _build
TOPDIR=..
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
mkdir -p %{buildroot}/usr/include
cp -a $TOPDIR/src/include/*  %{buildroot}/usr/include/
cp -a out/public-include/*  %{buildroot}/usr/include/
rm -f %{buildroot}/%{_libdir}/lib*.la
find %{buildroot}/usr/include out/libsmbios_c++ out/libsmbios_c -exec touch -r $TOPDIR/configure.ac {} \;

# backwards compatible:
%if %{build_python}
ln -s ../sbin/dellWirelessCtl %{buildroot}/usr/bin/dellWirelessCtl
ln -s smbios-sys-info %{buildroot}%{_sbindir}/getSystemId
ln -s smbios-wireless-ctl %{buildroot}%{_sbindir}/dellWirelessCtl
ln -s smbios-lcd-brightness %{buildroot}%{_sbindir}/dellLcdBrightness
ln -s smbios-rbu-bios-update %{buildroot}%{_sbindir}/dellBiosUpdate
%endif

%find_lang %{lang_dom}

# hardlink files to save some space.
%fdupes $RPM_BUILD_ROOT

%clean
rm -rf %{buildroot}

%post   -n %{release_name}   -p /sbin/ldconfig
%postun -n %{release_name}   -p /sbin/ldconfig

%files -n %{release_name} -f _build/%{lang_dom}.lang
%defattr(-,root,root,-)
%{_libdir}/libsmbios_c.so.*
%{_libdir}/libsmbios.so.*

%if %{build_python}
%files -n python-smbios
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README
%{py_sitedir}/*
%endif

%files -n libsmbios-devel -f _build/buildlogs.txt
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README src/bin/getopts_LICENSE.txt src/include/smbios/config/boost_LICENSE_1_0_txt
/usr/include/smbios
/usr/include/smbios_c
%{_libdir}/libsmbios.so
%{_libdir}/libsmbios_c.so
%{_libdir}/pkgconfig/*.pc
%doc _build/out/libsmbios_c++
%doc _build/out/libsmbios_c

%files -n smbios-utils
# opensuse 11.1 enforces non-empty file list :(
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README
# no other files.

%files -n smbios-utils-bin
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README
%doc src/bin/getopts_LICENSE.txt src/include/smbios/config/boost_LICENSE_1_0_txt
%doc doc/pkgheader.sh

# legacy C++
%{_sbindir}/dellBiosUpdate-compat
%{_sbindir}/dellLEDCtl
%ifnarch ia64
%{_sbindir}/dellMediaDirectCtl
%endif

# new C utilities
%{_sbindir}/smbios-state-byte-ctl
%{_sbindir}/smbios-get-ut-data
%{_sbindir}/smbios-upflag-ctl
%{_sbindir}/smbios-sys-info-lite


%if %{build_python}
%files -n smbios-utils-python
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README
%doc src/bin/getopts_LICENSE.txt src/include/smbios/config/boost_LICENSE_1_0_txt
%doc doc/pkgheader.sh
%dir %{_sysconfdir}/libsmbios
%config(noreplace) %{_sysconfdir}/libsmbios/*

# YUM Plugin
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/dellsysidplugin2.conf
%{_exec_prefix}/lib/yum-plugins/*
# SUSE build has anal directory ownership check. RPM which owns all dirs *must*
# be installed at buildtime.
%if 0%{?suse_version} >= 1100
%dir %{_sysconfdir}/yum
%dir %{_sysconfdir}/yum/pluginconf.d/
%dir %{_exec_prefix}/lib/yum-plugins/
%endif

# python utilities
%{_sbindir}/smbios-sys-info
%{_sbindir}/smbios-token-ctl
%{_sbindir}/smbios-passwd
%{_sbindir}/smbios-wakeup-ctl
%{_sbindir}/smbios-wireless-ctl
%{_sbindir}/smbios-rbu-bios-update
%{_sbindir}/smbios-lcd-brightness

# symlinks: backwards compat
%{_sbindir}/dellLcdBrightness
%{_sbindir}/getSystemId
%{_sbindir}/dellWirelessCtl
%{_sbindir}/dellBiosUpdate
# used by HAL in old location, so keep it around until HAL is updated.
%{_bindir}/dellWirelessCtl

# data files
%{_datadir}/smbios-utils
%endif

%changelog
* Mon Mar 24 2009 Michael E Brown <michael_e_brown at dell.com> - 2.2.16-1
- add gcc 4.4 support

* Mon Mar 24 2009 Michael E Brown <michael_e_brown at dell.com> - 2.2.15-1
- update to lastest upstream.
- fixes bug in bios update on systems with versions like x.y.z.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 3 2009 Michael E Brown <michael_e_brown at dell.com> - 2.2.12-1
- Add feature to turn on debugging printf()'s without recompiling by setting
  certain environment variables:
    LIBSMBIOS_C_DEBUG_OUTPUT_ALL    -- all debugging output
        or, per module:
    LIBSMBIOS_C_DEBUG_CONSTRUCTOR_C
    LIBSMBIOS_C_DEBUG_SYSINFO_C
    LIBSMBIOS_C_DEBUG_SMBIOS_C
    LIBSMBIOS_C_DEBUG_TOKEN_C
    LIBSMBIOS_C_DEBUG_MEMORY_C
    LIBSMBIOS_C_DEBUG_CMOS_C
    LIBSMBIOS_C_DEBUG_SMI_C

* Mon Feb 2 2009 Michael E Brown <michael_e_brown at dell.com> - 2.2.12-1
- Add pkgconfig files to -devel
- fixup yum plugin to not parse certain data that causes a crash on some machines (Optiplex 755, others may be affected)

* Thu Jan 15 2009 Michael E Brown <michael_e_brown at dell.com> - 2.2.8-1
- revert change in upstream renaming rpm to libsmbios2

* Thu Jan 15 2009 Michael E Brown <michael_e_brown at dell.com> - 2.2.7-1
- change source to bz2 format
- Update to latest upstream release. Many changes in the new release:
  - python interface
  - libsmbios_c interface almost fully implemented
  - libsmbios c++ interface deprecated

* Tue Oct 28 2008 Michael E Brown <michael_e_brown at dell.com> - 2.2.0-1
- Spec updates

* Mon Apr 21 2008 Michael E Brown <michael_e_brown at dell.com> - 2.0.1-2.1
- obsolete libsmbios-libs as well

* Mon Mar 3 2008 Michael E Brown <michael_e_brown at dell.com> - 2.0.1-2
- properly obsolete older versions

* Wed Feb 13 2008 Michael E Brown <michael_e_brown at dell.com> - 2.0.1
- Fixup GCC 4.3 compile issues.

* Wed Jan 9 2008 Michael E Brown <michael_e_brown at dell.com> - 2.0.0
- ABI incompatible, minor API changes
- sync up libsmbios soname with version #
- move binaries to /usr/sbin as they are only runnable by root
- drop libsmbiosxml lib as it was mostly unused.
- drop autotools generated files out of git and add autogen.sh
- drop tokenCtl binary-- pysmbios has a *much* improved version

* Wed Aug 22 2007 Michael E Brown <michael_e_brown at dell.com> - 0.13.9
- Fix a couple of failure-to-check-return on fopen. most were unit-test code
  only, but two or three were in regular code.
- Add hinting to the memory class, so that it can intelligently close /dev/mem
  file handle when it is not needed (which is most of the time). it only
  leaves it open when it is scanning, so speed is not impacted.

* Tue Aug 6 2007 Michael E Brown <michael_e_brown at dell.com> - 0.13.8
- new upstream

* Tue Apr 3 2007 Michael E Brown <michael_e_brown at dell.com> - 0.13.6
- critical bugfix for dellBiosUpdate utility for packet mode
- autoconf/automake support for automatically building docs
- more readable 'make' lines by splitting out env vars
- remove run_cppunit option... always run unit tests.
- update autoconf/automake utilities to latest version
- fix LDFLAGS to not overwrite user entered LDFLAGS
- add automatic doxygen build of docs
- fix urls of public repos
- remove yum repo page in favor of official page from docs
- split dmi table entry point from smbios table entry point
- support legacy _DMI_ tables
- fix support for EFI-based imacs without proper _SM_ anchor

* Tue Mar 20 2007 Michael E Brown <michael_e_brown at dell.com> - 0.13.5
- rpmlint cleanups
- Add dellLEDCtl binary
- update AUTHORS file to add credit for dellLEDCtl
- update doc/DellToken.txt to add a few more useful tokens.
- updated build system to create documentation
- skip cppunit dep on .elX builds (not in EPEL yet)

* Mon Mar 12 2007 Michael E Brown <michael_e_brown at dell.com> - 0.13.4-1
- Added dellWirelessCtl binary
- Added 'static' makefile target to build static binaries and clean them as well
- fix for signed/unsigned bug in probes binary. CPU temp misreported
- simplify interface for DELL_CALLING_INTERFACE_SMI, autodetect Port/Magic
- document all of the tokens for controlling wireless on dell notebooks
- enums for SMI args/res to make code match docs better (cbRES1 = res[0], which
  was confusing.
- helper functions isTokenActive() and activateToken() to simplify token API.
- Added missing windows .cpp files to the dist tarball for those who compile
  windows from dist tarball vs source control
- Add support for EFI based machines without backwards compatible smbios table
  entry point in 0xF0000 block.
- Added wirelessSwitchControl() and wirelessRadioControl() API for newer
  laptops.
- fixed bug in TokenDA activate() code where it wasnt properly using SMI
  (never worked, but apparently wasnt used until now.)

* Tue Oct 3 2006 Michael E Brown <Michael_E_Brown@Dell.com> - 0.13.0-1
- autotools conversion
- add Changelog

* Tue Sep 26 2006 Michael E Brown <michael_e_brown at dell.com> - 0.12.4-1
- Changes per Fedora Packaging Guidelines to prepare to submit to Extras.
- Add in a changelog entry per Fedora Packaging Guidelines...

