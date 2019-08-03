#2017255:Pratik Pathak
#2017273: Yash Kalyani
from tables import *

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def checkifopcodeexists(temp):
    if(len(temp)==1):
        return (temp[0] in op_table.keys() or temp[0] in special_op.keys())
    elif(len(temp)==3):
        return (temp[1] in op_table.keys() or temp[1] in special_op.keys())
    else:
        if(temp[1] in op_table.keys() or temp[1] in special_op.keys()):
            return True
        elif(temp[0] in op_table.keys() or temp[0] in special_op.keys()):
            return True
        else:
            return False

def checkstp(temp):
    if(len(temp)==1):
        return (temp[0]=="STP")
    elif(len(temp)==3):
        return (temp[1]=="STP")
    else:
        if(temp[1]=="STP"):
            return True
        elif(temp[0]=="STP"):
            return True
        else:
            return False

def checkifliteral(temp):
	
	if(len(temp[-1])>1 and temp[-1][0]=='\'' and temp[-1][1]=='=' and temp[-1][-1]=='\''):
		return True
	else:
		return False

def checkifcomment(temp):
    c=-1
    x="//"
    t=-1
    for i in temp:
        t+=1
        if x in i:
            c=t
            return c
    return c

def printtable(dict1):
    if(len(dict1.keys())==0):
        print("table is empty")
    else:
        for i in dict1.keys():
            print(str(i)+"   "+str(dict1[i]))


content=[]
relocation_dict={"offset":0}
symbol_table={}
label_table={}
literal_table={}
value_table={}
external_reference_table=[]
entry_point_table={}
ilc1=relocation_dict["offset"]
il=0
stpflag=0

errfile=open("errors.txt","w")
machinecodefile=open("machinecode.txt","w")
relocation_dict_file=open("relocationfile.txt","w")
linecount=1

with open("input.txt") as f:
    content=f.readlines()
content=[x.strip() for x in content]

instruction_count=0
for l in content:
	temp=list(map(str, l.split()))
	val=checkifcomment(temp)
	if(val!=-1):
		temp=temp[:val]    
	if(len(temp)!=0):
		instruction_count+=1

ilc2=8*instruction_count

ilc2+=relocation_dict["offset"]
globalmaincheck=0
stp=0
errcheck=0

for l in content:
	lngth=0
	val=0
	illegal=0
	temp=list(map(str, l.split()))
	val=checkifcomment(temp)
	if(val!=-1):
		temp=temp[:val]
	if(len(temp)>3):
		errfile.write("Line "+str(linecount)+" has invalid instruction")
		print("Line "+str(linecount)+" has invalid instruction") 
		errcheck=1   
	elif(len(temp)!=0):
		
		if(checkifopcodeexists(temp)):
			
			if(ilc1>256 or ilc2>256):
				print("Memory limit exceeded")
				errcheck=1
				break

			if(len(temp)==1):
				
				if(temp[0]!='CLA' and temp[0]!='STP'):
					errfile.write("Line "+ str(linecount)+" has an opcode with insufficient operands")
					print("Line "+ str(linecount)+" has an opcode with insufficient operands")
					errcheck=1

			elif(len(temp)==2):
				
				if(temp[0] in op_table.keys()):	
					
					if(temp[0]=='CLA' or temp[0]=='STP'):
						errfile.write("Line "+ str(linecount)+" has an opcode with insufficient operands")
						print("Line "+ str(linecount)+" has an opcode with insufficient operands")
						errcheck=1

				elif(temp[1] in op_table.keys()):
					
					if(temp[1]!='CLA' and temp[1]!='STP'):
						errfile.write("Line "+ str(linecount)+" has an opcode with insufficient operands")
						print("Line "+ str(linecount)+" has an opcode with insufficient operands")
						errcheck=1
			
			elif(len(temp)==3):
				
				if(temp[0] in op_table.keys() or temp[0] in special_op.keys()):
					errfile.write("Line "+ str(linecount)+" has an opcode with too many operands")
					print("Line "+ str(linecount)+" has an opcode with too many operands")
					errcheck=1
				
				if(temp[1]=='CLA' and temp[1]=='STP'):
					errfile.write("Line "+ str(linecount)+" has an opcode with insufficient operands")
					print("Line "+ str(linecount)+" has an opcode with insufficient operands")
					errcheck=1

			if(stp==0 and checkstp(temp)):
				stp=1
			
			if(temp[0] not in op_table.keys()):
				
				if(temp[0] not in label_table.keys()):
					label_table[temp[0]]=ilc1
			
			if(checkifliteral(temp)):
				
				if(temp[-1] not in literal_table.keys()):
					literal_table[temp[-1]]=ilc2
					ilc2+=8
			
			elif(len(temp)>1):
				
				if(temp[-2] in op_table.keys()):
					
					if(temp[-1] not in label_table.keys()):
						symbol_table[temp[-1]]=ilc1

					else:
						errfile.write("Line "+str(linecount)+ " has multiple declarations of the symbol. "+temp[-1])
						print("Line "+str(linecount)+" Multiple declarations of the symbol "+temp[-1])
				
				elif(temp[-2] in special_op.keys()):
					value_table[temp[0]]=temp[1]

			elif(len(temp)==1):
				
				if(temp[0] not in op_table.keys() and temp[0] not in special_op.keys()):
					illegal=1

		elif(temp[0]=='Global' and temp[1]=='Main'):
			globalmaincheck=1
		
		elif(temp[0]=='EXTERN'):
			
			if(len(temp)!=2):
				errfile.write("At Line "+str(linecount)+" invalid command")
				print("At Line "+str(linecount)+" invalid command")
			
			else:
				
				if(globalmaincheck!=1):
					errfile.write("At "+str(linecount)+ " Use of Extern without defining Global Main")
					print("At "+str(linecount)+ " Use of Extern without defining Global Main")
				external_reference_table.append(temp[1])

		elif(temp[0]=='Public'):
			
			if(len(temp)!=2):
				errfile.write("At Line "+str(linecount)+" invalid command")
				print("At Line "+str(linecount)+" invalid command")
			
			else:
				entry_point_table[temp[1]]=1
		
		else:
			errfile.write("Line "+str(linecount)+ " No valid opcode.     ")
			print("Line "+str(linecount)+" No valid opcode exists")
			errcheck=1
		ilc1+=8
	linecount+=1

