% I just sent 10000 won to @Mike
s(User, Price) --> i(I), sendp(Send), pricep(Price), userp(User).

i(I) --> [Word], {lex(Word, iword)}.

sendp(Send) --> send(Send).
sendp(Send) --> manner(Manner), sendp(Send).
manner(Manner) --> [Word], {lex(Word, mannerword)}.
send(Send) --> [Word], {lex(Word, sendword)}.

pricep(Price) --> price(Price), won(Won).
price(Price) --> [Price].
won(Won) --> [Word], {lex(Word, wonword)}.

userp(User) --> to(To), user(User).
to(To) --> [Word], {lex(Word, toword)}.
user(User) --> [User].

lex('I', iword).
lex(i, iword).
lex(just, mannerword).
lex(have, mannerword).
lex(sent, sendword).
lex(granted, sendword).
lex(donated, sendword).
lex(won, wonword).
lex(to, toword).
lex(for, toword).

% s(User, Price, [i, just, have, donated, 7000, won, for, mia], []).