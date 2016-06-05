import pygame

KeysBuffer__=0
ReadNumber__=0
LastWrote___=0

keys=[0]*255

def Strobe():
	global KeysBuffer__, ReadNumber__, LastWrote___
	KeysBuffer__=0
	if ReadNumber__==0:
		if keys[pygame.K_a]:
			KeysBuffer__=1
	elif ReadNumber__==1:
		if keys[pygame.K_s]:
			KeysBuffer__=1
	elif ReadNumber__==2:
		if keys[pygame.K_SPACE]:
			KeysBuffer__=1
	elif ReadNumber__==3:
		if keys[pygame.K_RETURN]:
			KeysBuffer__=1
	elif ReadNumber__==4:
		if keys[pygame.K_UP]:
			KeysBuffer__=1
	elif ReadNumber__==5:
		if keys[pygame.K_DOWN]:
			KeysBuffer__=1
	elif ReadNumber__==6:
		if keys[pygame.K_LEFT]:
			KeysBuffer__=1
	elif ReadNumber__==7:
		if keys[pygame.K_RIGHT]:
			KeysBuffer__=1
	elif ReadNumber__==16:
		KeysBuffer__=1
	ReadNumber__+=1
	if ReadNumber__>23:
		ReadNumber__=0