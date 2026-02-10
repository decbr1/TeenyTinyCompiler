# teeny tiny compiler
**original guide** https://austinhenley.com/blog/teenytinycompiler1<br><br>
example code:
```
PRINT "How many fibonacci numbers do you want?"
INPUT nums
PRINT ""

LET a = 0
LET b = 1
WHILE nums > 0 REPEAT
    PRINT a
    LET c = a + b
    LET a = b
    LET b = c
    LET nums = nums - 1
ENDWHILE
```

## licence
mit licence, deal the software without restriction. <br>
copyright (c) 2020 austin henly <br>
copyright (c) 2026 decbr1 <br>
