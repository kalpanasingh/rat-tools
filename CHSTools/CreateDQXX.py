#!/usr/bin/env python
#######################
#
# CreateDQXX.py
# This code will output a PMT_DQXX ratdb file
# for the specified runnumber. It is work in progress
# as many DQXX definitions are not yet available in
# the ORCA configuration file.
#
# Author: Freija Descamps
#         <fbdescamps@lbl.gov>
#
#######################

import getpass
import argparse
import httplib
import json
import sys

def create_dqxx(runnumber):
    """

    Create the DQXX file for runnumber.
    Input is the runnumber

    """
    # First, get the Db username and password from the user
    # database server
    db_user = raw_input("[%s] Username: " % db_server)
    db_pswd = getpass.getpass("[%s] Password: " % db_server)
    auth = db_user + ":" + db_pswd
    request_url = '/orca/_design/OrcaViews/_view/viewConfigDocByRunNumber?descending=true&include_docs=true&startkey=%s&endkey=%s' % (runnumber, runnumber)
    request_headers = {'Content-type': "application/json"}
    request_headers['Authorization'] = 'Basic {}'.format(auth.encode('base64'))
    connection = httplib.HTTPConnection(db_server)
    connection.request('GET', request_url, headers=request_headers)
    try:
        data = json.loads(connection.getresponse().read())
    except ValueError, e:
        print "Failed to contact database, try again"
        sys.exit()            
    rows = data['rows']
    if len(rows) == 0:
        print "No ORCA data for this run"
        return
    # Get the mtc, xl3 and fec information
    for value in rows:
        mtc = value['doc']['mtc']
        xl3s = value['doc']['xl3s']
        fecs = value['doc']['fec32_card']
    # Create the arrays that will hold the dqid, dqcr and dqch info
    dqid = [0 for i in range(19 * 96)]
    dqcr = [0 for i in range(19 * 16 * 32)]
    dqch = [0 for i in range(19 * 16 * 32)]
    # Now loop over crate/card/channel and fill the DQID, DQCR and DQCH words
    for crate in range(0, 19):
        for card in range(0, 16):
            dqcr_word = 0
            if len(fecs[str(crate)][str(card)]) > 0:
                dqid[(crate * 96) + (card * 6)] = hex(int(fecs[str(crate)][str(card)]['mother_board']['mother_board_id'], 16))
                dqid[(crate * 96) + (card * 6) + 1] = hex(int("0x0", 16))
                for db in range(0, 4):
                    dqid[(crate * 96) + (card * 6) + 2 + db] = hex(int(fecs[str(crate)][str(card)]['daughter_board'][str(db)]['daughter_board_id'], 16))
            else:
                # The DQIDs will be zero in this case
                print "Warning: no FEC info for crate/card " + str(crate) + "/" + str(card)
            # Time for DQCR!
            # 0   CRATE        Crate present present(0), not present(1)
            # SNO+ : this is now replaced with: XL3 communicating.
            # FIXME (Freija): not available in ORCA database for so I am just checking to see if
            # there is XL3 info present... this might just be always the case though.
            xl3com = not(len(xl3s[str(crate)]) > 0)
            dqcr_word |= (xl3com << 0)
            # 1   MB           MB present(0), not present(1)
            #                  If the board id cannot be read, assume board not present
            #  Just check if ID is not "0x0"
            if len(fecs[str(crate)][str(card)]) > 0:
                mbPresent = (fecs[str(crate)][str(card)]['mother_board']['mother_board_id'] == "0")
            else:
                mbPresent = 1
            dqcr_word |= (mbPresent << 1)
            # 2   PMTIC        PMTIC present(0), not present(1)
            #                  If the board id cannot be read, assume board not present
            # FIXME (Freija) PMTIC ID is not available. For now, leave as present=hardcoded for now
            pmticPresent = 0
            dqcr_word |= (pmticPresent << 2)
            # 3   DAQ          DAQ readout (eCPU) online(0), offline(1)
            # SNO+ - Crate is in Normal Mode (0->normal mode, 1-> not-normal mode).
            # Modes: 1=init, 2=normal, 3:cgt (no one seems to know what this last one means?)
            slotNormal = ((xl3s[str(crate)]["xl3_mode"]) == "2")
            dqcr_word |= (slotNormal << 3)
            # 4   DC           Daughter cards all present(0), 4 bit mask of present DC
            #                  Channel i associated with DC at bit DC + i/8
            #                  If the board id cannot be read, assume not present
            for db in range(0, 4):
                if len(fecs[str(crate)][str(card)]) > 0:
                    dbPresent = (fecs[str(crate)][str(card)]["daughter_board"][str(db)]["daughter_board_id"] == "0")
                else:
                    dbPresent = 1
                dqcr_word |= (mbPresent << 4 + db)
            # 9   GT           GT mask for crate, i.e., is this crate receiving
            #                  global triggers? yes = 0, no =1
            # The GT mask is now a bitmask
            crMask = (1 << crate)
            gtMask = not(crMask & int(mtc["gt_mask"]))
            # FIXME (Freija) The GT mask is not being written out correctly at the moment
            # Default to always masked in for now
            # dqcr_word |= (gtMask << 9)
            dqcr_word |= (0 << 9)
            # 10   CR_ONLINE   Crate on-line (i.e., is being read out by ECPU)
            # New definition: is the crate initialized. FIXME (Freija): this is not available in
            # configuration file.
            dqcr_word |= (0 << 10)
            # 12   RELAY        HV relays all on(0), 4 bit mask of relays on
            # The status of the HV relays come in two words: hv_relay_high_mask and hv_relay_low_mask
            # So cards 0-7 are defined in the low mask and 8-15 in the high mask.
            relay_word = 0
            if card < 8:
                # As a reminder: '0' means that the relay is closed...
                relay_word = int((xl3s[str(crate)]["hv_relay_low_mask"]) >> (card * 4)) & 0xf
                relay_word = ~relay_word & 0xf
            else:
                relay_word = int((xl3s[str(crate)]["hv_relay_high_mask"]) >> ((card - 8) * 4)) & 0xf
                relay_word = ~relay_word & 0xf
            dqcr_word |= (relay_word << 12)
            # 8   SLOT_OP      OR of bits 0-7, 12-15.
            #                  This is deemed to mean, 'slot operational', as it is
            #                  an OR of crate, slot, db, etc operational.
            # FIXME (Freija) I do not see why an entire slot is un-operational if one HV relay is off?
            # Or when a DB is missing?
            # In any case, this just comes down to checking if dqcr_word is zero at this point
            slotOp = not(dqcr_word == 0)
            dqcr_word |= (slotOp << 8)
            # 16   HV           HV for this card. 12 bits (0-4095)
            # This is now in the xl3 information as hv_voltage_read_value_a or hv_voltage_read_value_b
            # This is not in ADC counts but in actual Volts
            readHV = int(xl3s[str(crate)]["hv_voltage_read_value_a"])
            dqcr_word |= (readHV << 16)
            # 11   CR_HV        or of bit 0 (SNO crate present) and bits 16-31 (HV bits).
            crate_hv = not((dqcr_word & 0x1) | readHV > 0)
            dqcr_word |= (crate_hv << 11)
            # Now time for DQCH = channel-dependent status word...
            # We can pnly get this info if the FEC card object exists
            for ch in range(0, 32):
                # Find out which DB this channel is on
                db_index = int(ch / 8)
                # Find out which channel this is on the DB in question
                db_channel = ch % 8
                if len(fecs[str(crate)][str(card)]) > 0:
                    # 0, 1, 5, 6, 7, 8, 9: All zero, meaning present & operating
                    dqch_word = 0
                    # 2 : sequencer
                    # FIXME (Freija) This seems to be always 1 (disabled).. will set to 0 by default for now.
                    # Uncomment the next line when this is fixed...
                    # sequencer = not(int(fecs[str(crate)][str(card)]["mother_board"]["sequencer_mask"]) >> ch) & 0x1;
                    sequencer = 0
                    dqch_word |= (sequencer << 2)
                    # 3: N100 enabled
                    # FIXME (Freija) This seems to be always 1 (disabled).. will set to 0 by default for now.
                    # Uncomment the next line when this is fixed...
                    # n100 = not( int(fecCards[str(crate)][str(card)]["mother_board"]["trigger_100ns_mask"]) >> ch) & 0x1;
                    n100 = 0
                    dqch_word |= (n100 << 3)
                    # 4: N20 enabled
                    # FIXME (Freija) This seems to be always 1 (disabled).. will set to 0 by default for now.
                    # Uncomment the next line when this is fixed...
                    # n20 = not(int(fecs[str(crate)][str(card)]["mother_board"]["trigger_100ns_mask"]) >> ch) & 0x1;
                    n20 = 0
                    dqch_word |= (n20 << 4)
                    # 10: Bad (or of bits 0-9)
                    bad = ((dqch_word & 0x511) > 0)
                    dqch_word |= (bad << 10)
                    # 16-23: vthr
                    vthr = int(fecs[str(crate)][str(card)]["daughter_board"][str(db_index)]["vt"][str(db_channel)])
                    dqch_word |= ((vthr & 0xff) << 16)
                    # 24-31: vthr zero
                    vthr_zero = int(fecs[str(crate)][str(card)]["daughter_board"][str(db_index)]["vt_zero"][str(db_channel)])
                    dqch_word |= ((vthr_zero & 0xff) << 24)
                else:
                    dqch_word = 0
                dqch[(crate * 16 * 32) + (card * 32) + ch] = dqch_word
                dqcr[(crate * 16 * 32) + (card * 32) + ch] = dqcr_word
    # Write out the dqid, dqcr and dqch to the outputfile
    outfilename = "PMT_DQXX_%i.ratdb" % int(runnumber)
    f = open(outfilename, 'w')
    f.write('{\n name: "PMT_DQXX",\n valid_begin: [0,0], \n valid_end: [0,0], \n')
    # The following variables are zero by default? (Freija)
    f.write(' cratestatus_n100: 0, \n cratestatus_n20: 0, \n cratestatus_esumL: 0, \n cratestatus_esumH: 0,\n cratestatus_owlN: 0, \n cratestatus_owlEL: 0, \n cratestatus_owlEH: 0,')
    f.write('\n\n dqid : [ ')
    for x in range(0, 19 * 96):
        f.write(str(dqid[x]))
        f.write(', ')
    f.write('],\n')
    f.write('\n dqch : [ ')
    for x in range(0, 19 * 16 * 32):
        f.write(str(hex(dqch[x])))
        f.write(', ')
    f.write('],\n ')
    f.write('\n dqcr : [ ')
    for x in range(0, 19 * 16 * 32):
        f.write(str(hex(dqcr[x])))
        f.write(', ')
    f.write('],\n }')
    print "Created " + outfilename
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="runnumber", help="Run number", default="0")
    args = parser.parse_args()
    if args.runnumber == "0":
        print "Please supply a runnumber using \'-n\'"
    if int(args.runnumber) < 8300:
        print "Please supply a runnumber larger than 8300 (December 2014 dark running)"
    else:
        print "Assembling DQXX info for run " + args.runnumber
        create_dqxx(args.runnumber)