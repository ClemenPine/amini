from Levenshtein import distance as lev
from typing import List, Tuple
import sqlite3 as sql

import kb

def add(matrix: str, *, name: str, date: str, who: int) -> Tuple[str, kb.Layout]:
    con, cur = connect()

    if len(name) > 25:
        res = 'LENGTH'

    elif cur.execute('SELECT * from layout WHERE matrix=?', (matrix,)).fetchone():
        res = 'MATRIX'

    elif cur.execute('SELECT * from layout WHERE name=? COLLATE NOCASE', (name,)).fetchone():
        res = 'NAME'

    else:
        payload = (name, matrix, who, date)
        cur.execute('INSERT INTO layout VALUES(?, ?, ?, ?)', payload)

        res = 'OK'

    con.commit()

    ll = kb.Layout(name=name, matrix=matrix)
    return res, ll


def forget(name: str, *, perm: str) -> str:
    con, cur = connect()

    if perm:
        cur.execute('DELETE from layout WHERE name=? COLLATE NOCASE and author_id=?', (name, perm))
    else:
        cur.execute('DELETE from layout WHERE name=? COLLATE NOCASE', (name,))

    con.commit()

    if cur.rowcount:
        res = 'OK'

    elif cur.execute('SELECT * from layout WHERE name=? COLLATE NOCASE', (name,)).fetchone():
        res = 'NOPERM'

    else:
        res = 'NOLAYOUT'

    return res


def change(old: str, new: str, *, perm: str) -> str:
    con, cur = connect()

    if not cur.execute('SELECT * from layout WHERE name=? COLLATE NOCASE', (new,)).fetchone():
        if perm:
            cur.execute('UPDATE layout SET name=? WHERE name=? COLLATE NOCASE and author_id=?', (new, old, perm))
        else:
            cur.execute('UPDATE layout SET name=? WHERE name=? COLLATE NOCASE', (new, old))

        con.commit()

    if cur.rowcount == 1:
        res = 'OK'

    elif cur.rowcount == -1:
        res = 'TAKEN'

    elif cur.execute('SELECT * from layout where name=? COLLATE NOCASE', (old,)).fetchone():
        res = 'NOPERM'

    else:
        res = 'NOLAYOUT'

    return res


def recall(who: str) -> str:
    _, cur = connect()

    names = cur.execute('SELECT name FROM layout WHERE author_id=?', (who,))
    return '\n'.join(x[0] for x in names)


def find(name: str) -> kb.Layout:
    _, cur = connect()

    layouts = cur.execute('SELECT name, matrix FROM layout order by rowid').fetchall()
    
    layouts = sorted(layouts, key=lambda x: len(x[0]))
    closest = min(layouts, key=lambda x: lev(''.join(y for y in x[0].lower() if y in name), name))

    ll = kb.Layout(name=closest[0], matrix=closest[1])
    return ll


def connect(file: str='amini.db'):
    con = sql.connect(file)
    cur = con.cursor()
    return con, cur


def init():
    _, cur = connect()
    cur.execute('CREATE TABLE layout(name, matrix, author_id, year)')