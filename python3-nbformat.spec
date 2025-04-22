#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	The Jupyter Notebook Format
Summary(pl.UTF-8):	Format Jupyter Notebook
Name:		python3-nbformat
Version:	5.10.4
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/nbformat/
Source0:	https://files.pythonhosted.org/packages/source/n/nbformat/nbformat-%{version}.tar.gz
# Source0-md5:	68dfea58a1236aa0518f1fec9c968473
URL:		https://pypi.org/project/nbformat/
BuildRequires:	python3-build
BuildRequires:	python3-hatch-nodejs-version
BuildRequires:	python3-hatchling >= 1.5
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
%if %{with tests}
BuildRequires:	python3-fastjsonschema
BuildRequires:	python3-ipython_genutils
BuildRequires:	python3-jsonschema >= 2.5.1
BuildRequires:	python3-jupyter_core
BuildRequires:	python3-pep440
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-testpath
BuildRequires:	python3-traitlets >= 4.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	sphinx-pdg-3
BuildRequires:	python3-ipython_genutils
BuildRequires:	python3-jsonschema >= 2.5.1
BuildRequires:	python3-jupyter_core
BuildRequires:	python3-traitlets
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nbformat contains the reference implementation of the Jupyter Notebook
format and Python APIs for working with notebooks.

%description -l pl.UTF-8
nbformat zawiera wzorcową implementację formatu Jupyter Notebook oraz
API Pythona do pracy z takimi notatnikami.

%package apidocs
Summary:	API documentation for Python nbformat module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona nbformat
Group:		Documentation

%description apidocs
API documentation for Python nbformat module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona nbformat.

%prep
%setup -q -n nbformat-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest -p no:unraisableexception tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__mv} $RPM_BUILD_ROOT%{_bindir}/jupyter-trust{,-3}
ln -s jupyter-trust-3 $RPM_BUILD_ROOT%{_bindir}/jupyter-trust

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/jupyter-trust
%attr(755,root,root) %{_bindir}/jupyter-trust-3
%{py3_sitescriptdir}/nbformat
%{py3_sitescriptdir}/nbformat-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
