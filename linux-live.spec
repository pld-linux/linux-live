Summary:	Linux Live scripts
Summary(pl):	Skrypty Linux Live
Name:		linux-live
Version:	5.5.0
Release:	1.3
License:	GPL
Group:		Applications/System
Source0:	http://www.linux-live.org/dl/%{name}-%{version}.tar.gz
# Source0-md5:	6a59f1ecf30780f8b3facd5dfcb01f13
Patch0:		%{name}-fixes.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-modprobe.patch
Patch3:		%{name}-modules.patch
URL:		http://www.linux-live.org/
BuildRequires:	busybox-initrd
BuildRequires:	e2fsprogs
BuildRequires:	eject
BuildRequires:	unionfs
Requires:	squashfs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir	%{_prefix}/lib
%define		_libexecdir	%{_libdir}/%{name}

%description
Linux Live is a set of shell scripts which allows you to create own
LiveCD from every Linux distribution. Just install your favourite
distro, remove all unnecessary files (for example man pages and all
other files which are not important for you) and then download and run
these scripts to build your custom Live Linux.

%description -l pl
Linux Live to zestaw skryptów pow³oki pozwalaj±cych tworzyæ w³asne
LiveCD z ka¿dej dystrybucji Linuksa. Wystarczy zainstalowaæ ulubion±
dystrybucjê, usun±æ wszystkie niepotrzebne pliki (na przyk³ad strony
manuala i wszystkie inne nieistotne dla nas pliki), a nastêpnie
¶ci±gn±æ i uruchomiæ te skrypty, aby stworzyæ w³asnego Live Linuksa.

%package build
Summary:	Linux Live build scripts
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description build
Scripts to build your livecd with Linux Live scripts.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

rm -rf initrd/kernel-modules/2.6.16
find . '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
# tools for livecd
install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_sbindir}}
cp -a tools/liblinuxlive $RPM_BUILD_ROOT%{_libdir}
cp -a tools/{deb2mo,dir2mo,img2mo,mo2dir,tgz2mo} $RPM_BUILD_ROOT%{_bindir}
cp -a tools/uselivemod $RPM_BUILD_ROOT%{_sbindir}

# tools for building livecd
install -d $RPM_BUILD_ROOT%{_libexecdir}
cp -a cd-root $RPM_BUILD_ROOT%{_libexecdir}
cp -a runme.sh $RPM_BUILD_ROOT%{_libexecdir}

# initrd
install -d $RPM_BUILD_ROOT%{_libexecdir}/initrd
cp -a initrd/{cleanup,initrd_create,linuxrc} $RPM_BUILD_ROOT%{_libexecdir}
ln -s %{_libdir}/liblinuxlive $RPM_BUILD_ROOT%{_libexecdir}/initrd
# copy /bin
install -d $RPM_BUILD_ROOT%{_libexecdir}/initrd/rootfs/bin
cp -a /bin/initrd-busybox $RPM_BUILD_ROOT%{_libexecdir}/initrd/rootfs/bin/busybox
cp -a /sbin/blkid $RPM_BUILD_ROOT%{_libexecdir}/initrd/rootfs/bin
cp -a %{_bindir}/eject $RPM_BUILD_ROOT%{_libexecdir}/initrd/rootfs/bin
cp -a initrd/rootfs/bin/modprobe $RPM_BUILD_ROOT%{_libexecdir}/initrd/rootfs/bin
cp -a %{_sbindir}/unionctl $RPM_BUILD_ROOT%{_libexecdir}/initrd/rootfs/bin
cp -a %{_sbindir}/uniondbg $RPM_BUILD_ROOT%{_libexecdir}/initrd/rootfs/bin
install -d $RPM_BUILD_ROOT%{_libexecdir}/initrd/rootfs/lib
# /%{_lib}
%if "%{_lib}" != "lib"
ln -s lib $RPM_BUILD_ROOT%{_libexecdir}/initrd/rootfs/%{_lib}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/deb2mo
%attr(755,root,root) %{_bindir}/dir2mo
%attr(755,root,root) %{_bindir}/img2mo
%attr(755,root,root) %{_bindir}/mo2dir
%attr(755,root,root) %{_bindir}/tgz2mo
%attr(755,root,root) %{_sbindir}/uselivemod
%{_libdir}/liblinuxlive

%files build
%defattr(644,root,root,755)
%doc DOC/changelog.txt DOC/requirements.txt
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/runme.sh
%attr(755,root,root) %{_libexecdir}/cleanup
%attr(755,root,root) %{_libexecdir}/initrd_create
%{_libexecdir}/linuxrc
%{_libexecdir}/cd-root
%{_libexecdir}/initrd
