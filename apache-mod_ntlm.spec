# TODO: review security issues
%define		mod_name	ntlm
%define 	apxs		/usr/sbin/apxs
Summary:	This is the NTLM authentication module for Apache
Summary(pl):	Modu³ uwierzytelnienia NTLM dla Apache
Name:		apache-mod_%{mod_name}
Version:	0.1
Release:	0.1
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modntlm/mod_%{mod_name}2-%{version}.tgz
# Source0-md5:	8abe4f235af6825f723412e187cac96b
#Patch0:		%{name}-security.patch
URL:		http://modntlm.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
Requires(post,preun):	%{apxs}
Requires:	apache
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
%setup -q -n mod_%{mod_name}2-%{version}
#%patch -p1

%build
%{__make} APXS=%{apxs}

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
