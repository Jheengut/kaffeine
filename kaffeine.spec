# TODO
# - kaffeine-mozilla-0.2.tar.bz2 (Starter-Plugin for Mozilla)
# - check: http://kaffeine.sourceforge.net/index.php?page=faq#question4
#
# Conditional build:
%bcond_without	gstreamer	# build without gstreamer part
#
Summary:	Full featured Multimedia-Player for KDE
Summary(pl.UTF-8):	Frontend do xine pod KDE
Name:		kaffeine
Version:	0.8.6
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/kaffeine/%{name}-%{version}.tar.bz2
# Source0-md5:	102cced6a686f5ffffee94652ca2a093
Patch0:		%{name}-win32-path.patch
Patch1:		%{name}-desktop.patch
Patch2:		kde-ac260-lt.patch
URL:		http://kaffeine.sourceforge.net/
BuildRequires:	automake
BuildRequires:	cdparanoia-III-devel
BuildRequires:	kdelibs-devel >= 9:3.2.0
BuildRequires:	lame-libs-devel
BuildRequires:	rpmbuild(macros) >= 1.122
BuildRequires:	xine-lib-devel >= 2:1.1.9
%if %{with gstreamer}
BuildRequires:	gstreamer-plugins-base-devel >= 0.10
Requires:	gstreamer >= 0.10
%endif
Requires:	kdebase-core >= 9:3.2.0
Requires:	libdvdcss
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kaffeine is a full featured Multimedia-Player for KDE. By default it
uses xine as backend.

%description -l pl.UTF-8
W pełni zintegrowany z KDE frontend do xine.

%prep
%setup -q
%patch0 -p1
#%patch1 -p1
%patch2 -p1

%build
cp -f /usr/share/automake/config.sub admin
%{__make} -f admin/Makefile.common
%configure \
	--disable-rpath \
	--with-qt-libraries=%{_libdir} \
	--with%{!?with_gstreamer:out}-gstreamer
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir}

# no devel libraries, why did these get installed?
rm -r $RPM_BUILD_ROOT%{_includedir}/%{name}

rm $RPM_BUILD_ROOT%{_datadir}/mimelnk/application/x-mplayer2.desktop
# only for translators
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/xx

# pick docs
%find_lang %{name} --with-kde
# second try. pic locale files
# FIXME: remove version?
%find_lang %{name}-%{version} --with-kde
cat  %{name}-%{version}.lang >> %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kaffeine
%attr(755,root,root) %{_libdir}/libkaffeineaudioencoder.so.0.0.1
%attr(755,root,root) %{_libdir}/kde3/libkaffeinemp3lame.so
%attr(755,root,root) %{_libdir}/kde3/libkaffeineoggvorbis.so
%{_datadir}/apps/kaffeine
%{_datadir}/apps/konqueror/servicemenus/*
%{_datadir}/apps/profiles/kaffeine.profile.xml
%{_datadir}/mimelnk/application/*.desktop
%{_datadir}/services/kaffeinemp3lame.desktop
%{_datadir}/services/kaffeineoggvorbis.desktop
%{_datadir}/servicetypes/kaffeineaudioencoder.desktop
%{_desktopdir}/kde/kaffeine.desktop
%{_iconsdir}/[!l]*/*/*/*.png
%attr(755,root,root) %{_libdir}/kde3/libxinepart.so
%attr(755,root,root) %{_libdir}/libkaffeinedvbplugin.so.0.0.1
%attr(755,root,root) %{_libdir}/libkaffeineepgplugin.so.0.0.1
%attr(755,root,root) %{_libdir}/libkaffeinepart.so
%{_datadir}/services/xine_part.desktop
%{_datadir}/servicetypes/kaffeinedvbplugin.desktop
%{_datadir}/servicetypes/kaffeineepgplugin.desktop

# gstreamer part
%if %{with gstreamer}
%attr(755,root,root) %{_libdir}/kde3/libgstreamerpart.so
%dir %{_datadir}/apps/gstreamerpart
%{_datadir}/apps/gstreamerpart/gstreamer_part.rc
%{_datadir}/services/gstreamer_part.desktop
%endif
