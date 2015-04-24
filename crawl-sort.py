import os
import re
import sys

url = "https://s-p.mit.edu/myacct/room_details.php?room_ID="
matched_str = "<tr><td class='tableRowLight'><b>Square Footage:</b></td><td class='tableRowLight'>"


if __name__ == "__main__":
    
    if len(sys.argv) != 5:
        print 'Usage:', sys.argv[0], 'ssl_certificate ssl_privatekey outfile input_roomfile'
        exit(11)

    certificate = sys.argv[1]
    private_key = sys.argv[2]
    
    rooms = []
    for line in open(sys.argv[4]).readlines():
        rooms += [line.split(' ')[1]]

    d = {}
    for room in rooms:
        #wget --no-check-certificate --certificate=cert.pem --private-key=cert_out.pem https://s-p.mit.edu/myacct/room_details.php?room_ID=497A
        os.system('wget --no-check-certificate --certificate=%s --private-key=%s %s%s -O temp -q' %(certificate, private_key, url, room))

        for line in open('temp').readlines():
            if line.find('Square Footage') >= 0:
                size =  int(line.split(matched_str)[1].split('</td></tr>')[0])
                d[room] = size

    
    ## write sorted rooms into output file
    o_fh = open(sys.argv[3],'w')
    d = sorted(d.items(), key=lambda x: x[1], reverse=True)

    for r in d:
        o_fh.write(r[0] + '\t' + str(r[1]) + '\n')    
    
    o_file.close()
