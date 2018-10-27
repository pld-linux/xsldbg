#
# Conditional build:
%bcond_without	kde		# install KDE Docbook documentation

Summary:	XSLT stylesheets debugger
Summary(pl.UTF-8):	Odpluskiwacz styli XSLT
Name:		xsldbg
Version:	4.8.0
Release:	1
License:	GPL
Group:		Development/Debuggers
Source0:	http://downloads.sourceforge.net/xsldbg/%{name}-%{version}.tar.gz
# Source0-md5:	e9bf58a2f81c19279ddc9d686a464902
URL:		http://xsldbg.sourceforge.net/
BuildRequires:	Qt5Core-devel
BuildRequires:	docbook-dtd412-xml
%{?with_kde:BuildRequires: kf5-kdoctools}
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	perl-base
BuildRequires:	qt5-qmake
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.596
Requires:	desktop-file-utils
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xsldbg is debugger with interface similar to gdb, but used to debug
XSLT stylesheets.

It has three major modes of execution of stylesheets: run the whole
stylesheet; step to next xsl instruction; continue until next break
point is found, or stylesheet has restarted.

%description -l pl.UTF-8
xsldbg jest odpluskwiaczem z interfejsem podobnym do gdb, ale służącym
do odpluskwiania styli XSLT.

Ma trzy podstawowe tryby wykonywania styli: uruchomienie całości; krok
do następnej instrukcji xsl; kontynuacja do następnego punktu stopu
lub restartu stylu.

%package apidocs
Summary:	xsldbg KDE Docbook
Group:		Documentation
BuildArch:	noarch

%description apidocs
xsldbg KDE Docbook.

%prep
%setup -q

%build
qmake-qt5 \
	QMAKE_EXTRAS="CONFIG+=xsldbg_shortcut" \
	-r xsldbg.pro
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	KDEDOCS_ROOT=%{_kdedocdir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# fixup borked icons path
install -d $RPM_BUILD_ROOT%{_iconsdir}
mv $RPM_BUILD_ROOT{%{_prefix}/icons/*,%{_iconsdir}}

# KDEDOCS_ROOT override in makefile or qmake-qt5 does not work
install -d $RPM_BUILD_ROOT%{_kdedocdir}
mv $RPM_BUILD_ROOT{%{_docdir}/HTML/*,%{_kdedocdir}}

rm -r $RPM_BUILD_ROOT%{_docdir}/packages/xsldbg

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc README.md AUTHORS ChangeLog TODO
%attr(755,root,root) %{_bindir}/xsldbg
%{_mandir}/man1/xsldbg.1*
%{_desktopdir}/xsldbg.desktop
%{_iconsdir}/hicolor/*/apps/xsldbg_source.png

%if %{with kde}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/kde/HTML/en/xsldbg/index.cache.bz2
%endif