for i in entry_point_table.keys():
	try:
		entry_point_table[i]=label_table[i]
	except:
		KeyError
		errfile.write("")

for i in symbol_table.keys():
    if(i not in label_table.keys()):
        errfile.write("Symbol "+i+" is not defined")
        print("Symbol "+i+" is not defined")
        label_table[i]=ilc2
        ilc2+=8

for i in label_table.keys():
	if(i in op_table.keys()):
		errfile.write("Label "+str(i)+" cannot be a valid label because it is an opcode")
		print("Label "+str(i)+" cannot be a valid label because it is an opcode")
		errcheck=1
	
if(stp==0):
    errfile.write("No end statement encountered")
    print("No end statement encountered")
    content.append("STP")

errfile.close()
print()
print()
count=0

if(errcheck==0):
	for l in content:
		printstr=""
		temp=list(map(str, l.split()))
		val=checkifcomment(temp)
		if(val!=-1):
			temp=temp[:val]    
		if(len(temp)!=0):
			
			if(checkifopcodeexists(temp)):
				#print(l)
				counter=bin(count)[2:]
				#print(counter,count)
				counter=(8-len(counter))*'0'+counter 
				printstr1=counter+"                   "
				printstr2=""
				
				if(len(temp)==1):
					printstr2+=op_table[temp[0]]

				elif(len(temp)==2):
					
					if(temp[0] in op_table.keys()):
						printstr2+=op_table[temp[0]]+"  "
						
						if(temp[1] in label_table.keys()):
							counter=bin(label_table[temp[1]])[2:]
							counter=(8-len(counter))*'0'+counter 
							printstr2+=counter+"  "
						
						elif(temp[1] in literal_table.keys()):
							counter=bin(literal_table[temp[1]])[2:]
							counter=(8-len(counter))*'0'+counter 
							printstr2+=counter+"  "
					
					elif(temp[0] in label_table.keys()): 
						printstr2+=op_table[temp[1]]


				elif(len(temp)==3):
					
					if(temp[1] not in special_op.keys()): 
						printstr2+=op_table[temp[1]]+"  "
						
						if(temp[2] in label_table.keys()):
							counter=bin(label_table[temp[2]])[2:]
							counter=(8-len(counter))*'0'+counter 
							printstr2+=counter+"  "
						
						elif(temp[2] in literal_table.keys()):
							counter=bin(literal_table[temp[2]])[2:]
							counter=(8-len(counter))*'0'+counter 
							printstr2+=counter+"  "
				
				if(printstr2!=""):
					machinecodefile.write(printstr2)
					print(printstr1,printstr2)
				count+=8
	print("Do you want to print the Symbol table?? Yes/No")
	s=str(input())
	if(s=='Yes'):
		print("SYMBOL","   TYPE   "," OFFSET"," VALUE "," SIZE ")
		for i in label_table.keys():
			if(i in value_table.keys()):
				print("  "+i+"  |  Variable  |  "+str(label_table[i])+"  |  "+str(value_table[i])+"  |  Byte  ")
			elif(i in symbol_table.keys()):
				print("  "+i+"  |  Label  |  "+str(label_table[i])+"  |  -  |  Byte  ")
else:
	print("Input file is not convertable! Please recheck the input code")
	             

"""printtable(value_table)
print()
printtable(symbol_table)
print()
printtable(label_table)
print()
printtable(literal_table)"""

relocation_dict_file.write("offset " +str(relocation_dict["offset"]))
value_table_file=open("value_table_file.txt","w")
for i in value_table:
    value_table_file.write(str(i)+" "+str(value_table[i]))
value_table_file.close()


symbol_table_file=open("symbol_table_file.txt","w")
for i in symbol_table:
    symbol_table_file.write(str(i)+" "+str(symbol_table[i]))
symbol_table_file.close()


label_table_file=open("label_table_file.txt","w")
for i in label_table:
    label_table_file.write(str(i)+" "+str(label_table[i]))
label_table_file.close()


literal_table_file=open("literal_table_file.txt","w")
for i in literal_table:
    literal_table_file.write(str(i)+" "+str(literal_table[i]))
literal_table_file.close()

relocation_dict_file.close()
machinecodefile.close()
errfile.close()







