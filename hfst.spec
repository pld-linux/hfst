#
# Conditional build:
%bcond_with	foma	# use foma by linking with libfoma (GPL v2-strict, which is not compliant)
#
Summary:	Helsinki Finite-State Transducer (library and application suite)
Summary(pl.UTF-8):	Helsinki Finite-State Transducer (biblioteka i zestaw aplikacji)
Name:		hfst
Version:	3.0.2
Release:	1
License:	GPL v3
Group:		Applications/Text
Source0:	http://downloads.sourceforge.net/hfst/%{name}-%{version}.tar.gz
# Source0-md5:	ae502571684f706b372d669c36652892
Patch0:		%{name}-pc.patch
URL:		http://www.ling.helsinki.fi/kieliteknologia/tutkimus/hfst/
BuildRequires:	SFST-devel
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	bison
%{?with_foma:BuildRequires:	foma-devel}
BuildRequires:	flex >= 2.5.35
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.0
BuildRequires:	openfst-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Helsinki Finite-State Transducer software is intended for the
implementation of morphological analysers and other tools which are
based on weighted and unweigted finite-state transducer technology.

%description -l pl.UTF-8
Pakiet HFST (Helsinki Finite-State Transducer) to oprogramowanie
służące do implementacji analizatorów morfologicznych i innych
narzędzi opartych na technice przetwarzania ze skończoną liczbą
stanów z wagami lub bez.

%package devel
Summary:	Header files for HFST library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki HFST
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	SFST-devel
%{?with_foma:Requires:	foma-devel}
Requires:	libstdc++-devel
Requires:	openfst-devel

%description devel
Header files for HFST library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki HFST.

%package static
Summary:	Static HFST library
Summary(pl.UTF-8):	Statyczna biblioteka HFST
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static HFST library.

%description static -l pl.UTF-8
Statyczna biblioteka HFST.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	FOMACLI=/usr/bin/foma \
	--disable-silent-rules \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# missing in make install
[ ! -f $RPM_BUILD_ROOT%{_pkgconfigdir}/hfst.pc ] || exit 1
install -D libhfst/hfst.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/hfst.pc

# obsoleted by pkgconfig
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libhfst.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS
%attr(755,root,root) %{_bindir}/hfst-*
%attr(755,root,root) %{_bindir}/htwolcpre*
%attr(755,root,root) %{_libdir}/libhfst.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhfst.so.1
%{_mandir}/man1/hfst-*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhfst.so
%{_includedir}/hfst
%{_pkgconfigdir}/hfst.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libhfst.a
