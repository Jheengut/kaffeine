# TODO
# - kaffeine-mozilla-0.2.tar.bz2 (Starter-Plugin for Mozilla)
# - check: http://kaffeine.sourceforge.net/index.php?page=faq#question4
Summary:	A KDE xine frontend
Summary(pl):	Frontend do xine pod KDE
Name:		kaffeine
Version:	0.7
Release:	0.1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/kaffeine/%{name}-%{version}.tar.bz2
# Source0-md5:	6b887a80af11a9a252bd3c1524ef31f5
Patch0:		%{name}-win32-path.patch
Patch1:		%{name}-locale_names.patch
Patch2:		%{name}-desktop.patch
URL:		http://kaffeine.sourceforge.net/
BuildRequires:	automake
BuildRequires:	kdelibs-devel >= 3.1
BuildRequires:	rpmbuild(macros) >= 1.122
BuildRequires:	xine-lib-devel >= 1:1.0
Requires:	kdebase-core >= 9:3.1.90
Requires:	kdelibs >= 9:3.4.0-4
Requires:	xine-lib >= 1:1.0
Requires:	libdvdcss
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A powerful, fully integrated with KDE xine GUI.

%description -l pl
W pe�ni zintegrowany z KDE frontend do xine.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
mv -f po/{pt_PT,pt}.po

%build
cp /usr/share/automake/config.sub admin

%{__make} -f admin/Makefile.common

%configure \
	--disable-rpath \
	--with-qt-libraries=%{_libdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir}

# no devel libraries, why did these get installed?
rm -r $RPM_BUILD_ROOT%{_includedir}/%{name}
rm $RPM_BUILD_ROOT%{_includedir}/%{name}_export.h

rm $RPM_BUILD_ROOT/%{_datadir}/mimelnk/application/x-mplayer2.desktop

%find_lang %{name} --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kaffeine
%attr(755,root,root) %{_libdir}/libkmediapart.so.0.0.1
%{_libdir}/libkmediapart.la
%attr(755,root,root) %{_libdir}/kde3/libkaffeinepart.so
%attr(755,root,root) %{_libdir}/kde3/libgstreamerpart.so
%{_libdir}/kde3/libkaffeinepart.la
%{_libdir}/kde3/libgstreamerpart.la
%{_datadir}/apps/kaffeine
%{_datadir}/apps/konqueror/servicemenus/*
%{_datadir}/apps/profiles/kaffeine.profile.xml
# FIXME: move to kdelibs the directory?
%dir %{_datadir}/apps/gstreamerpart
%{_datadir}/apps/gstreamerpart/gstreamer_part.rc
%{_datadir}/mimelnk/application/*.desktop
%{_datadir}/services/kaffeine_part.desktop
%{_datadir}/services/gstreamer_part.desktop
%{_desktopdir}/kde/kaffeine.desktop
%{_iconsdir}/[!l]*/*/*/*.png
%{_mandir}/man1/kaffeine.1*
%lang(de) %{_mandir}/de/man1/kaffeine.1*
