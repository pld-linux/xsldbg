Summary:	XSLT stylesheets debugger
Summary(pl):	Odpluskiwacz styli XSLT
Name:		xsldbg
Version:	2.1.8
Release:	1
License:	GPL
Group:		Development/Debuggers
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	f9a4a5b834d874afacf35b15cc17ccb1
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-no-static.patch
Patch2:		%{name}-docpath.patch
URL:		http://xsldbg.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	docbook-dtd412-xml
BuildRequires:	libtool
BuildRequires:	libxslt-devel
BuildRequires:	perl-base
BuildRequires:	readline-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xsldbg is debugger with interface similar to gdb, but used to debug
XSLT stylesheets.

It has three major modes of execution of stylesheets: run the whole
stylesheet; step to next xsl instruction; continue until next break
point is found, or stylesheet has restarted.

%description -l pl
xsldbg jest odpluskwiaczem z interfejsem podobnym do gdb, ale s³u¿±cym
do odpluskwiania styli XSLT.

Ma trzy podstawowe tryby wykonywania styli: uruchomienie ca³o¶ci; krok
do nastêpnej instrukcji xsl; kontynuacja do nastêpnego punktu stopu
lub restartu stylu.

%package devel
Summary:	Headers for %{name}
Summary(pl):	Pliki nag³ówkowe dla %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Headers and libraries for %{name}. You don't need them, unless you
want to develop frontends to %{name}.

%description devel -l pl
Pliki nag³ówkowe dla %{name}. Nie potrzebujesz ich, chyba, ¿e chcesz
pisaæ nak³adki na %{name}.

%package static
Summary:	Static libraries for %{name}
Summary(pl):	Statyczne biblioteki dla %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static libraries for %{name}. You don't need them, unless you want to
develop frontends to %{name}.

%description static -l pl
Statyczne biblioteki dla %{name}. Nie potrzebujesz ich, chyba, ¿e
chcesz pisaæ nak³adki na %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
autoupdate
%{__automake}
%{__autoconf}
# if anybody is intrested in KDE/GNOME docs, feel free to change it ;)
%configure \
	--disable-kde-docs \
	--disable-gnome-docs \
	--enable-docs-macro \
	--with-html-dir=%{_docdir}/%{name}-%{version}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog TODO
%doc docs/en/plain/index.html docs/en/xsldoc.{dtd,xml,xsl}
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_bindir}/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
