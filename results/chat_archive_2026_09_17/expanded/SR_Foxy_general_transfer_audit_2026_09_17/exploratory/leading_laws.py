exec(open('/mnt/data/sr_foxy_pass03/explore_cabling_transfer.py').read().split('for n in range(2,9):')[0])
F=s.symbols('F0:10')
for n in range(1,9):
 fs={r:s.cancel(sum(S[r].coeff(z,j)*z**j*(1 if j==0 else E[j]) for j in range(r+1))/S[r]) for r in range(n%2,n+1,2)}
 H=0
 for j in range(n%2,n+1,2):
  v=s.cancel(sum((comb(n,(n-r)//2)-(comb(n,(n-r)//2-1) if (n-r)//2 else 0))*S[r].coeff(z,j)*fs[r] for r in range(n%2,n+1,2)))
  lead=s.cancel(v/z**(n-j)).subs(z,0)
  H+=lead*(1 if j==0 else F[j])
 H=s.factor(H)
 print(n,H)
