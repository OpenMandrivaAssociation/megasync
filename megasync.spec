Name:           megasync
Version:        5.11.1.0
Release:        1
Summary:        Easy automated syncing between your computers and your MEGA Cloud Drive 
License:        MEGA LIMITED CODE LICENCE
URL:            https://mega.io/desktop
Source0:        https://github.com/meganz/MEGAsync/archive/v%{version}_Linux/MEGAsync-%{version}_Linux.tar.gz

BuildRequires:  pkgconfig(libcares)
BuildRequires:  pkgconfig(readline)
BuildRequires:  freeimage-devel
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(cryptopp)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(libmediainfo)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  cmake(Qt5LinguistTools)
#BuildRequires:  libqt5-qtbase-devel
#BuildRequires:  libqt5-qtdeclarative-devel
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Svg)
BuildRequires:  cmake(Qt5X11Extras)
BuildRequires:  pkgconfig(libsodium)
BuildRequires:  pkgconfig(libuv)
BuildRequires:  lsb-release
BuildRequires:  pkgconfig
BuildRequires:  python
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(zlib)

%description
- Sync your entire MEGA Cloud or selected folders with your computer so your MEGA stays up to date with the changes you make to your data on your computer and vice versa.

- Back up your computer with MEGA to automatically copy data to MEGA in real time and eliminate the risk of accidental data loss.

- Easily add, sort, search for, prioritise, pause, and cancel your uploads and downloads using our transfer manager.

%prep
%autosetup -n MEGAsync-5.11.1.0_Linux -p1
#mv src/MEGASync/mega/cmake/modules/packages/* src/MEGASync/mega/cmake/modules/

%build
%cmake -DBUILD_SHARED_LIBS:BOOL=OFF -DBUILD_STATIC_LIBS:BOOL=ON \
       -DENABLE_DESKTOP_APP_TESTS=OFF \
       -DENABLE_DESKTOP_UPDATE_GEN=OFF \
       -DUSE_PDFIUM=OFF \
       -DENABLE_ISOLATED_GFX=ON \
       -DENABLE_DESIGN_TOKENS_IMPORTER=OFF

%make_build

%install
%make_install -C build

mkdir -p  %{buildroot}%{_sysctldir}
echo "fs.inotify.max_user_watches = 524288" > %{buildroot}%{_sysctldir}/99-megasync-inotify-limit.conf

mkdir -p  %{buildroot}%{_udevrulesdir}
echo "SUBSYSTEM==\"block\", ATTRS{idDevtype}==\"partition\"" > %{buildroot}%{_udevrulesdir}/99-megasync-udev.rules

%preun
if [ "$1" == "1" ]; then
    killall -s SIGUSR1 megasync 2> /dev/null || true
else
    killall megasync 2> /dev/null || true
    username=$SUDO_USER 2> /dev/null || true
    # Check if the variable is empty (e.g. if the script is not executed with sudo)
    [ -z "$username" ] && username=$(whoami) 2> /dev/null || true
    su -c 'timeout 1 megasync --send-uninstall-event' $username 2> /dev/null || true
fi
sleep 2

%posttrans
# to restore dormant MEGAsync upon updates
killall -s SIGUSR2 megasync 2> /dev/null || true

%files
%license LICENCE.md
%doc README.md CREDITS.md
%{_bindir}/%{name}
%{_bindir}/mega-desktop-app-gfxworker
%{_datadir}/applications/megasync.desktop
%dir %{_datadir}/icons/hicolor
%dir %{_datadir}/icons/hicolor/16x16
%dir %{_datadir}/icons/hicolor/16x16/apps
%dir %{_datadir}/icons/hicolor/256x256
%dir %{_datadir}/icons/hicolor/256x256/apps
%dir %{_datadir}/icons/hicolor/48x48
%dir %{_datadir}/icons/hicolor/48x48/apps
%dir %{_datadir}/icons/hicolor/scalable
%dir %{_datadir}/icons/hicolor/scalable/status
%dir %{_datadir}/icons/ubuntu-mono-dark
%dir %{_datadir}/icons/ubuntu-mono-dark/status
%dir %{_datadir}/icons/ubuntu-mono-dark/status/24
%{_datadir}/icons/hicolor/*/*/mega.png
%{_datadir}/icons/*/*/*/*
%dir %{_sysctldir}
%{_sysctldir}/99-megasync-inotify-limit.conf
%dir %{_udevrulesdir}
%{_udevrulesdir}/99-megasync-udev.rules
