#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="asteroid"
service="minimum_laser_server"
args_list = [
    ('level',str),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import exit
import asteroid_lib as al


from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 
if ENV['level']=='easy':
    q=5
if ENV['level']=='medium':
    q=8
if ENV['level']=='difficult':  
    q=11
TAc.print(LANG.render_feedback("instance", 'Instance:'), "yellow", ["bold"])
quad=al.random_quad(q)
al.visualizza(quad)  
TAc.print(LANG.render_feedback("solu", 'Insert your solution: '), "yellow", ["bold"]) 
solu0=input().split(' ')
solu=[]
for i in range(len(solu0)):
    solu.append((solu0[i][0],int(solu0[i][1])))

al.verifica(solu,quad,TAc,LANG)
    
    
exit(0)
