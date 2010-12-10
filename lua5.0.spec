%define	major	5.0
%define	libname %mklibname lua %{major}
%define alt_priority %(echo %{major} | sed -e 's/[^0-9]//g')

Summary:	Powerful, light-weight programming language
Name:		lua5.0
Version:	5.0.3
Release:	%mkrel 10
License:	MIT
URL:		http://www.lua.org/
Group:		Development/Other
Source0:	http://www.lua.org/ftp/lua-%{version}.tar.bz2
Patch0:		lua-config.patch
Patch1:		lua-lbaselib.patch
Patch2:		lua-default.patch
Patch3:		lua-soname.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
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
rm -rf $RPM_BUILD_ROOT

%makeinstall_std INSTALL_LIB=%buildroot%_libdir
install -d $RPM_BUILD_ROOT%{_libdir}/lua/%{major}/
install -d $RPM_BUILD_ROOT%{_datadir}/lua/%{major}/
install -m 755 lib/*.so.* $RPM_BUILD_ROOT%{_libdir}/
cp -a lib/*.so $RPM_BUILD_ROOT%{_libdir}/
install -m 644 lib/*.lua $RPM_BUILD_ROOT%{_datadir}/lua/%{major}/

# for update-alternatives
mv $RPM_BUILD_ROOT/%{_bindir}/lua $RPM_BUILD_ROOT/%{_bindir}/lua%{major}
mv $RPM_BUILD_ROOT/%{_bindir}/luac $RPM_BUILD_ROOT/%{_bindir}/luac%{major}

# to avoid conflict with other versions
mv $RPM_BUILD_ROOT/%{_mandir}/man1/lua.1 $RPM_BUILD_ROOT/%{_mandir}/man1/lua%{major}.1
mv $RPM_BUILD_ROOT/%{_mandir}/man1/luac.1 $RPM_BUILD_ROOT/%{_mandir}/man1/luac%{major}.1

%clean
rm -rf $RPM_BUILD_ROOT


%post
/usr/sbin/update-alternatives --install %{_bindir}/lua lua %{_bindir}/lua%{major} %{alt_priority} --slave %{_bindir}/luac luac %{_bindir}/luac%{major}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%postun
[[ -f %_bindir/lua%{major} ]] || /usr/sbin/update-alternatives --remove lua %{_bindir}/lua%{major}

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr (-,root,root)
%doc COPYRIGHT HISTORY INSTALL MANIFEST README
%doc doc/*.html doc/*.gif
%{_bindir}/*
%dir %{_libdir}/lua
%{_libdir}/lua/%{major}
%{_datadir}/lua/%{major}/*.lua
%{_mandir}/man1/*

%files -n %{libname}
%defattr (-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr (-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a

%files -n %{libname}-devel-static
%defattr (-,root,root)
%{_libdir}/*.a

