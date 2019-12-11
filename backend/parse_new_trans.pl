% @John Give me 10,000 won
s(User, Price, What) --> user(User), givep(Give), pricep(Price), whatp(What).

user(User) --> [User].

givep(Give) --> give(Give), me(Me).
givep(Give) --> manner(Manner), givep(Give).
manner(Manner) --> [Word], {lex(Word, mannerword)}.
give(Give) --> [Word], {lex(Word, giveword)}.
me(Me) --> [Word], {lex(Word, meword)}.

pricep(Price) --> price(Price), won(Won).
price(Price) --> [Price].
won(Won) --> [Word], {lex(Word, wonword)}.

whatp(What) --> for(For), what(What).
for(For) --> [Word], {lex(Word, forword)}.
what(What) --> [What].

lex(please, mannerword).
lex(just, mannerword).
lex(should, mannerword).
lex(must, mannerword).
lex('Give', giveword).
lex(give, giveword).
lex(grant, giveword).
lex(donate, giveword).
lex(me, meword).
lex(won, wonword).
lex(for, forword).

% s(User, Price, What, [john, please, just, give, me, 1000, won, for, dinner], []).