#!/usr/bin/python
import subprocess
import re

inventory_path="/root/ansible/my_inventory/aws/ec2-inventory-lab"

class EC2_INC:
   def __init__(self,id,pub_ip,image,ssh_user):
     self.id=id
     self.pub_ip=pub_ip
     self.image=image
     self.ssh_user=ssh_user
   def __str__(self):
     return "ID: "+self.id+" Pub IP: "+self.pub_ip+" OS Image: "+self.image+" User: "+self.ssh_user

def get_string(a_string):
  rs_str=a_string.strip()
  rs_str=rs_str.replace('[','')
  rs_str=rs_str.replace(']','')
  rs_str=rs_str.replace('"','')
  rs_str=rs_str.replace('\n','')
  rs_str=rs_str.replace('\t','')
  rs_str=rs_str.replace(' ','')
  rs_str=rs_str.replace(',','')
  rs_str=rs_str.replace('Name:','')
  return rs_str

def get_list(rs_string):
   rs=[]
   for i in rs_string.split():
     if(len(i)>2):
       i=i.replace('"','')
       i=i.replace(',','')
       rs.append(i)
   return rs	

def get_inc_ip(id):
  rs_string=subprocess.getoutput("aws ec2 describe-instances --query Reservations[].Instances[].PublicIpAddress --filter 'Name=instance-id,Values="+id+"'")
  rs_str=get_string(rs_string)
  return rs_str

def get_image(id):
  rs_string=subprocess.getoutput("aws ec2 describe-instances --query Reservations[].Instances[].ImageId --filter 'Name=instance-id,Values="+id+"'")
  rs_img_id=get_string(rs_string)
  rs_string=subprocess.getoutput("aws ec2 describe-images --image-ids "+rs_img_id+" |grep -iw Name" )
  img_name=get_string(rs_string)
  return img_name

def get_ssh_user(image_name):
   if("ubuntu" in image_name):
     return "ubuntu"
   return "ec2-user"

rs_string=subprocess.getoutput("aws ec2 describe-instances --query Reservations[].Instances[].InstanceId")
rs_list=get_list(rs_string)
list_ec2_inc=[]
inv_file=open(inventory_path,"w")
inv_file.write("[ec2-servers]\n")
for a_id in rs_list:
  pub_ip=get_inc_ip(a_id)
  img_name=get_image(a_id)
  ssh_user=get_ssh_user(img_name)
  a_instance=EC2_INC(a_id,pub_ip,img_name,ssh_user) 
  list_ec2_inc.append(a_instance) 
  print(str(a_instance))
  print("------------------------------------------------------------")


for a_inc in list_ec2_inc:
   str_inv=a_inc.pub_ip+" Image="+a_inc.image+" ansible_user="+a_inc.ssh_user+"\n"
   inv_file.write(str_inv)

inv_file.close()
  
