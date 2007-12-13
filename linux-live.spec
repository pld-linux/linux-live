Summary:	Linux Live scripts
Summary(pl.UTF-8):	Skrypty Linux Live
Name:		linux-live
Version:	6.1.5
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.slax.org/Linux-Live/%{name}-%{version}.tar.gz
# Source0-md5:	9d3639408907a7b98012e0bdcff9c0d1
Patch0:		%{name}-fixes.patch
Patch1:		%{name}-package.patch
URL:		http://www.linux-live.org/
Requires:	squashfs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir	%{_prefix}/lib
%define		_libexecdir	%{_libdir}/%{name}
%define		_sysconfdir	/etc/%{name}
%define		__cp	cp --preserve=timestamps

%description
Linux Live is a set of shell scripts which allows you to create own
LiveCD from every Linux distribution. Just install your favourite
distro, remove all unnecessary files (for example man pages and all
other files which are not important for you) and then download and run
these scripts to build your custom Live Linux.

%description -l pl.UTF-8
Linux Live to zestaw skryptów powłoki pozwalających tworzyć własne
LiveCD z każdej dystrybucji Linuksa. Wystarczy zainstalować ulubioną
dystrybucję, usunąć wszystkie niepotrzebne pliki (na przykład strony
manuala i wszystkie inne nieistotne dla nas pliki), a następnie
ściągnąć i uruchomić te skrypty, aby stworzyć własnego Live Linuksa.

%package build
Summary:	Linux Live build scripts
Summary(pl.UTF-8):	Skrypty do tworzenia Linux Live
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	busybox
Requires:	coreutils
Requires:	e2fsprogs
Requires:	eject
Requires:	grep
Requires:	mawk
Requires:	mkisofs
Requires:	pci-database
Requires:	sed
Requires:	unionfs

%description build
Scripts to build your livecd with Linux Live scripts.

%description build -l pl.UTF-8
Skrypty do tworzenia własnego livecd przy użyciu skryptów Linux Live.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

rm -rf initrd/kernel-modules/2.6.16
find . '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
# tools for livecd
install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_sbindir}}
%{__cp} -p tools/liblinuxlive $RPM_BUILD_ROOT%{_libdir}
%{__cp} -a tools/{deb2mo,dir2mo,img2mo,mo2dir,tgz2mo} $RPM_BUILD_ROOT%{_bindir}
%{__cp} -a tools/uselivemod $RPM_BUILD_ROOT%{_sbindir}

# tools for building livecd
install -d $RPM_BUILD_ROOT%{_sysconfdir}
%{__cp} config $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT%{_libexecdir}
%{__cp} -a cd-root $RPM_BUILD_ROOT%{_libexecdir}
%{__cp} runme.sh $RPM_BUILD_ROOT%{_libexecdir}
%{__cp} -a DOC $RPM_BUILD_ROOT%{_libexecdir}

# initrd
install -d $RPM_BUILD_ROOT%{_libexecdir}/initrd
%{__cp} -p initrd/{cleanup,initrd_create,linuxrc} $RPM_BUILD_ROOT%{_libexecdir}/initrd
ln -s %{_libdir}/liblinuxlive $RPM_BUILD_ROOT%{_libexecdir}/initrd
# copy /bin
install -d $RPM_BUILD_ROOT%{_libexecdir}/initrd/rootfs/bin
%{__cp} initrd/rootfs/bin/modprobe $RPM_BUILD_ROOT%{_libexecdir}/initrd/rootfs/bin
install -d $RPM_BUILD_ROOT%{_libexecdir}/initrd/rootfs/lib

# avoid autodeps
# FIXME: how to copy file without preserving +x bit?
chmod -x $RPM_BUILD_ROOT%{_libexecdir}/initrd/rootfs/bin/modprobe
chmod -x $RPM_BUILD_ROOT%{_libexecdir}/initrd/initrd_create
chmod -x $RPM_BUILD_ROOT%{_libdir}/liblinuxlive

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
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config
%dir %{_libexecdir}
%{_libexecdir}/DOC
%attr(755,root,root) %{_libexecdir}/runme.sh
%dir %{_libexecdir}/cd-root
%{_libexecdir}/cd-root/boot
%{_libexecdir}/cd-root/tools
%{_libexecdir}/cd-root/filelist.txt
%{_libexecdir}/cd-root/isolinux.cfg
%{_libexecdir}/cd-root/livecd.sgn
%{_libexecdir}/cd-root/*.bat
%attr(755,root,root) %{_libexecdir}/cd-root/*.sh
%dir %{_libexecdir}/initrd
%{_libexecdir}/initrd/linuxrc
%attr(755,root,root) %{_libexecdir}/initrd/cleanup
%attr(755,root,root) %{_libexecdir}/initrd/initrd_create
%dir %{_libexecdir}/initrd/rootfs
%dir %{_libexecdir}/initrd/rootfs/bin
%attr(755,root,root) %{_libexecdir}/initrd/rootfs/bin/modprobe
