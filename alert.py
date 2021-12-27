import subprocess

def sendmessage(icon,message):
    subprocess.Popen(['notify-send',icon,message])
    return
    
# to add to code
sendmessage("--icon=important",'Careful! You are slouching, sit properly!')
sendmessage("--icon=info",'Correct posture! Keep it up!')
