%define	major	5.0
%define	libname %mklibname lua %{major}
%define alt_priority %(echo %{major} | sed -e 's/[^0-9]//g')

Summary:	Powerful, light-weight programming language
Name:		lua5.0
Version:	5.0.3
Release:	11
License:	MIT
URL:		https://www.lua.org/
Group:		Development/Other
Source0:	http://www.lua.org/ftp/lua-%{version}.tar.bz2
Patch0:		lua-config.patch
Patch1:		lua-lbaselib.patch
Patch2:		lua-default.patch
Patch3:		lua-soname.patch
# Provides:	lua = %{version}-%{release}

%description
Lua is a programming language originally designed for extending applications, 
but also frequently used as a general-purpose, stand-alone language. Lua
combines simple procedural syntax (similar to Pascal) with powerful data 
description constructs based on associative arrays and extensible semantics.
Lua is dynamically typed, interpreted from bytecodes, and has automatic memory
management, making it ideal for configuration, scripting, and rapid
prototyping. Lua is implemented as a small library of C functions, written in 
ANSI C, and compiles unmodified in all known platforms. The implementation
goals are simplicity, efficiency, portability, and low embedding cost.

%package -n	%{libname}
Summary:	Powerful, light-weight programming language
Group:		System/Libraries

%description -n	%{libname}
Lua is a programming language originally designed for extending applications,
but also frequently used as a general-purpose, stand-alone language. Lua
combines simple procedural syntax (similar to Pascal) with powerful data
description constructs based on associative arrays and extensible semantics.
Lua is dynamically typed, interpreted from bytecodes, and has automatic memory
management, making it ideal for configuration, scripting, and rapid
prototyping. Lua is implemented as a small library of C functions, written in
ANSI C, and compiles unmodified in all known platforms. The implementation
goals are simplicity, efficiency, portability, and low embedding cost.

This package includes the libraries.


%package -n	%{libname}-devel
Summary:	Powerful, light-weight programming language
Group:		Development/Other
Requires:	%{libname} = %{version}
# to have the same provides on all arches
Provides:	lua%{major}-devel = %{version}-%{release}
# conflict with other versions
Conflicts:	lua-devel

%description -n	%{libname}-devel
Lua is a programming language originally designed for extending applications,
but also frequently used as a general-purpose, stand-alone language. Lua
combines simple procedural syntax (similar to Pascal) with powerful data
description constructs based on associative arrays and extensible semantics.
Lua is dynamically typed, interpreted from bytecodes, and has automatic memory
management, making it ideal for configuration, scripting, and rapid
prototyping. Lua is implemented as a small library of C functions, written in
ANSI C, and compiles unmodified in all known platforms. The implementation
goals are simplicity, efficiency, portability, and low embedding cost.

This package contains the headers and development files for lua.


%package -n	%{libname}-devel-static
Summary:	Powerful, light-weight programming language
Group:		Development/Other
Requires:	%{libname}-devel = %{version}
# to have the same provides on all arches
Provides:	lua%{major}-devel-static = %{version}-%{release}
# conflict with other versions
Conflicts:	lua-devel-static

%description -n	%{libname}-devel-static
Lua is a programming language originally designed for extending applications,
but also frequently used as a general-purpose, stand-alone language. Lua
combines simple procedural syntax (similar to Pascal) with powerful data
description constructs based on associative arrays and extensible semantics.
Lua is dynamically typed, interpreted from bytecodes, and has automatic memory
management, making it ideal for configuration, scripting, and rapid
prototyping. Lua is implemented as a small library of C functions, written in
ANSI C, and compiles unmodified in all known platforms. The implementation
goals are simplicity, efficiency, portability, and low embedding cost.

This package contains the headers and development files for lua.


%prep
%setup -q -n lua-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0 -b .soname

%build

%ifarch x86_64
fpic="-fPIC"
%endif
%make MYCFLAGS="$RPM_OPT_FLAGS ${fpic}" MYLDFLAGS="%{?ldflags}"
make so

%install
rm -rf %{buildroot}

%makeinstall_std INSTALL_LIB=%buildroot%_libdir
install -d %{buildroot}%{_libdir}/lua/%{major}/
install -d %{buildroot}%{_datadir}/lua/%{major}/
install -m 755 lib/*.so.* %{buildroot}%{_libdir}/
cp -a lib/*.so %{buildroot}%{_libdir}/
install -m 644 lib/*.lua %{buildroot}%{_datadir}/lua/%{major}/

# for update-alternatives
mv %{buildroot}/%{_bindir}/lua %{buildroot}/%{_bindir}/lua%{major}
mv %{buildroot}/%{_bindir}/luac %{buildroot}/%{_bindir}/luac%{major}

# to avoid conflict with other versions
mv %{buildroot}/%{_mandir}/man1/lua.1 %{buildroot}/%{_mandir}/man1/lua%{major}.1
mv %{buildroot}/%{_mandir}/man1/luac.1 %{buildroot}/%{_mandir}/man1/luac%{major}.1

%post
/usr/sbin/update-alternatives --install %{_bindir}/lua lua %{_bindir}/lua%{major} %{alt_priority} --slave %{_bindir}/luac luac %{_bindir}/luac%{major}

%files
%doc COPYRIGHT HISTORY INSTALL MANIFEST README
%doc doc/*.html doc/*.gif
%{_bindir}/*
%dir %{_libdir}/lua
%{_libdir}/lua/%{major}
%{_datadir}/lua/%{major}/*.lua
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{libname}-devel
%{_includedir}/*
%{_libdir}/*.so

%files -n %{libname}-devel-static
%{_libdir}/*.a
