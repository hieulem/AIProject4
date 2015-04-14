irange(X):-connect(X,:).
irange(X):-connect(:,X).

path(A,B):-irange(A),irange(B),connect(A,B).
path(A,B):-path(A,C),path(C,B).


