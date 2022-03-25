#
# Conditional build:
%bcond_without	python3		# Python 3 binding
%bcond_without	readline	# readline in interactive programs
#
Summary:	Helsinki Finite-State Transducer (library and application suite)
Summary(pl.UTF-8):	Helsinki Finite-State Transducer (biblioteka i zestaw aplikacji)
Name:		hfst
Version:	3.15.1
Release:	5
License:	LGPL v3 (library), GPL v3 (tools)
Group:		Applications/Text
#Source0Download: https://github.com/hfst/hfst/releases
Source0:	https://github.com/hfst/hfst/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	31b046a2c42c5f169dd1a973b82677f4
Patch0:		%{name}-pc.patch
Patch1:		build.patch
Patch2:		%{name}-python3.patch
URL:		http://www.ling.helsinki.fi/kieliteknologia/tutkimus/hfst/
# bundled library is used
#BuildRequires:	SFST-devel
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.12
BuildRequires:	bison
BuildRequires:	flex >= 2.5.35
BuildRequires:	glib2-devel >= 1:2.16
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.2
# disabled in sources
#BuildRequires:	libxml2-devel >= 2
BuildRequires:	ncurses-devel
# bundled library is used
#BuildRequires:	openfst-devel
BuildRequires:	pkgconfig >= 1:0.14
BuildRequires:	python >= 1:2.4
%{?with_python3:BuildRequires:	python3 >= 1:3.2}
%{?with_readline:BuildRequires:	readline-devel}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%{?with_python3:BuildRequires:	swig-python}
BuildRequires:	zlib-devel
Requires:	glib2 >= 1:2.16
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

%package tagger
Summary:	HFST Tagger scripts
Summary(pl.UTF-8):	Skrypty HFST Tagger
License:	GPL v3
Group:		Applications/Text
Requires:	%{name} = %{version}-%{release}

%description tagger
HFST Tagger scripts written in Python.

%description tagger -l pl.UTF-8
Skrypty HFST Tagger napisane w Pythonie.

%package devel
Summary:	Header files for HFST library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki HFST
License:	LGPL v3
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
#Requires:	SFST-devel
Requires:	glib2-devel >= 1:2.16
Requires:	libstdc++-devel
#Requires:	openfst-devel
Requires:	readline-devel

%description devel
Header files for HFST library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki HFST.

%package static
Summary:	Static HFST library
Summary(pl.UTF-8):	Statyczna biblioteka HFST
License:	LGPL v3
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static HFST library.

%description static -l pl.UTF-8
Statyczna biblioteka HFST.

%package -n python-hfst
Summary:	Python 2 binding for HFST library
Summary(pl.UTF-8):	Wiązanie Pythona 2 do biblioteki HFST
License:	LGPL v3
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-hfst
Python 2 binding for HFST library.

%description -n python-hfst -l pl.UTF-8
Wiązanie Pythona 2 do biblioteki HFST.

%package -n python3-hfst
Summary:	Python 3 binding for HFST library
Summary(pl.UTF-8):	Wiązanie Pythona 3 do biblioteki HFST
License:	LGPL v3
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-hfst
Python 3 binding for HFST library.

%description -n python3-hfst -l pl.UTF-8
Wiązanie Pythona 3 do biblioteki HFST.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-calculate \
	--enable-foma-wrapper \
	--enable-lexc \
	--enable-lexc-wrapper \
	--enable-proc \
	--disable-silent-rules \
	--enable-tagger \
	--enable-train-tagger \
	--enable-xfst \
	%{?with_readline:--with-readline} \
	--with-unicode-handler=glib

# parallel build is broken with foma backend
%{__make} -j1

cd python
%py_build
%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkgconfig
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libhfst.la

# for transducer data
install -d $RPM_BUILD_ROOT%{_datadir}/hfst

cd python
%py_install
%py_postclean
%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README THANKS
%attr(755,root,root) %{_bindir}/hfst-*
%attr(755,root,root) %{_bindir}/hfst_foma
%attr(755,root,root) %{_libdir}/libhfst.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhfst.so.52
%dir %{_datadir}/hfst
%{_mandir}/man1/hfst-*.1*

%files tagger
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hfst_tagger_compute_data_statistics.py
%{py3_sitescriptdir}/hfst_tagger_compute_data_statistics.py
%{py3_sitescriptdir}/tagger_aux.py
%{py3_sitescriptdir}/__pycache__/hfst_tagger_compute_data_statistics.cpython-*.py[co]
%{py3_sitescriptdir}/__pycache__/tagger_aux.cpython-*.py[co]
%{_mandir}/man1/hfst_tagger_compute_data_statistics.py.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhfst.so
%{_includedir}/hfst
%{_aclocaldir}/hfst.m4
%{_pkgconfigdir}/hfst.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libhfst.a

%files -n python-hfst
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_libhfst.so
%{py_sitedir}/hfst
%{py_sitedir}/libhfst.py[co]
%{py_sitedir}/libhfst_swig-%{version}_beta-py*.egg-info

%if %{with python3}
%files -n python3-hfst
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_libhfst.cpython-*.so
%{py3_sitedir}/hfst
%{py3_sitedir}/libhfst.py
%{py3_sitedir}/__pycache__/libhfst.cpython-*.py[co]
%{py3_sitedir}/libhfst_swig-%{version}_beta-py*.egg-info
%endif
