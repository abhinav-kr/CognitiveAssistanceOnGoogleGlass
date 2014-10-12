import pymatlab
matlab_session = pymatlab.session_factory()
matlab_session.run('A = randn(4)')
a = matlab_session.getvalue('A')
print(a);
