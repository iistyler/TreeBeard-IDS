import subprocess

for i in range(1, 5):
	for j in range(1, 5):
		for k in range(1, 5):
			# for l in range(1, 2):

				subprocess.call(["rm", "-f", "NetBinarySaves/normal2"])
				normal = '{"hiddenLayers":'

				normal += str( [i, j, k] )

				normal += ',"input":["count","logged_in","dst_bytes","http","smtp","private","domain_u","other","ftp_data","urp_i"],"success": "normal"}'

				target = open("JSONNetDesc/normal2", 'w')
				target.write(normal)
				target.close()


				proc = subprocess.Popen(["python testObject.py 2> /dev/null | grep 'Correctly' | egrep -o '[0-9.]+'"], stdout=subprocess.PIPE, shell=True)
				(out, err) = proc.communicate()

				f= open("times.txt","a+")
				f.write(str( [i, j, k] ) + " " + out)
				f.close 

				print str( [i, j, k] ) + " " + out

