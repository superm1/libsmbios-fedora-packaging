# these are all substituted by autoconf
%define major 0
%define minor 13
%define sub 13
%define extralevel %{nil}
%define release_name libsmbios
%define release_version %{major}.%{minor}.%{sub}%{extralevel}

Name: %{release_name}
Version: %{release_version}
Release: 1%{?dist}
License: GPLv2+ or OSL
Group: System Environment/Libraries
Source: http://linux.dell.com/libsmbios/download/%{name}/%{name}-%{version}/%{name}-%{version}.tar.gz
URL: http://linux.dell.com/libsmbios/main
Summary: Open BIOS parsing libs
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# libsmbios only ever makes sense on intel compatible arches
# no DMI tables on ppc, s390, etc.
ExclusiveArch: x86_64 ia64 %{ix86}

BuildRequires: libxml2-devel

#EPEL4/5 dont have cppunit/cppunit-devel, so skip build tests
# everything else should be able to pull in cppunit to run unit tests
# during build. Doesnt affect binaries produced, so doesnt affect
# build reproducability.
%if %(test "%{dist}" != ".el4" -a "%{dist}" != ".el5" && echo 1 || echo 0)
BuildRequires: cppunit-devel
%endif

# no doxygen native for suse
%if %(test ! -e /etc/SuSE-release && echo 1 || echo 0)
BuildRequires: doxygen
%endif

%description
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

%package libs
Summary: Libsmbios shared libraries
Group: System Environment/Libraries
Obsoletes: libsmbiosxml-libs < 0:%{version}-%{release}
Obsoletes: libsmbios < 0:%{version}-%{release}
Provides: libsmbiosxml-libs = %{version}-%{release}


%package bin
Summary: The "supported" sample binaries that use libsmbios
Group: Applications/System
Requires: libsmbios-libs = %{version}-%{release}
Obsoletes: libsmbiosxml-bin < 0:%{version}-%{release}
Provides: libsmbiosxml-bin = %{version}-%{release}
Obsoletes: smbios-utils < 0:%{version}-%{release}

%package unsupported-bin
Summary: Unsupported sample binaries using libsmbios
Group: Applications/System
Requires: libsmbios-libs = %{version}-%{release}

%package devel
Summary: Development headers and archives
Group: Development/Libraries
Requires: libsmbios-libs = %{version}-%{release}

%description libs
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

%description devel
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

This package contains the headers and .a files necessary to compile new 
client programs against libsmbios.

%description bin
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

This package contains some sample binaries that use libsmbios.

%description unsupported-bin
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

This package contains some sample binaries that use libsmbios.

%prep
%setup -q 
find . -type d -exec chmod -f 755 {} \;
find doc include libraries bin-unsupported build bin-supported cppunit -type f -exec chmod -f 644 {} \;
chmod 755 cppunit/*.sh

%build
export EXTRA_CXXFLAGS="%{optflags}" 
export EXTRA_CFLAGS="%{optflags}" 
export RELEASE_MAJOR=%{major} 
export RELEASE_MINOR=%{minor} 
export RELEASE_SUBLEVEL=%{sub} 
export RELEASE_EXTRALEVEL=%{extralevel}
%configure
mkdir -p doc/full/html 
make -e %{?_smp_mflags} 
[ ! -d /usr/include/cppunit ] || make -e check

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
mkdir -p %{buildroot}/usr/include
cp -a include/smbios %{buildroot}/usr/include/
rm -f %{buildroot}/%{_libdir}/lib*.la
find %{buildroot}/usr/include -exec touch -r configure.ac {} \;
find doc/full -exec touch -r configure.ac {} \;

# backwards compatible:
ln -s /usr/sbin/dellWirelessCtl %{buildroot}/usr/bin/dellWirelessCtl


%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README
%{_libdir}/libsmbios.so.*
%{_libdir}/libsmbiosxml.so.*

%files devel
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README bin-unsupported/getopts_LICENSE.txt
/usr/include/smbios
%{_libdir}/libsmbios.a
%{_libdir}/libsmbios.so
%{_libdir}/libsmbiosxml.a
%{_libdir}/libsmbiosxml.so

%files bin 
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README bin-unsupported/getopts_LICENSE.txt
%{_sbindir}/assetTag
%{_sbindir}/dellBiosUpdate
%{_sbindir}/getSystemId
%{_sbindir}/propertyTag
%{_sbindir}/serviceTag
%{_sbindir}/tokenCtl
%{_sbindir}/verifySmiPassword
%{_sbindir}/wakeupCtl
%{_sbindir}/dellLcdBrightness
%{_sbindir}/dellWirelessCtl
%{_bindir}/dellWirelessCtl

%files unsupported-bin 
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README include/smbios/config/boost_LICENSE_1_0_txt bin-unsupported/getopts_LICENSE.txt
%{_sbindir}/dellLEDCtl
%{_sbindir}/activateCmosToken
%{_sbindir}/ascii2enUS_scancode
%{_sbindir}/createUnitTestFiles
%{_sbindir}/disable_console_redir
%{_sbindir}/dumpCmos
%{_sbindir}/getPasswordFormat
%{_sbindir}/isCmosTokenActive
%{_sbindir}/probes
%{_sbindir}/smitest
%{_sbindir}/stateByteCtl
%{_sbindir}/upBootCtl
%{_sbindir}/dumpSmbios

# ./ChangeLog is appended by configure
%changelog
* Mon Nov 26 2007 Michael Brown <mebrown@michaels-house.net> - 0.13.13-1
- Fix for compiling with recent gcc (from Danny Kukawa @ suse)
- fix for lsb issues - moved binaries to /usr/sbin/ because they require admin
  privs to run. Made one backwards-compat symlink to work with existing HAL
  which expects current location.

* Mon Aug 28 2007 Michael E Brown <michael_e_brown at dell.com> - 0.13.10-1
- Fix one instance where return code to fread was incorrectly checked.

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

