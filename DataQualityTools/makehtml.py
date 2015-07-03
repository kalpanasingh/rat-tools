# Produce a html page from the DQ LL JSON table

import argparse
import array
import json
import sys

from pprint import pprint

# Read the DQ LL JSON table
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="filename", help="JSON table filename", type=str, required=True)
    args = parser.parse_args()
    if args.filename is None:
        sys.stderr.write("Please supply a JSON table filename using \'-f\'")
        sys.exit(1)

    jsonfile = args.filename

    splitjson = jsonfile.split("_")

    runnumber = int(splitjson[1])

    # Create the html table
    htmlfile = "run_{0}_dqll.html".format(runnumber)
        
    htmltable = open(htmlfile,'w')

    # Open the JSON table and reads it
    jsontable = open(jsonfile,'r')

    jsondata = json.load(jsontable)

    # Check that run number is correct
    runrange = jsondata["run_range"]
     
    run1 = runrange[0]

    run2 = runrange[1]
    
    if (run1 != run2) or (run1 != runnumber):

        sys.stderr.write("Problem with run number: no match between filename and/or run range")
        sys.exit(1)

    startdate = jsondata["start_time"]
    
    duration = jsondata["duration_seconds"]
    
    print "Creating a html file for run {0} started {1} of duration {2} seconds".format(run1,startdate,duration)
    
    # Racks
    numberofracks = 12
    
    rackid = (1,2,3,4,5,6,7,8,9,10,11,'Timing')
    
    # Crates
    numberofcrates = 19
    
    crateid = array.array('i',(i for i in range(0,numberofcrates)))
    
    # compensation coils
    numberofcompcoils = 14
    
    compcoilname = ('1A','1B',2,3,4,5,6,7,'8A','8B','9A','9B',10,11)
    
    #Hold up ropes
    numberofholdupropes = 10
    
    holdupropesid = (1,2,3,4,5,6,7,8,9,10)
    
    #Hold down ropes
    numberofholddownropes = 20
    
    holddownropesid = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)
    
    #Equator monitors
    numberofequatormonitors = 4
    
    equatormonitorsid = (1,2,3,4)

    # Retrieve crate HV status power-supply A
    cratestatusa = jsondata["crate_hv_status_a"]

    # Retrieve crate 16 HV status power-supply B
    cratestatusb = jsondata["crate_16_hv_status_b"]

    # Retrieve crate HV nominal power-supply A
    cratehvnominala = jsondata["crate_hv_nominal_a"]

    # Retrieve crate 16 HV nominal power-supply B
    cratehvnominalb = jsondata["crate_16_hv_nominal_b"]

    # Retrieve crate HV read power-supply A
    cratehvreada = jsondata["crate_hv_read_value_a"]

    # Retrieve crate 16 HV read power-supply B
    cratehvreadb = jsondata["crate_16_hv_read_value_b"]

    # Retrieve crate current read power-supply A
    cratecurrentreada = jsondata["crate_current_read_value_a"]

    # Retrieve crate 16 current read power-supply B
    cratecurrentreadb = jsondata["crate_16_current_read_value_b"]

    # Retrieve Xl3 error packets
    xl3errorcmdrejected = jsondata["xl3_error_packet_cmd_rejected"]
    xl3errorpackettransfererror = jsondata["xl3_error_packet_transfer_error"]
    xl3errorpacketxl3dataavailunknown = jsondata["xl3_error_packet_xl3_data_avail_unknown"]
    xl3errorpacketfecbundlereaderror = jsondata["xl3_error_packet_fec_bundle_read_error"]
    xl3errorpacketfecbundleresyncherror = jsondata["xl3_error_packet_fec_bundle_resynch_error"]
    xl3errorpacketfecmemlevelunknown = jsondata["xl3_error_packet_fec_mem_level_unknown"]
    
    # Retrieve XL3 screwed packets
    xl3screwedpacketfecscrewed = jsondata["xl3_screwed_packet_fec_screwed"]
            
    # Create the html file
    htmltable.write("<!DOCTYPE html>\n")
    htmltable.write("<html><head>\n")
    htmltable.write("<meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">\n")
    htmltable.write("\n")
    htmltable.write("<script language=\"javascript\" src=\"http://www.lip.pt/~gersende/snop/dq_ll/css/jquery.js\"></script>\n")
    htmltable.write("<script language=\"javascript\" src=\"http://www.lip.pt/~gersende/snop/dq_ll/css/bootstrap.js\"></script>\n")
    htmltable.write("<script language=\"javascript\" src=\"http://www.lip.pt/~gersende/snop/dq_ll/css/cookies.js\"></script>\n")
    htmltable.write("<script language=\"javascript\" src=\"http://www.lip.pt/~gersende/snop/dq_ll/css/toastr.js\"></script>\n")
    htmltable.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"http://www.lip.pt/~gersende/snop/dq_ll/css/bootstrap.css\">\n")
    htmltable.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"http://www.lip.pt/~gersende/snop/dq_ll/css/style.css\">\n")
    htmltable.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"http://www.lip.pt/~gersende/snop/dq_ll/css/tabs.css\">\n")
    htmltable.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"http://www.lip.pt/~gersende/snop/dq_ll/css/toastr.css\">\n")
    htmltable.write("\n")

    filetitle = "<title>Run {0} Data Quality Low level checks</title>\n".format(runnumber)
    htmltable.write(filetitle)
    htmltable.write("<style></style>\n")
    htmltable.write("</head>\n")

    htmltable.write("\n")
    htmltable.write("<body style=\"\"\>\n")
    htmltable.write("\n")
    htmltable.write("<div id=\"content\">\n")
    htmltable.write("<a href=\"http://www.lip.pt/~gersende/snop/dq_ll//index.html\">Back to the run list</a>\n")
    htmltable.write("<h1>\n")

    title = "Run {0}\n".format(runnumber)
    htmltable.write(title)
    htmltable.write("</h1>\n")
    htmltable.write("\n")
    htmltable.write("<ul class=\"nav nav-tabs\">\n")
    htmltable.write("<li class=\"active\"><a href=\"#quality\" data-toggle=\"tab\">Data Quality</a></li>\n")
    htmltable.write("</ul>\n")
    htmltable.write("<div class=\"tab-content\">\n")
    htmltable.write("\n")
    htmltable.write("<div class=\"tab-pane active\" id=\"quality\">\n")
    htmltable.write("<h2>\n")
    htmltable.write("Low-level checks analysed:&nbsp;<span style=\"color:#3399FF;\">yes</span>\n")
    htmltable.write("</h2>\n")
    htmltable.write("</div>\n")
    htmltable.write("\n")
    htmltable.write("<br>\n")
    htmltable.write("\n")
    htmltable.write("<b>Rack Voltages</b><br>\n")
    htmltable.write("<table class=\"table table-striped table-condensed\">\n")
    htmltable.write("<tbody><tr>\n")
    htmltable.write("<th></th>\n")
    htmltable.write("<th style=\"white-space: nowrap;\">&nbsp;</th>\n")

    for aa in range(0, numberofracks):
        rackentry = "<th style=\"white-space: nowrap;\">{0}</th>\n".format(rackid[aa])
        htmltable.write(rackentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>-24V</b></td>\n")

    for ab in range(0,numberofracks):
        htmltable.write("<td style=\"white-space: nowrap;\"></td>\n")

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>+24V</b></td>\n")

    for ac in range(0,numberofracks):
        htmltable.write("<td style=\"white-space: nowrap;\"></td>\n")

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>+8V</b></td>\n")

    for ad in range(0,numberofracks):
        htmltable.write("<td style=\"white-space: nowrap;\"></td>\n")

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>-5V</b></td>\n")

    for ae in range(0,numberofracks):
        htmltable.write("<td style=\"white-space: nowrap;\"></td>\n")

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>+5V</b></td>\n")

    for af in range(0,numberofracks):
        htmltable.write("<td style=\"white-space: nowrap;\"></td>\n")

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("</tbody>\n")
    htmltable.write("</table>\n")
    htmltable.write("\n")
    htmltable.write("<br>\n")
    htmltable.write("\n")
    htmltable.write("<b>Crate High Voltages</b><br>\n")
    htmltable.write("<table class=\"table table-striped table-condensed\">\n")
    htmltable.write("<tbody><tr>\n")
    htmltable.write("<th></th>\n")
    htmltable.write("<th style=\"white-space: nowrap;\">&nbsp;</th>\n")

    for ag in range(0, numberofcrates):
        crateentry = "<th style=\"white-space: nowrap;\">{0}</th>\n".format(crateid[ag])
        htmltable.write(crateentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>Status</b></td>\n")

    for ah in range(0, numberofcrates):
        if ah == 16:
            if cratestatusa[ah] != True:
                if cratestatusb != True:
                    statusentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">OFF (A) OFF (B)</span></td>\n"
                else:
                    statusentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">OFF (A) </span>ON (B)</td>\n" 
            else:
                if cratestatusb == False:
                    statusentry = "<td style=\"white-space: nowrap;\">ON (A) <span style=\"color:#FF0000;\">OFF (B)</span></td>\n"
                else:
                    statusentry = "<td style=\"white-space: nowrap;\">ON (A) ON (B)</td>\n"
        else:
            if cratestatusa[ah] == False:
                statusentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">OFF</span></td>\n"
            else:
                statusentry = "<td style=\"white-space: nowrap;\">ON</td>\n"
        htmltable.write(statusentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>HV nominal</b></td>\n")

    for ai in range(0,numberofcrates):
        if ai == 16:
            if ((cratehvnominala[ai] > 2500) | (cratehvnominala[ai] < 1500)):
                nominalentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0} (A) {1} (B)</span></td>\n".format(cratehvnominala[ai],cratehvnominalb)
            else:
                nominalentry = "<td style=\"white-space: nowrap;\">{0} (A) {1} (B)</td>\n".format(cratehvnominala[ai],cratehvnominalb)
        else:
            if ((cratehvnominala[ai] > 2500) | (cratehvnominala[ai] < 1500)):
                nominalentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0}</span></td>\n".format(cratehvnominala[ai])
            else:
                nominalentry = "<td style=\"white-space: nowrap;\">{0}</td>\n".format(cratehvnominala[ai])
        htmltable.write(nominalentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")

    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>HV read</b></td>\n")

    for aj in range(0,numberofcrates):
        if aj == 16:
            if (cratestatusa[aj] == False) | (cratestatusb == False):
                if (cratehvreada[aj] > 0) | (cratehvreadb > 0):
                    readentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0} (A) {1} (B)</span></td>\n".format(cratehvreada[aj],cratehvreadb)
                else:
                    readentry = "<td style=\"white-space: nowrap;\">{0} (A) {1} (B)</td>\n".format(cratehvreada[aj],cratehvreadb)
            else:
                if (abs(cratehvreada[aj] - cratehvnominala[aj]) > 50):
                    readentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0} (A) {1} (B)</span></td>\n".format(cratehvreada[aj],cratehvreadb)
                else:
                    readentry = "<td style=\"white-space: nowrap;\">{0} (A) {1} (B)</td>\n".format(cratehvreada[aj],cratehvreadb)
        else:
            if cratestatusa[aj] == False:
                if cratehvreada[aj] > 0:
                    readentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0}</span></td>\n".format(cratehvreada[aj])
                else:
                    readentry = "<td style=\"white-space: nowrap;\">{0}</td>\n".format(cratehvreada[aj])
            else:
                if (abs(cratehvreada[aj] - cratehvnominala[aj]) > 50) & (cratestatusa[aj] != False):
                    readentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0}</span></td>\n".format(cratehvreada[aj])
                else:
                    readentry = "<td style=\"white-space: nowrap;\">{0}</td>\n".format(cratehvreada[aj])
        htmltable.write(readentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>Current read</b></td>\n")

    for ak in range(0,numberofcrates):
        if ak == 16:
            if (cratestatusa[ak] == False) | (cratestatusb == False):
                if (cratecurrentreada[ak] > 0) | (cratecurrentreadb > 0):
                    currententry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0} (A) {1} (B)</span></td>\n".format(cratecurrentreada[ak],cratecurrentreadb)
                else:
                    currententry = "<td style=\"white-space: nowrap;\">{0} (A) {1} (B)</td>\n".format(cratecurrentreada[ak],cratecurrentreadb)
            else:
                if ((cratecurrentreada[ak] > 60) | (cratecurrentreada[ak] < 45)):
                    if ((cratecurrentreadb > 60) | (cratecurrentreadb < 45)):
                        currententry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0} (A) {1} (B)</span></td>\n".format(cratecurrentreada[ak],cratecurrentreadb)
                    else:
                        currententry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0} (A)</span> {1} (B)</td>\n".format(cratecurrentreada[ak],cratecurrentreadb)
                else:
                    if ((cratecurrentreadb > 60) | (cratecurrentreadb < 45)):
                        currententry = "<td style=\"white-space: nowrap;\">{0} (A) <span style=\"color:#FF0000;\">{1} (B)</span></td>\n".format(cratecurrentreada[ak],cratecurrentreadb)
                    else:
                        currententry = "<td style=\"white-space: nowrap;\">{0} (A) {1} (B)</td>\n".format(cratecurrentreada[ak],cratecurrentreadb)
        else:
            if cratestatusa[ak] == False:
                if cratecurrentreada[ak] > 0:
                    currententry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0}</span></td>\n".format(cratecurrentreada[ak])
                else:
                    currententry = "<td style=\"white-space: nowrap;\">{0}</td>\n".format(cratecurrentreada[ak])
            else:
                if ((cratecurrentreada[ak] > 60) | (cratecurrentreada[ak] < 45)):
                    currententry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0}</span></td>\n".format(cratecurrentreada[ak])
                else:
                    currententry = "<td style=\"white-space: nowrap;\">{0}</td>\n".format(cratecurrentreada[ak])
        htmltable.write(currententry)

    htmltable.write("</tr>\n")
    htmltable.write("</tbody>\n")
    htmltable.write("</table>\n")
    htmltable.write("\n")
    htmltable.write("<br>\n")
    htmltable.write("\n")
    htmltable.write("<b>Crate Low Voltages</b><br>\n")
    htmltable.write("<table class=\"table table-striped table-condensed\">\n")
    htmltable.write("<tbody><tr>\n")
    htmltable.write("<th></th>\n")
    htmltable.write("<th style=\"white-space: nowrap;\">&nbsp;</th>\n")

    for al in range(0, numberofcrates):
        cratelventry = "<th style=\"white-space: nowrap;\">{0}</th>\n".format(crateid[al])
        htmltable.write(cratelventry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>+8V current</b></td>\n")

    for am in range(0, numberofcrates):
        htmltable.write("<th style=\"white-space: nowrap;\"></th>\n")

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>+5V current</b></td>\n")

    for an in range(0, numberofcrates):
        htmltable.write("<th style=\"white-space: nowrap;\"></th>\n")

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>-5V current</b></td>\n")

    for ao in range(0, numberofcrates):
        htmltable.write("<th style=\"white-space: nowrap;\"></th>\n")

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>Voltage OK</b></td>\n")

    for ap in range(0, numberofcrates):
        htmltable.write("<th style=\"white-space: nowrap;\"></th>\n")

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>Temperature OK</b></td>\n")

    for aq in range(0, numberofcrates):
        htmltable.write("<th style=\"white-space: nowrap;\"></th>\n")

    htmltable.write("</tr>\n")
    htmltable.write("</tbody>\n")
    htmltable.write("</table>\n")
    htmltable.write("\n")
    htmltable.write("<br>\n")
    htmltable.write("\n")
    htmltable.write("<b>XL3 ErrorPacket</b><br>\n")
    htmltable.write("<table class=\"table table-striped table-condensed\">\n")
    htmltable.write("<tbody><tr>\n")
    htmltable.write("<th></th>\n")
    htmltable.write("<th style=\"white-space: nowrap;\">&nbsp;</th>\n")
    
    for ar in range(0, numberofcrates):
        cratexl3errorentry = "<th style=\"white-space: nowrap;\">{0}</th>\n".format(crateid[ar])
        htmltable.write(cratexl3errorentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>cmdRejected</b></td>\n")

    for at in range(0, numberofcrates):
        if xl3errorcmdrejected[at] != 0:
            cmdentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0}</span></td>\n".format(xl3errorcmdrejected[at])
        else:
            cmdentry = "<td style=\"white-space: nowrap;\">{0}</td>\n".format(xl3errorcmdrejected[at])
        htmltable.write(cmdentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>transferError</b></td>\n")

    for au in range(0, numberofcrates):
        if xl3errorpackettransfererror[au] != 0:
            transferentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0}</span></td>\n".format(xl3errorpackettransfererror[au])
        else:
            transferentry = "<td style=\"white-space: nowrap;\">{0}</td>\n".format(xl3errorpackettransfererror[au])
        htmltable.write(transferentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>xl3DataAvailUnknown</b></td>\n")

    for av in range(0, numberofcrates):
        if xl3errorpacketxl3dataavailunknown[av] != 0:
            xl3dataentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0}</span></td>\n".format(xl3errorpacketxl3dataavailunknown[av])
        else:
            xl3dataentry = "<td style=\"white-space: nowrap;\">{0}</td>\n".format(xl3errorpacketxl3dataavailunknown[av])
        htmltable.write(xl3dataentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>fecBundleReadError</b></td>\n")

    for aw in range(0, numberofcrates):
        if xl3errorpacketfecbundlereaderror[aw] != 0:
            bundlereadentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0}</span></td>\n".format(xl3errorpacketfecbundlereaderror[aw])
        else:
            bundlereadentry = "<td style=\"white-space: nowrap;\">{0}</td>\n".format(xl3errorpacketfecbundlereaderror[aw])
        htmltable.write(bundlereadentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>fecBundleResynchError</b></td>\n")

    for ax in range(0, numberofcrates):
        if xl3errorpacketfecbundleresyncherror[ax] != 0:
            bundleresynchentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0}</span></td>\n".format(xl3errorpacketfecbundleresyncherror[ax])
        else:
            bundleresynchentry = "<td style=\"white-space: nowrap;\">{0}</td>\n".format(xl3errorpacketfecbundleresyncherror[ax])
        htmltable.write(bundleresynchentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\"&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>fecMemLevelUnknown</b></td>\n")

    for ay in range(0, numberofcrates):
        if xl3errorpacketfecmemlevelunknown[ay] != 0:
            memlevelentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0}</span></td>\n".format(xl3errorpacketfecmemlevelunknown[ay])
        else:
            memlevelentry = "<td style=\"white-space: nowrap;\">{0}</td>\n".format(xl3errorpacketfecmemlevelunknown[ay])
        htmltable.write(memlevelentry)

    htmltable.write("</tr>\n")
    htmltable.write("</tbody>\n")
    htmltable.write("</table>\n")
    htmltable.write("\n")
    htmltable.write("<br>\n")
    htmltable.write("\n")
    htmltable.write("<b>XL3 ScrewedPacket</b><br>\n")
    htmltable.write("<table class=\"table table-striped table-condensed\">\n")
    htmltable.write("<tbody><tr>\n")
    htmltable.write("<th></th>\n")
    htmltable.write("<th style=\"white-space: nowrap;\">&nbsp;</th>\n")
    
    for az in range(0, numberofcrates):
        xl3screwedentry = "<th style=\"white-space: nowrap;\">{0}</th>\n".format(crateid[az])
        htmltable.write(xl3screwedentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>fecScrewed</b></td>\n")

    for ba in range(0, numberofcrates):
        if xl3screwedpacketfecscrewed[ba] != 0:
            screwedentry = "<td style=\"white-space: nowrap;\"><span style=\"color:#FF0000;\">{0}</span></td>\n".format(xl3screwedpacketfecscrewed[ba])
        else:
            screwedentry = "<td style=\"white-space: nowrap;\">{0}</td>\n".format(xl3screwedpacketfecscrewed[ba])
        htmltable.write(screwedentry)

    htmltable.write("</tr>\n")
    htmltable.write("</tbody>\n")
    htmltable.write("</table>\n")
    htmltable.write("<br>\n")
    htmltable.write("\n")
    htmltable.write("<b>Compensation coils</b><br>\n")
    htmltable.write("<table class=\"table table-striped table-condensed\">\n")
    htmltable.write("<tbody><tr>\n")
    htmltable.write("<th></th>\n")
    htmltable.write("<th style=\"white-space: nowrap;\">&nbsp;</th>\n")
    
    for bb in range(0, numberofcompcoils):
        compcoilsentry = "<th style=\"white-space: nowrap;\">{0}</th>\n".format(compcoilname[bb])
        htmltable.write(compcoilsentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>Status</b></td>\n")

    for bc in range(0,numberofcompcoils):
        htmltable.write("<td style=\"white-space: nowrap;\"></td>\n")

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>Current</b></td>\n")

    for bd in range(0,numberofcompcoils):
        htmltable.write("<td style=\"white-space: nowrap;\"></td>\n")

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>Alarm</b></td>\n")

    for be in range(0,numberofcompcoils):
        htmltable.write("<td style=\"white-space: nowrap;\"></td>\n")

    htmltable.write("</tr>\n")
    htmltable.write("</tbody>\n")
    htmltable.write("</table>\n")
    htmltable.write("\n")
    htmltable.write("<b>Hold-up rope tensions</b><br>\n")
    htmltable.write("<table class=\"table table-striped table-condensed\">\n")
    htmltable.write("<tbody><tr>\n")
    htmltable.write("<th></th>\n")
    htmltable.write("<th style=\"white-space: nowrap;\">&nbsp;</th>\n")
    
    for bf in range(0, numberofholdupropes):
        holdupropeentry = "<th style=\"white-space: nowrap;\">{0}</th>\n".format(holdupropesid[bf])
        htmltable.write(holdupropeentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\">&nbsp;</td>\n")

    for bg in range(0,numberofholdupropes):
        htmltable.write("<td style=\"white-space: nowrap;\"></td>\n")

    htmltable.write("</tr>\n")
    htmltable.write("</tbody>\n")
    htmltable.write("</table>\n")
    htmltable.write("\n")
    htmltable.write("<br>\n")
    htmltable.write("\n")
    htmltable.write("<b>Hold-down rope tensions</b><br>\n")
    htmltable.write("<table class=\"table table-striped table-condensed\">\n")
    htmltable.write("<tbody><tr>\n")
    htmltable.write("<th></th>\n")
    htmltable.write("<th style=\"white-space: nowrap;\">&nbsp;</th>\n")

    for bh in range(0, numberofholddownropes):
        holddownropeentry = "<th style=\"white-space: nowrap;\">{0}</th>\n".format(holddownropesid[bh])
        htmltable.write(holddownropeentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\">&nbsp;</td>\n")
    
    for bi in range(0,numberofholddownropes):
        htmltable.write("<td style=\"white-space: nowrap;\"></td>\n")

    htmltable.write("</tr>\n")
    htmltable.write("</tbody>\n")
    htmltable.write("</table>\n")
    htmltable.write("\n")
    htmltable.write("<br>\n")
    htmltable.write("\n")
    htmltable.write("<b>Equator monitors</b><br>\n")
    htmltable.write("<table class=\"table table-striped table-condensed\">\n")
    htmltable.write("<tbody><tr>\n")
    htmltable.write("<th></th>\n")
    htmltable.write("<th style=\"white-space: nowrap;\">&nbsp;</th>\n")

    for bj in range(0, numberofequatormonitors):
        equatormonitorentry = "<th style=\"white-space: nowrap;\">{0}</th>\n".format(equatormonitorsid[bj])
        htmltable.write(equatormonitorentry)

    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\">&nbsp;</td>\n")

    for bk in range(0,numberofequatormonitors):
        htmltable.write("<td style=\"white-space: nowrap;\"></td>\n")

    htmltable.write("</tr>\n")
    htmltable.write("</tbody>\n")
    htmltable.write("</table>\n")
    htmltable.write("\n")
    htmltable.write("<br>\n")
    htmltable.write("\n")
    htmltable.write("<b>Cavity water</b><br>\n")
    htmltable.write("<table class=\"table table-striped table-condensed\">\n")
    htmltable.write("<tbody><tr>\n")
    htmltable.write("<th></th>\n")
    htmltable.write("<th style=\"white-space: nowrap;\"><b>Temperature</b></th>\n")
    htmltable.write("<th style=\"white-space: nowrap;\"></th>\n")
    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>Level</b></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"></td>\n")
    htmltable.write("</tr>\n")
    htmltable.write("</tbody>\n")
    htmltable.write("</table>\n")
    htmltable.write("\n")
    htmltable.write("<b>Deck</b><br>\n")
    htmltable.write("<table class=\"table table-striped table-condensed\">\n")
    htmltable.write("<tbody><tr>\n")
    htmltable.write("<th></th>\n")
    htmltable.write("<th style=\"white-space: nowrap;\"><b>Temperature</b></th>\n")
    htmltable.write("<th style=\"white-space: nowrap;\"></th>\n")
    htmltable.write("</tr>\n")
    htmltable.write("\n")
    htmltable.write("<tr>\n")
    htmltable.write("<td width=\"1%\"><div style=\"width: 16px; height: 14px\">&nbsp;</div></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"><b>Humidity</b></td>\n")
    htmltable.write("<td style=\"white-space: nowrap;\"></td>\n")
    htmltable.write("</tr>\n")
    htmltable.write("</tbody>\n")
    htmltable.write("</table>\n")
    htmltable.write("\n")
    htmltable.write("</div>\n")
    htmltable.write("\n")
    htmltable.write("</div>\n")
    htmltable.write("\n")
    htmltable.write("</div>\n")
    htmltable.write("</body>\n")
    htmltable.write("</html>\n")
    
    htmltable.close()
