%define		mod_name	ntlm
%define 	apxs		/usr/sbin/apxs
Summary:	This is the NTLM authentication module for Apache
Summary(pl):	Modu³ uwierzytelnienia NTLM dla Apache
Name:		apache-mod_%{mod_name}
Version:	0.4
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modntlm/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	5e9b8d1abf872926d6ff01a05a7deb2a
Patch0:		%{name}-security.patch
URL:		http://modntlm.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
Requires(post,preun):	%{apxs}
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using samba or windows-like server (using
NTLM protocol).

%description -l pl
To jest modu³ uwierzytelnienia dla Apache pozwalaj±cy na
uwierzytelnianie klientów HTTP poprzez sambê lub serwer na Windows (z
u¿yciem protoko³u NTLM).

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch -p1

%build
PATH=$PATH:/usr/sbin %{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*
