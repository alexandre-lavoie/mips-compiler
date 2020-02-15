.reg    
.word   0,100,0,200,0,300,0,0,0

.data
.word   124,348,246,468,368,584
.space  92
.word   17
.space  102
.word   41

.main
lw      r2,4(r1)
lw      r4,8(r3)
multu   r6,r2,r4
addu    r8,r4,r6
sw      r6,8(r3)
sw      r8,4(r5)      