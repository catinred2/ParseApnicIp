import re
import os.path, time

def getMask( value ):
    mask_value = 0
    temp = int( value )
    while temp > 0:
        temp = temp >> 1
        mask_value = mask_value + 1
    mask_value = 32 - mask_value + 1
    return mask_value


APNIC_IP_FILE = "delegated-apnic-latest"
COUNTRY = "CN"
OUTPUT_FILE_NAME = "cn-ipv4-address.txt"
OUTPUT_IPv6_FILE_NAME = "cn-ipv6-address.txt"
OUTPUT_ACL_FILE_NAME = "gr-cn-ipv4-acl.txt"

try:
   with open( APNIC_IP_FILE ):
       apnic_file = open( APNIC_IP_FILE, 'r' )
except IOError:
   print "Missing file: %s" % APNIC_IP_FILE
   exit()

output_file = open( OUTPUT_FILE_NAME, 'w' )
ipv6_output_file = open( OUTPUT_IPv6_FILE_NAME, 'w' )
acl_output_file = open( OUTPUT_ACL_FILE_NAME, 'w' )

acl_line_num = 20
acl_output_file.write( "ipv4 access-list source-taiwan-ipv4\n" )
ref_apnic_file_time = time.strftime( '%Y%m%d', time.gmtime( os.path.getmtime( APNIC_IP_FILE ) ) )
acl_output_file.write( "  10 remark delegated-apnic-%s\n" % ref_apnic_file_time )

address_line = apnic_file.readline()

while address_line:
    ### match ipv4 address
    address_line = apnic_file.readline()
    matchIpv4Address = re.match( "apnic\|%s\|ipv4\|(\d*.\d*.\d*.\d*)\|(\d*)\|(\d*)\|*" % COUNTRY, address_line, re.M|re.I )
    if matchIpv4Address:
        mask = getMask( matchIpv4Address.group(2) )
        output_file.write( matchIpv4Address.group(1) + "/" + str(mask) + "\n" )
        ipv4_address = matchIpv4Address.group(1) + "/" + str(mask)
        acl_output_file.write( "%4d permit ipv4 %s any\n" % (acl_line_num, ipv4_address))
        acl_line_num += 10

    matchIpv6Address = re.match( "apnic\|%s\|ipv6\|([0-9A-Fa-f:]*)\|(\d*)\|(\d*)\|*" % COUNTRY, address_line, re.M|re.I )
    if matchIpv6Address:
        ipv6_output_file.write( "%s/%s\n" % ( matchIpv6Address.group(1), matchIpv6Address.group(2) ) )


apnic_file.close()
output_file.close()
ipv6_output_file.close()
