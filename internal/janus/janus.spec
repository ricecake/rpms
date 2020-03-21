Summary:    Janus Openid login system
Name:       janus
Version:    0.1
Release:    1
Buildroot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
License:    MIT
Group:      Applications/System
BuildArch:  x86_64
AutoReq:    0
AutoProv:   0

Requires(pre): /usr/sbin/useradd, /usr/bin/getent
BuildRequires:  pkgconfig(systemd)
%{?systemd_requires}

%define debug_package %{nil}
%define _source_payload w0.gzdio
%define _binary_payload w0.gzdio
%define _binary_filedigest_algorithm 1

%description
janus is an openid login system

%pre
/usr/bin/getent group janus > /dev/null || /usr/sbin/groupadd -r janus
/usr/bin/getent passwd janus > /dev/null || /usr/sbin/useradd -r -d /usr/local/ -s /sbin/nologin -g janus janus

%prep
%setup -q -T -D -n %{name}
%build
make package

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
mkdir -p ${RPM_BUILD_ROOT}/etc/janus/
mkdir -p ${RPM_BUILD_ROOT}/etc/systemd/system/
mkdir -p ${RPM_BUILD_ROOT}/srv/janus/
install -m700 _package/janus/bin/janus ${RPM_BUILD_ROOT}/usr/bin/janus
install -m600 janus.service ${RPM_BUILD_ROOT}/etc/systemd/system/
cp -R _package/janus/assets ${RPM_BUILD_ROOT}/srv/janus/
find ${RPM_BUILD_ROOT}/srv/janus/ -type d -exec chmod 700 '{}' \;
find ${RPM_BUILD_ROOT}/srv/janus/ -type f -exec chmod 600 '{}' \;

%define STATE_DIR %{_localstatedir}/lib/rpm-state/janus
%define SUPPORTED_DISTRO %{STATE_DIR}/supported

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%files
%defattr(-,janus,janus)
%attr(0755,root,janus) /usr/bin/janus
%attr(0770,root,janus) /etc/janus/
%attr(0644,root,janus) /etc/systemd/system/janus.service
/srv/janus


%changelog
* Fri Mar 20 2020 Sebastian Green-Husted <geoffcake@gmail.com> 0.1-1
- Initial Build
