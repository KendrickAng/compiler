.data
	
L1:
	.asciz "true"
	
L2:
	.asciz "false"
	
L3:
	.asciz "true"
	
L4:
	.asciz "false"
	.text
	.global main
	
main:
	stmfd sp!,{fp,lr,v1,v2,v3,v4,v5}
	add fp,sp,#24
	sub sp,fp,#64
	mov v5,#4
	mov a4,v5
	mov v5,#5
	mov a3,v5
	mov v5,#1
	mov a2,v5
	mov v5,#0
	mov v1,v5
	and v5,a2,v1
	cmp v5,#0
	moveq v5,#0
	movne v5,#1
	orr v2,v5,v1
	cmp v2,#0
	moveq v2,#0
	movne v2,#1
	orr v4,a2,v1
	cmp v4,#0
	moveq v4,#0
	movne v4,#1
	orr v3,v2,v4
	cmp v3,#0
	moveq v3,#0
	movne v3,#1
	str v3,[fp,#-44]
	cmp a4,a3
	movlt v3,#1
	movge v3,#0
	ldr v5,[fp,#-44]
	and v5,v3,v5
	cmp v5,#0
	moveq v5,#0
	movne v5,#1
	cmp v5,#0
	beq .1
	str a4,[fp,#-28]
	str a3,[fp,#-32]
	ldr a1,=L1
	bl printf(PLT)
	b .2
	
.1:
	ldr a1,=L2
	bl printf(PLT)
	
.2:
	ldr a3,[fp,#-28]
	ldr a4,[fp,#-32]
	cmp a3,a4
	movgt a1,#1
	movle a1,#0
	orr a4,v5,a1
	cmp a4,#0
	moveq a4,#0
	movne a4,#1
	cmp a4,#0
	beq .3
	ldr a1,=L3
	bl printf(PLT)
	b .4
	
.3:
	ldr a1,=L4
	bl printf(PLT)
	
.4:
	
.L1exit:
	mov r3,#0
	mov r0,r3
	sub sp,fp,#24
	ldmfd sp!,{fp,pc,v1,v2,v3,v4,v5}
