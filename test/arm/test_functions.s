.data
	
L1:
	.asciz "Square of d larger than sum of squares"
	
L2:
	.asciz "Square of d larger than sum of squares"
	
L3:
	.asciz "\nFactorial of:"
	
L4:
	.asciz "%i"
	
L5:
	.asciz " equal to:"
	
L6:
	.asciz "%i"
	
L7:
	.asciz "\n"
	.text
	.global main
	
Compute_1:
	stmfd sp!,{fp,lr,v1,v2,v3,v4,v5}
	add fp,sp,#24
	sub sp,fp,#28
	add v1,a2,a3
	mov a1,v1
	b .L5exit
	
.L5exit:
	sub sp,fp,#24
	ldmfd sp!,{fp,pc,v1,v2,v3,v4,v5}
	
Compute_2:
	stmfd sp!,{fp,lr,v1,v2,v3,v4,v5}
	add fp,sp,#24
	sub sp,fp,#48
	ldr a2,[a1,#4]
	cmp a2,#0
	beq .5
	ldr a3,[a1,#0]
	mov a1,a3
	b .L4exit
	b .6
	
.5:
	mov v5,#1
	mov v5,v5
	str v5,[a1,#4]
	mov a1,a1
	mov a2,a2
	bl Compute_0(PLT)
	mov v2,a1
	mov a1,a1
	ldr a2,[fp,#-36]
	bl Compute_0(PLT)
	mov v1,a1
	mov a1,a1
	mov a2,v2
	mov a3,v1
	bl Compute_1(PLT)
	mov v5,a1
	mov a1,v5
	b .L4exit
	
.6:
	
.L4exit:
	sub sp,fp,#24
	ldmfd sp!,{fp,pc,v1,v2,v3,v4,v5}
	
Compute_0:
	stmfd sp!,{fp,lr,v1,v2,v3,v4,v5}
	add fp,sp,#24
	sub sp,fp,#28
	mul a3,a2,a2
	mov a1,a3
	b .L3exit
	
.L3exit:
	sub sp,fp,#24
	ldmfd sp!,{fp,pc,v1,v2,v3,v4,v5}
	
Compute_3:
	stmfd sp!,{fp,lr,v1,v2,v3,v4,v5}
	add fp,sp,#24
	sub sp,fp,#36
	cmp a2,#1
	movlt v5,#1
	movge v5,#0
	cmp v5,#0
	beq .3
	mov v5,#1
	mov v1,v5
	mov a1,v1
	b .L2exit
	b .4
	
.3:
	sub v4,a2,#1
	str a2,[fp,#-32]
	str a1,[fp,#-28]
	mov a1,a1
	mov a2,v4
	bl Compute_3(PLT)
	mov a2,a1
	ldr v2,[fp,#-32]
	mul v2,v2,a2
	mov a1,v2
	b .L2exit
	
.4:
	
.L2exit:
	sub sp,fp,#24
	ldmfd sp!,{fp,pc,v1,v2,v3,v4,v5}
	
main:
	stmfd sp!,{fp,lr,v1,v2,v3,v4,v5}
	add fp,sp,#24
	sub sp,fp,#68
	mov v5,#1
	mov a4,v5
	mov v5,#2
	mov a3,v5
	mov v5,#3
	mov a2,v5
	mov v5,#4
	mov v1,v5
	str a4,[fp,#-28]
	str a3,[fp,#-32]
	str a2,[fp,#-36]
	mov a1,#8
	bl _Znwj(PLT)
	mov a4,a1
	str a4,[fp,#-52]
	ldr a1,[fp,#-52]
	ldr a2,[fp,#-28]
	ldr a3,[fp,#-32]
	bl Compute_2(PLT)
	mov v5,a1
	ldr a1,[fp,#-52]
	ldr a2,[fp,#-36]
	bl Compute_0(PLT)
	mov a4,a1
	add a1,v5,a4
	str a1,[fp,#-44]
	ldr a1,[fp,#-52]
	mov a2,v1
	bl Compute_0(PLT)
	mov a3,a1
	ldr a4,[fp,#-44]
	cmp a3,a4
	movgt a1,#1
	movle a1,#0
	cmp a1,#0
	beq .1
	str a4,[fp,#-44]
	ldr a1,=L1
	bl printf(PLT)
	b .2
	
.1:
	ldr a1,=L2
	bl printf(PLT)
	
.2:
	ldr a1,[fp,#-52]
	mov a2,#4
	bl Compute_3(PLT)
	mov a2,a1
	str a2,[fp,#-44]
	ldr a1,=L3
	bl printf(PLT)
	ldr a1,=L4
	mov a2,#4
	bl printf(PLT)
	ldr a1,=L5
	bl printf(PLT)
	ldr v4,[fp,#-44]
	ldr a1,=L6
	mov a2,v4
	bl printf(PLT)
	ldr a1,=L7
	bl printf(PLT)
	
.L1exit:
	mov r3,#0
	mov r0,r3
	sub sp,fp,#24
	ldmfd sp!,{fp,pc,v1,v2,v3,v4,v5}
