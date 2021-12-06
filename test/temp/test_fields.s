.data

L1:
	.asciz "%i"
	.text
	.global main

FieldAccess_0:
	stmfd sp!,{fp,lr,v1,v2,v3,v4,v5}
	add fp,sp,#24
	sub sp,fp,#28
	mov v1,#6
	add v2,v1,a2
	mov a1,v2
	b .L2exit

.L2exit:
	sub sp,fp,#24
	ldmfd sp!,{fp,pc,v1,v2,v3,v4,v5}

main:
	stmfd sp!,{fp,lr,v1,v2,v3,v4,v5}
	add fp,sp,#24
	sub sp,fp,#56
	mov a1,#4
	bl _Znwj(PLT)
	mov v5,a1
	mov a1,v5
	mov a2,#5
	bl FieldAccess_0(PLT)
	mov a3,a1
	mov a2,#7
	mov a2,a2
	str a2,[v5,#0]
	ldr v3,[v5,#0]
	add a4,v3,a3
	mov a2,#2
	mul v4,a4,a2
	ldr a1,=L1
	mov a2,v4
	bl printf(PLT)

.L1exit:
	mov r3,#0
	mov r0,r3
	sub sp,fp,#24
	ldmfd sp!,{fp,pc,v1,v2,v3,v4,v5}
