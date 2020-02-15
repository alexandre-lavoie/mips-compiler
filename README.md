# mips-compiler
MIPS Compiler


# Assembler Directives

```
.data: Stores following instructions in data section.
.space: Adds N \x00 bytes.
.word w1,...,wn: Stores 32-bit value.
.reg: Stores following instructions in registry section.
.main: Start of code.
```

# File Header

```
0x0 -> 0x3: MIPS (Magic Key)
0x4 <- 0x5: Registry Section Size
0x6 <- 0x7: Data Section Size
0x8 <- 0x9: Program Section Size
```