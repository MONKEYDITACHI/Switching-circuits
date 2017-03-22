n=5
#imports===========================================================
import math
#------------------------------------------------------------------
#functions====================================================================
def one(n):     #no.of 1 in binary rep. of n
    binary = [int(i) for i in bin(n)[2:]]
    total = sum(binary)
    return total

def checkexistence(list,x):
    for y in list:
        if(y.term==x.term):
            return False
    return True       

def is_2(n):
    if(n==0):return False
    while(n%2==0):n=n/2
    if(n==1):return True
    return False  

def implicants(minterm,list): #list refers to prime implicant
    list1=[]  #temp. hold for list of prime implicants having minterm 
    for i in list:
        if minterm in i.term:list1.append(i)
    return [list1,len(list1)]

def converter(minterm): #takes minterm class object and convert it to functional rep.
    list2=list(bin(minterm.term[-1])[2:].zfill(n-1))
    for i in minterm.diff[1:]:
        list2[n-2-int(math.log(i,2))]='_'        
    return ''.join(list2)
#-----------------------------------------------------------------------------

#objects====================================================================================
class minterm:
    def __init__(self, term, diff,count):
        self.term=term
        self.diff=diff
        self.count=count

#---------------------------------------------------------------------------------------------      
        
#definition of variables=======================================================
        
A={"minterm":[],"d_care":[]} #stores input minterm's and don't cares.
B={}  #B is a dictionary stores the table data for finding tabular method
C={}    #dictionary to store no.of prime implicant per minterm
first_list=[0]*n   #for n bit no. n+1 size of first_list
prime_implicant=[] #stores prime implicant
function=[] #stores prime implicants in final functions
record=1
#--------------------------------------------------------------------------------


while(1):
    x=input("tell the min_term or press enter to move over")
    if not x:break
    A["minterm"].append(int(x))    

while(1):
    x=input("tell the don_t care or press enter to move over")
    if not x:break
    A["d_care"].append(int(x))    

#print(A)

for i in range(n):
    first_list[i]=[]
    
for i in A["minterm"]:
    id=one(i)
    x=minterm([i],[0],0)
    first_list[id].append(x)
    
for i in A["d_care"]:
    id=one(i)
    x=minterm([i],[0],0)
    first_list[id].append(x)
    
#print(first_list[2][0].term)  

while(record!=0):           # code for first part
    record=0
    second_list=[0]*n
    for i in range(n):second_list[i]=[] #initialize second_list
    for i in range(n-1):
        for j in first_list[i]:
            for k in first_list[i+1]:
                if(j.diff==k.diff):
                    if(is_2(abs(k.term[0]-j.term[0]))):
                        if(k.term[0]>j.term[0]):
                            x=minterm(sorted(j.term+k.term),sorted(k.diff+[k.term[0]-j.term[0]]),0)
                            if(checkexistence(second_list[i],x)): #check whether x already exists in list returns false if already exists
                                second_list[i].append(x);  
                        j.count=k.count=1
                        record=1
                        
    for i in range(n):
        for j in first_list[i]:
            if(j.count==0):
                prime_implicant.append(j)
                
    #Reinitialize things
    first_list=second_list 
        
print("\n")
print([i.term for i in prime_implicant])

for i in A["minterm"]:
    x=implicants(i,prime_implicant)
    B[i]=x[0]
    if x[1] in C:C[x[1]].append(i)  #append list
    else:C[x[1]]=[i]       #start list

print("\n\nessential prime implicants are:")
if 1 in C:
    for i in C[1]:
        print(converter(B[i][0]))  

#when deleted from B whole index is deleted ,but from C only a part of list is deleted so there is a chance of list going to null        

if 1 in C:
    while(len(C[1])!=0):
        for i in C[1]:
            for j in B[i]:
                function.append(j)
                for k in j.term:
                    if k in B:
                        index=len(B[k])
                        C[index].remove(k)
                        del(B[k])                  
                        

l=max([i for i in C])
if(len(C[l])==0):del(C[l])  #to take care of the fact that max is not null
while(len(B)!=0):
    l=max([i for i in C]) #maximum no. of prime implicants of which terms                    
    i=C[l][0]
    if i in B:
        j=B[i][0]
        function.append(j)
        for k in j.term:
            if k in B:
                index=len(B[k])
                C[index].remove(k)
                del(B[k]) 
    if(len(C[l])==0):del(C[l])

print("\n\nfunction is:")
print([converter(i) for i in function])