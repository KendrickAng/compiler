.data
	
L1:
	.asciz "%i"
	.text
	.global main
	
main:
	stmfd sp!,{fp,lr,v1,v2,v3,v4,v5}
	add fp,sp,#24
	sub sp,fp,#92
	mov v5,#1
	add a4,v5,#2
	add a3,a4,#3
	add a2,a3,#4
	add v1,a2,#5
	add v5,v1,#6
	add v2,v5,#7
	add v4,v2,#8
	add v3,v4,#9
	str v3,[fp,#-32]
	add v3,v3,#10
	add v5,v3,#11
	add v3,v5,#12
	add a4,v3,#13
	add a3,a4,#14
	add v3,a3,#15
	add a3,v3,#16
	add v5,a3,#17
	add v4,v5,#18
	add a1,v4,#19
	add v3,a1,#20
	ldr a1,=L1
	mov a2,v3
	bl printf(PLT)
	
.L1exit:
	mov r3,#0
	mov r0,r3
	sub sp,fp,#24
	ldmfd sp!,{fp,pc,v1,v2,v3,v4,v5}
