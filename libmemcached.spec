Name:      libmemcached
Summary:   Client library and command line tools for memcached server
Version:   0.28
Release:   2%{?dist}
License:   BSD
Group:     System Environment/Libraries
URL:       http://tangent.org/552/libmemcached.html
Source0:   http://download.tangent.org/libmemcached-%{version}.tar.gz

# Patch from upstream to disable hsieh hash (non free)
# http://hg.tangent.org/libmemcached/rev/0fc201158518
Patch0:    %{name}-hsieh.patch
# Temporary for above patch
BuildRequires: libtool

# checked during configure (for test suite)
BuildRequires: memcached

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
libmemcached is a C client library to the memcached server
(http://danga.com/memcached). It has been designed to be light on memory
usage, and provide full access to server side methods.

It also implements several command line tools:

memcat - Copy the value of a key to standard output.
memflush - Flush the contents of your servers.
memrm - Remove a key(s) from the server.
memstat - Dump the stats of your servers to standard output.
memslap - Generate testing loads on a memcached cluster.
memcp - Copy files to memcached servers.
memerror - Creates human readable messages from libmemcached error codes.


%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, 
you will need to install %{name}-devel.


%prep
%setup -q

%patch0 -p1 
%{__rm} -f libmemcached/hsieh_hash.c 

%{__mkdir} examples
%{__cp} -p tests/*.{c,cpp,h} examples/

# Temporary because of patched .m4 files
libtoolize --force
aclocal
automake --add-missing -Wno-portability
autoconf
autoheader


%build
%configure
%{__make} %{_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install  DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""


%check
# For documentation only:
# test suite cannot run in mock (same port use for memcache servers on all arch)
# All tests completed successfully
# diff output.res output.cmp fails but result depend on server version
#%{__make} test


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig
 

%files
%defattr (-,root,root,-) 
%doc AUTHORS COPYING README THANKS TODO ChangeLog
%{_bindir}/mem*
%exclude %{_libdir}/libmemcached.a
%exclude %{_libdir}/libmemcached.la
%{_libdir}/libmemcached.so.*
%{_mandir}/man1/mem*


%files devel
%defattr (-,root,root,-) 
%doc examples
%{_includedir}/libmemcached
%{_libdir}/libmemcached.so
%{_libdir}/pkgconfig/libmemcached.pc
%{_libdir}/libmemcached.so
%{_mandir}/man3/libmemcached*.3.gz
%{_mandir}/man3/memcached_*.3.gz


%changelog
* Fri May 01 2009 Remi Collet <Fedora@famillecollet.com> - 0.28-2
- add upstream patch to disable nonfree hsieh hash method

* Sat Apr 25 2009 Remi Collet <Fedora@famillecollet.com> - 0.28-1
- Initial RPM from Brian Aker spec
- create -devel subpackage
- add %%post %%postun %%check section

