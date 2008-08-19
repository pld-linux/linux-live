# TODO:
# - generate initramfs image instead of ext2 (our kernels don't support ext2 anyway)
Summary:	Linux Live scripts
Summary(pl.UTF-8):	Skrypty Linux Live
Name:		linux-live
Version:	6.2.4
Release:	2
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.slax.org/Linux-Live/%{name}-%{version}.tar.gz
# Source0-md5:	1d14e9323bb98ef5621e0c7f7755cbd0
Source1:	%{name}-build.sh
Patch0:		%{name}-package.patch
URL:		http://www.linux-live.org/
Requires:	squashfs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir	%{_prefix}/lib
%define		_libexecdir	%{_libdir}/%{name}
%define		_sysconfdir	/etc/%{name}
%define		__cp	cp --preserve=timestamps

# do not touch initrd files
%define		_noautostrip	.*/cd-root/.*

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

%description build
Scripts to build your livecd with Linux Live scripts.

%description build -l pl.UTF-8
Skrypty do tworzenia własnego livecd przy użyciu skryptów Linux Live.

%prep
%setup -q
%patch0 -p1

rm -rf initrd/kernel-modules/2.6.16
find . '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
# tools for livecd
install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_sbindir}}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/linux-live-build
%{__cp} -p tools/liblinuxlive $RPM_BUILD_ROOT%{_libdir}
%{__cp} -a tools/{deb2lzm,dir2lzm,lzm2dir,tgz2lzm} $RPM_BUILD_ROOT%{_bindir}

# tools for building livecd
install -d $RPM_BUILD_ROOT%{_sysconfdir}
%{__cp} .config $RPM_BUILD_ROOT%{_sysconfdir}/config
install -d $RPM_BUILD_ROOT%{_libexecdir}
%{__cp} -a cd-root $RPM_BUILD_ROOT%{_libexecdir}
%{__cp} build $RPM_BUILD_ROOT%{_libexecdir}
%{__cp} install $RPM_BUILD_ROOT%{_libexecdir}
%{__cp} -a DOC $RPM_BUILD_ROOT%{_libexecdir}

# initrd
install -d $RPM_BUILD_ROOT%{_libexecdir}/initrd
%{__cp} -p initrd/{addlocaleslib,cleanup,initrd_create,linuxrc,upd-rootfs} $RPM_BUILD_ROOT%{_libexecdir}/initrd
%{__cp} -a initrd/{fuse,ntfs-3g,posixovl,rootfs} $RPM_BUILD_ROOT%{_libexecdir}/initrd
ln -s %{_libdir}/liblinuxlive $RPM_BUILD_ROOT%{_libexecdir}/initrd
ln -sf ntfs-3g $RPM_BUILD_ROOT%{_libexecdir}/initrd/ntfs-3g/usr/bin/mount.ntfs-3g

# avoid autodeps
# FIXME: how to copy file without preserving +x bit?
chmod -R -x+X $RPM_BUILD_ROOT%{_libexecdir}/initrd/
chmod -x $RPM_BUILD_ROOT%{_libdir}/liblinuxlive

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/deb2lzm
%attr(755,root,root) %{_bindir}/dir2lzm
%attr(755,root,root) %{_bindir}/lzm2dir
%attr(755,root,root) %{_bindir}/tgz2lzm
%{_libdir}/liblinuxlive

%files build
%defattr(644,root,root,755)
%doc DOC/changelog.txt DOC/requirements.txt
%attr(755,root,root) %{_sbindir}/linux-live-build
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config
%dir %{_libexecdir}
%{_libexecdir}/DOC
%attr(755,root,root) %{_libexecdir}/build
%attr(755,root,root) %{_libexecdir}/install
%dir %{_libexecdir}/cd-root
%{_libexecdir}/cd-root/boot
%{_libexecdir}/cd-root/linux
%dir %{_libexecdir}/initrd
%{_libexecdir}/initrd/liblinuxlive
%{_libexecdir}/initrd/linuxrc
%attr(755,root,root) %{_libexecdir}/initrd/addlocaleslib
%attr(755,root,root) %{_libexecdir}/initrd/cleanup
%attr(755,root,root) %{_libexecdir}/initrd/initrd_create
%attr(755,root,root) %{_libexecdir}/initrd/upd-rootfs
%dir %{_libexecdir}/initrd/fuse
%dir %{_libexecdir}/initrd/fuse/usr
%dir %{_libexecdir}/initrd/fuse/usr/bin
%attr(755,root,root) %{_libexecdir}/initrd/fuse/usr/bin/*
%dir %{_libexecdir}/initrd/fuse/usr/lib
%attr(755,root,root) %{_libexecdir}/initrd/fuse/usr/lib/*.so*
%dir %{_libexecdir}/initrd/ntfs-3g
%dir %{_libexecdir}/initrd/ntfs-3g/usr
%dir %{_libexecdir}/initrd/ntfs-3g/usr/bin
%attr(755,root,root) %{_libexecdir}/initrd/ntfs-3g/usr/bin/*
%dir %{_libexecdir}/initrd/ntfs-3g/usr/lib
%attr(755,root,root) %{_libexecdir}/initrd/ntfs-3g/usr/lib/*.so*
%dir %{_libexecdir}/initrd/posixovl
%dir %{_libexecdir}/initrd/posixovl/usr
%dir %{_libexecdir}/initrd/posixovl/usr/bin
%attr(755,root,root) %{_libexecdir}/initrd/posixovl/usr/bin/*
%dir %{_libexecdir}/initrd/rootfs
%dir %{_libexecdir}/initrd/rootfs/bin
%attr(755,root,root) %{_libexecdir}/initrd/rootfs/bin/*
%{_libexecdir}/initrd/rootfs/etc
%dir %{_libexecdir}/initrd/rootfs/lib
%attr(755,root,root) %{_libexecdir}/initrd/rootfs/lib/*.so*
%{_libexecdir}/initrd/rootfs/usr
