Summary:	Linux Live scripts
Name:		linux-live
Version:	5.4.4
Release:	0.4
License:	GPL
Group:		Applications
Source0:	http://www.linux-live.org/dl/%{name}-%{version}.tar.gz
# Source0-md5:	ede0569296df6470b1068a8d3a3c1f37
URL:		http://www.linux-live.org/
Requires:	squashfs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir	%{_prefix}/lib

%description
Linux Live is a set of shell scripts which allows you to create own
LiveCD from every Linux distribution. Just install your favourite
distro, remove all unnecessary files (for example man pages and all
other files which are not important for you) and then download and run
these scripts to build your custom Live Linux.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_sbindir}}
# don't remove -m644 here
install -m644 tools/liblinuxlive $RPM_BUILD_ROOT%{_libdir}
install tools/{deb2mo,dir2mo,img2mo,mo2dir,tgz2mo} $RPM_BUILD_ROOT%{_bindir}
install tools/uselivemod $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc DOC/changelog.txt DOC/requirements.txt
%attr(755,root,root) %{_bindir}/deb2mo
%attr(755,root,root) %{_bindir}/dir2mo
%attr(755,root,root) %{_bindir}/img2mo
%attr(755,root,root) %{_bindir}/mo2dir
%attr(755,root,root) %{_bindir}/tgz2mo
%attr(755,root,root) %{_sbindir}/uselivemod
%{_libdir}/liblinuxlive
