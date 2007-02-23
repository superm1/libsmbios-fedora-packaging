# automatically determine if we should build docs based on presence of doxygen
#%define build_docs %( ( which doxygen > /dev/null 2>&1 && echo 1) || echo 0 )
# comment out docs until automake has been taught how to build them.
%define build_docs 0

# automatically determine if we should run cppunit based on presence or
# absense of cppunit include files.
%define run_cppunit %( ([ -e /usr/include/cppunit ] && echo 1) || echo 0)

# Some SUSE stuff is different
%define is_suse %(test -e /etc/SuSE-release && echo 1 || echo 0)

###################################################################
#
# WARNING
#
# These are all automatically replaced by the release script.
# START = Do not edit manually
%define major 0
%define minor 13
%define sub 2
%define extralevel %{nil}
%define release_name libsmbios
%define release_version %{major}.%{minor}.%{sub}%{extralevel}
#
# END = Do not edit manually
#
###################################################################

# allow --with[out] <feature> at rpm command line build, to override the above
# e.g. --with docs    ...or...   --without docs 
%{?_without_docs: %{expand: %%define build_docs 0}}
%{?_with_docs: %{expand: %%define build_docs 1}}
%{?_without_cppunit: %{expand: %%define run_cppunit 0}}
%{?_with_cppunit: %{expand: %%define run_cppunit 1}}

Name: %{release_name}
Version: %{release_version}
Release: 1%{?dist}
License: GPL/OSL Dual License
Group: System Environment/Libraries
Source: http://linux.dell.com/libsmbios/download/%{name}/%{name}-%{version}/%{name}-%{version}.tar.gz
URL: http://linux.dell.com/libsmbios/main
Summary: Open BIOS parsing libs
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# libsmbios only ever makes sense on intel compatible arches
# no DMI tables on ppc, s390, etc.
ExclusiveArch: x86_64 ia64 %{ix86}

BuildRequires: libxml2-devel
BuildRequires: cppunit-devel
%if %{is_suse}
# no doxygen native for suse
%else
BuildRequires: doxygen
%endif

%description
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

%package libs
Summary: Libsmbios shared libraries
Group: System Environment/Libraries
Obsoletes: libsmbiosxml-libs
Provides: libsmbiosxml-libs


%package bin
Summary: The "supported" sample binaries that use libsmbios
Group: Applications/System
Requires: libsmbios-libs = %{version}-%{release}
Obsoletes: libsmbiosxml-bin
Provides: libsmbiosxml-bin

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
client programs against libsmbios

%description bin
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

This package contains some sample binaries that use libsmbios.

%description unsupported-bin
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

This package contains some sample binaries that use libsmbios.

%prep
%setup 
find . -type d -exec chmod -f 755 {} \;
find doc include libraries bins build supported-bins cppunit -type f -exec chmod -f 644 {} \;

%build
%configure
make %{?_smp_mflags} EXTRA_CXXFLAGS="%{optflags}" EXTRA_CFLAGS="%{optflags}" -e RELEASE_MAJOR=%{major} RELEASE_MINOR=%{minor} RELEASE_SUBLEVEL=%{sub} RELEASE_EXTRALEVEL=%{extralevel}
%if %{build_docs}
    make -e RELEASE_MAJOR=%{major} RELEASE_MINOR=%{minor} RELEASE_SUBLEVEL=%{sub} RELEASE_EXTRALEVEL=%{extralevel} doxygen
%endif
%if %{run_cppunit}
    make -e EXTRA_CXXFLAGS="%{optflags}" EXTRA_CFLAGS="%{optflags}" RELEASE_MAJOR=%{major} RELEASE_MINOR=%{minor} RELEASE_SUBLEVEL=%{sub} RELEASE_EXTRALEVEL=%{extralevel} unit_test
%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/usr/include
cp -a include/smbios %{buildroot}/usr/include/
rm -f %{buildroot}/%{_libdir}/lib*.la

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%defattr(-,root,root)
%doc COPYING-GPL COPYING-OSL README
%{_libdir}/libsmbios.so.*.*
%{_libdir}/libsmbiosxml.so.*.*

%files devel
%defattr(-,root,root)
%doc COPYING-GPL COPYING-OSL README bins/getopts_LICENSE.txt
/usr/include/smbios
%{_libdir}/libsmbios.a
%{_libdir}/libsmbios.so
%{_libdir}/libsmbios.so.1
%{_libdir}/libsmbiosxml.a
%{_libdir}/libsmbiosxml.so
%{_libdir}/libsmbiosxml.so.1

%if %{build_docs}
    %doc doc/full/html
%endif


%files bin 
%defattr(-,root,root)
%doc COPYING-GPL COPYING-OSL README bins/getopts_LICENSE.txt
%{_bindir}/assetTag
%{_bindir}/dellBiosUpdate
%{_bindir}/getSystemId
%{_bindir}/propertyTag
%{_bindir}/serviceTag
%{_bindir}/tokenCtl
%{_bindir}/verifySmiPassword
%{_bindir}/wakeupCtl
%{_bindir}/dellLcdBrightness

%files unsupported-bin 
%defattr(-,root,root)
%doc COPYING-GPL COPYING-OSL README include/smbios/config/boost_LICENSE_1_0_txt bins/getopts_LICENSE.txt
%{_bindir}/activateCmosToken
%{_bindir}/ascii2enUS_scancode
%{_bindir}/createUnitTestFiles
%{_bindir}/disable_console_redir
%{_bindir}/dumpCmos
%{_bindir}/getPasswordFormat
%{_bindir}/isCmosTokenActive
%{_bindir}/probes
%{_bindir}/smitest
%{_bindir}/stateByteCtl
%{_bindir}/upBootCtl
%{_bindir}/dumpSmbios
#%{_bindir}/sysid

%changelog
* Tue Sep 26 2006 Michael E Brown <michael_e_brown at dell.com> - 0.12.4-1
- Changes per Fedora Packaging Guidelines to prepare to submit to Extras.
- Add in a changelog entry per Fedora Packaging Guidelines...
