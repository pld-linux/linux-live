Summary:	Linux Live Kit
Name:		linux-live
Version:	1.8
Release:	0.1
Epoch:		1
License:	GPL
Group:		Applications/System
Source0:	https://github.com/Tomas-M/linux-live/archive/v%{version}.tar.gz?/%{name}-%{version}.tgz
# Source0-md5:	393c52991be3e4d21660e00b6bbf316c
Source1:	http://www.kernel.org/pub/linux/utils/boot/syslinux/syslinux-4.06.tar.gz
# Source1-md5:	ab705f8a0be0598770014bd5498b2eb2
Source2:	%{name}-build.sh
Patch0:		pld.patch
Patch1:		https://github.com/Tomas-M/linux-live/pull/5.patch
# Patch1-md5:	603c98f4c516929044bccf0419423586
URL:		http://www.linux-live.org/
BuildRequires:	libuuid-devel
BuildRequires:	nasm
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.583
BuildRequires:	upx
Requires:	coreutils
Requires:	grep
Requires:	mawk
Requires:	mkisofs
Requires:	sed
Requires:	squashfs
# suggests for rebuidling isolinux
Suggests:	gcc
Suggests:	glibc-devel
Suggests:	gzip
Suggests:	make
Suggests:	nasm
Suggests:	perl-base
Suggests:	tar
Suggests:	wget
Obsoletes:	linux-live-build < 6.2.4-7
ExclusiveArch:	%{ix86} %{x8664} arm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_prefix}/lib
%define		_libexecdir	%{_libdir}/%{name}
%define		_sysconfdir	/etc/%{name}

# autostrip nothing and disable debug (it is supposed to be noarch)
%define		_noautoprov	lib.*\.so.* ld-linux.*\.so.*
%define		_noautoreq	%{_noautoprov}
%define		_noautostrip	.*
%define		_enable_debug_packages 0

# undefined sym: pthread_sigmask
%define		skip_post_check_so	libulockmgr.so.1.0.1

%description
Linux Live Kit is a set of shell scripts which allows you to create
your own Live Linux from an already installed Linux distribution. The
Live system you create will be bootable from CD-ROM or a disk device,
for example USB Flash Drive, USB Pen Drive, Camera connected to USB
port, and so on. People use Linux Live Kit to boot Linux from iPod as
well.

%description -l pl.UTF-8
Linux Live to zestaw skryptów powłoki pozwalających tworzyć własne
LiveCD z każdej dystrybucji Linuksa. Wystarczy zainstalować ulubioną
dystrybucję, usunąć wszystkie niepotrzebne pliki (na przykład strony
manuala i wszystkie inne nieistotne dla nas pliki), a następnie
ściągnąć i uruchomić te skrypty, aby stworzyć własnego Live Linuksa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

cd initramfs/static
./update
rm -v *-{i486,x86_64}
cd -

tar -xf %{SOURCE1} -C tools

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
# rebuild isolinux to be in /pld/ subdir
cd tools
CC="%{__cc}" \
sed -e '/rm/d' ./isolinux.bin.update | sh -x

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libexecdir},%{_bindir},%{_sbindir}}
cp -a bootfiles bootinfo.txt build initramfs livekitlib tools $RPM_BUILD_ROOT%{_libexecdir}
install -p %{SOURCE2} $RPM_BUILD_ROOT%{_sbindir}/linux-live-build

rm -r $RPM_BUILD_ROOT%{_libexecdir}/tools/syslinux-*

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -p .config $RPM_BUILD_ROOT%{_sysconfdir}/config

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO DOC/*.txt
%attr(755,root,root) %{_sbindir}/linux-live-build
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/build
%{_libexecdir}/livekitlib
%{_libexecdir}/bootinfo.txt

%dir %{_libexecdir}/bootfiles
%{_libexecdir}/bootfiles/bootinst.bat
%{_libexecdir}/bootfiles/bootinst.sh
%{_libexecdir}/bootfiles/bootlogo.png
%{_libexecdir}/bootfiles/extlinux.exe
%{_libexecdir}/bootfiles/isolinux.bin
%{_libexecdir}/bootfiles/mbr.bin
%{_libexecdir}/bootfiles/pxelinux.0
%{_libexecdir}/bootfiles/syslinux.cfg
%{_libexecdir}/bootfiles/syslinux.com
%{_libexecdir}/bootfiles/syslinux.exe
%{_libexecdir}/bootfiles/vesamenu.c32

%dir %{_libexecdir}/initramfs
%{_libexecdir}/initramfs/cleanup
%{_libexecdir}/initramfs/init
%{_libexecdir}/initramfs/initramfs_create

%dir %{_libexecdir}/initramfs/static
%{_libexecdir}/initramfs/static/busybox
%{_libexecdir}/initramfs/static/eject
%{_libexecdir}/initramfs/static/mount.dynfilefs
%{_libexecdir}/initramfs/static/mount.ntfs-3g
%{_libexecdir}/initramfs/static/update

%dir %{_libexecdir}/tools
%attr(755,root,root) %{_libexecdir}/tools/isolinux.bin.update
