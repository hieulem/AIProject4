
go(Start, Goal) :-
empty_queue(Empty_open_queue),
enqueue([Start, nil], Empty_open_queue, Open_queue),
%empty_set(Closed_set),
Closed_set = [[Start, nil]],
path(Open_queue, Closed_set, Goal).

path(Open_queue, _, _) :-
empty_queue(Open_queue),
write('Graph searched, no solution found.').

path(Open_queue, Closed_set, Goal) :-
dequeue([State, Parent], Open_queue, _),
my_equal(State, Goal),
write('Solution path is :'), nl,
printsolution([State, Parent],Closed_set).

path(Open_queue, Closed_set, Goal) :-
dequeue([State, Parent], Open_queue, Rest_open_queue),
get_children(State, Rest_open_queue, Closed_set, Children),
add_list_to_queue(Children, Rest_open_queue, New_open_queue),
my_union([[State, Parent]], Closed_set, New_closed_set),
path(New_open_queue, New_closed_set, Goal),!.

get_children(State, Rest_open_queue, Closed_set, Children) :-
(bagof(Child,
moves(State, Rest_open_queue, Closed_set, Child),
Children);
Children = []).

moves(State, Rest_open_queue, Closed_set, [Next, State]) :-
move(State, Next),
not(member_queue([Next, _], Rest_open_queue)),
not(member_set([Next, _], Closed_set, _)).

printsolution([[X, Y, _, _], nil], _) :-
write([X, Y]), nl.

printsolution([State, Parent], Closed_set) :-
member_set([Parent, _], Closed_set, Grandparent),
printsolution([Parent, Grandparent], Closed_set),
my_write(State), nl.

my_write([X, Y, _, _]) :-
write([X, Y]).

my_equal([X, Y, _, _], [Z, W]) :-
X = Z,
Y = W.
