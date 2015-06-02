"""chstools.py
This code has some tools to access the channel hardware
status and to create the SNO-style dqxx file
for the specified runnumber. It is work in progress
as many DQXX definitions are not yet available in
the ORCA configuration file.

Author: Freija Descamps
         <fbdescamps@lbl.gov>
 Inspired by dqxx_view.js script by Andy Mastbaum
"""

import getpass
import argparse
import httplib
import json
import sys

# The SNO definition of DQXX. The 'in_use' flag denotes if we
# are actually reading this info from the ORCA configuration
# file at this time.
DQXX_DEFINITION = [
    # ['bit', 'Short description', 'In use? 1=yes, 0= no']
    [0, 'CRATE', False],
    [1, 'SLOT OP', True],
    [2, 'GT', False],
    [3, 'CR ONLINE', True],
    [4, 'CR HV', True],
    [8, 'Card MB', True],
    [9, 'DC', True],
    [10, 'DAQ', False],
    [16, 'SEQUENCER', False],
    [17, '100NS', False],
    [18, '20NS', False],
    [19, 'VTHR MAX', True],
    [20, 'QINJ', False],
    [21, 'N100', False],
    [22, 'N20', False],
    [24, 'PMTIC', False],
    [26, 'RELAY HV', True],
    [27, 'RESISTOR', False],
    [28, 'CABLE', False],
    [29, '75OHM', False],
    [30, 'NOT OP', False]
]


def check_bit(word, n):
    """Function that returns True if the n'th bit is set in the word.
    :param word: The word to check.
    :param n: The position of the bit to check, starting counting from 0.
    :returns: A Boolean True if n'th bit is set in word, False if not.
    """
    # The mask has the n'th bit set to 1
    mask = 2 ** n
    return (word & mask) > 0


def count_bits(dqxx, n):
    """Function that returns the number of channels that have bit n set.
    :param dqxx: A list of 9728 DQXX words (one per channel)
    :param n: The position of the bit to check, starting counting from 0.
    :returns: An integer which is the total number of channels that have bit n set.
    """
    return sum([check_bit(x, n) for x in dqxx])


def is_tube_online(dqxx, lcn):
    """Function that returns a boolean array defining if Tube is online or not.
    :param dqxx: A list of 9728 DQXX words (one per channel).
    :param lcn: The logical channel number for the channel in question.
    :returns: A Boolean True if tube is online, False if not.
    """
    tube_online_mask = 0x5D09071D  # This is the SNO definition of 'online'
    return (dqxx[lcn] & tube_online_mask) == tube_online_mask


def count_offline_tubes(dqxx):
    """Function that returns the number of offline channels.
    :param dqxx: A list of 9728 DQXX words (one per channel)
    :returns: An integer which is the total number of channels that are offline.
    """
    count = 0
    for lcn in range(0, len(dqxx)):
        if not is_tube_online(dqxx, lcn):
            count = count + 1
    return count


def form_dqxx_word(dqcr, dqch):
    """Function to form the DQXX bitmaps that show the detector status.
    :param dqcr: A list of 9728 DQCR words (one per channel)
    :param dqch: A list of 9728 DQCH words (one per channel)
    :returns: A list of 9728 combined DQXX words (one per channel)

    Definition of the DQXX words is as follows:
    (see also docdb 458)
    #####
    # 0 Crate CRATE Crate present = DQCR[0]
    # 1 SLOT OP Slot operational = DQCR[8]
    # 2 GT Crate receiving global triggers = DQCR[9]
    # 3 CR ONLINE Crate is being read out by ECPU = DQCR[10]
    # 4 CR HV Crate present with HV = DQCR[11]
    # 7 Reserved. Always set if status defined.
    # 8 Card MB Mother Board present = DQCR[1]
    # 9 DC Daughter Card present = DQCR[4-7]
    # 10 DAQ DAQ readout on-line = DQCR[3]
    # 16 Channel SEQUENCER Channel sequencer enabled = DQCH[2]
    # 17 100NS 100ns trigger enabled = DQCH[3]
    # 18 20NS 20 ns trigger enabled = DQCH[4]
    # 19 VTHR MAX V threshold < 255 = DQCH[16-23]
    # 20 QINJ Qinj OK = DQCH[6]
    # 21 N100 100ns trigger OK = DQCH[7]
    # 22 N20 20 ns trigger OK = DQCH[8]
    # 24 PMT PMTIC PMTIC present = DQCR[2]
    # 26 RELAY HV relay on = DQCR[12-15]
    # 27 PMTIC RESISTOR PMTIC channel resistor present = DQCH[1]
    # 28 PMT CABLE PMT cable in = DQCH[0]
    # 29 75OHM 75 Ohm terminator OK = DQCH[5]
    # 30 NOT OP Not operational from SHaRC DB = DQCH[9]
    # 31 Reserved for the undefined value (just this bit set).
    """
    # Loop over all channels and form the DQXX word
    dqxx = [0 for i in range(19 * 16 * 32)]
    for lcn in range(len(dqxx)):
        dqch_word = dqch[lcn]
        # get the crate number
        crate = (lcn & 0x3e00) >> 9
        # get the card number
        card = (lcn & 0x1e0 ) >> 5
        dqcr_word = dqcr[crate * 16 + card]
        # get the channel number
        ch = lcn & 0x1f
        # Get the daughterboard number for this channel
        db = ch / 8
        dqxx_word = 0
        # 0 DQXX[0] = DQCR[0]
        dqxx_word |= ((not check_bit(dqcr_word, 0)) << 0)
        # 1 DQXX[1] = DQCR[8]
        dqxx_word |= ((not check_bit(dqcr_word, 8)) << 1)
        # 2 DQXX[2] = DQCR[9]
        dqxx_word |= ((not check_bit(dqcr_word, 9)) << 2)
        # 3 DQXX[3] = DQCR[10]
        dqxx_word |= ((not check_bit(dqcr_word, 10)) << 3)
        # 4 DQXX[4] = DQCR[11]
        dqxx_word |= ((not check_bit(dqcr_word, 11)) << 4)
        # 8 DQXX[8] = DQCR[1]
        dqxx_word |= ((not check_bit(dqcr_word, 1)) << 8)
        # 9 DQXX[9] = DQCR[4+db]
        dqxx_word |= ((not check_bit(dqcr_word, 4 + db)) << 9)
        # 10 DQXX[10] = DQCR[3]
        dqxx_word |= ((not check_bit(dqcr_word, 3)) << 10)
        # 16 DQXX[16] = DQCH[2]
        dqxx_word |= ((not check_bit(dqch_word, 2)) << 16)
        # 17 DQXX[17] = DQCH[3]
        dqxx_word |= ((not check_bit(dqch_word, 3)) << 17)
        # 18 DQXX[18] = DQCH[4]
        dqxx_word |= ((not check_bit(dqch_word, 4)) << 18)
        # 19 check for maxed-out threshold ( value of 255 )
        threshold = (dqch_word & 0xff0000) >> 16
        if not (threshold == 255):
            dqxx_word |= (1 << 19)
        # 20 DQXX[20] = DQCH[6]
        dqxx_word |= ((not check_bit(dqch_word, 6)) << 20)
        # 21 DQXX[21] = DQCH[7]
        dqxx_word |= ((not check_bit(dqch_word, 7)) << 21)
        # 22 DQXX[22] = DQCH[8]
        dqxx_word |= ((not check_bit(dqch_word, 8)) << 22)
        # 24 DQXX[24] = DQCR[2]
        dqxx_word |= ((not check_bit(dqcr_word, 2)) << 24)
        # 26 DQXX[26] = DQCR[12+db]
        dqxx_word |= ((not check_bit(dqcr_word, (12 + db))) << 26)
        # 27 DQXX[27] = DQCH[1]
        dqxx_word |= ((not check_bit(dqch_word, 1)) << 27)
        # 28 DQXX[28] = DQCH[0]
        dqxx_word |= ((not check_bit(dqch_word, 0)) << 28)
        # 29 DQXX[29] = DQCH[5]
        dqxx_word |= ((not check_bit(dqch_word, 5)) << 29)
        # 30 DQXX[30] = DQCH[9]
        dqxx_word |= ((not check_bit(dqch_word, 9)) << 30)
        dqxx[lcn] = dqxx_word
    return dqxx


def get_run_configuration_from_db(runnumber, db_server, db_username, db_password):
    """Function to retrieve the ORCA runconfiguration document
    from the snoplus database.
    :param: The run-number (int).
    :param: The username for the snoplus database (string).
    :param: The password for the snoplus database (string).
    :returns: The ORCA run configuration data for specified run-number.
    """
    # Contact the snoplus ORCA database to retrieve the run configuration file
    # for the requested run
    auth = db_username + ":" + db_password
    request_url = '/orca/_design/OrcaViews/_view/viewConfigDocByRunNumber?descending=true&include_docs=true&startkey=%s&endkey=%s' % (runnumber, runnumber)
    request_headers = {'Content-type': "application/json"}
    request_headers['Authorization'] = 'Basic {}'.format(auth.encode('base64'))
    connection = httplib.HTTPConnection(db_server)
    connection.request('GET', request_url, headers=request_headers)
    try:
        data = json.loads(connection.getresponse().read())
    except ValueError, e:
        sys.stderr.write("Failed to contact database, try again\n")
        sys.exit(1)
    rows = data['rows']
    # Check if there is data available for this run
    if len(rows) == 0:
        sys.stderr.write("No ORCA data for this run\n")
        sys.exit(1)
    return data


def create_dqcr_dqch_dqid(runnumber, data):
    """Function that creates the dqcr, dqch and dqid words for runnumber.
    :param: The run-number (int).
    :param: The ORCA run configuration data for specified run-number.
    :returns: dqcr: A list of 9728 DQCR words (one per channel).
    :returns: dqch: A list of 9728 DQCH words (one per channel).
    :returns: dqid: A list of 1824 DQID words (6 per FEC card).
    """
    # Get the mtc, xl3 and fec information from the run configuration data
    rows = data['rows']
    for value in rows:
        mtc = value['doc']['mtc']
        xl3s = value['doc']['xl3s']
        fecs = value['doc']['fec32_card']
    # Create the arrays that will hold the dqid, dqcr and dqch info
    dqid = [0x0 for i in range(19 * 96)]
    dqcr = [0x0 for i in range(19 * 16)]
    dqch = [0x0 for i in range(19 * 16 * 32)]
    # Now loop over crate/card/channel and fill the DQID, DQCR and DQCH words
    for crate in range(0, 19):
        for card in range(0, 16):
            dqcr_word = 0
            if len(fecs.get(str(crate))[str(card)]) > 0:
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
            xl3com = len(xl3s.get(str(crate))) == 0
            dqcr_word |= (xl3com << 0)
            # 1   MB           MB present(0), not present(1)
            #                  If the board id cannot be read, assume board not present
            #  Just check if ID is not "0x0"
            if len(fecs.get(str(crate))[str(card)]) > 0:
                mbPresent = (fecs.get(str(crate))[str(card)]['mother_board']['mother_board_id'] == "0")
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
            slotNormal = ((xl3s.get(str(crate))["xl3_mode"]) == "2")
            dqcr_word |= (slotNormal << 3)
            # 4   DC           Daughter cards all present(0), 4 bit mask of present DC
            #                  Channel i associated with DC at bit DC + i/8
            #                  If the board id cannot be read, assume not present
            for db in range(0, 4):
                if len(fecs.get(str(crate))[str(card)]) > 0:
                    dbPresent = (fecs.get(str(crate))[str(card)]["daughter_board"][str(db)]["daughter_board_id"] == "0")
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
                relay_word = int((xl3s.get(str(crate))["hv_relay_low_mask"]) >> (card * 4)) & 0xf
                relay_word = ~relay_word & 0xf
            else:
                relay_word = int((xl3s.get(str(crate))["hv_relay_high_mask"]) >> ((card - 8) * 4)) & 0xf
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
            # The xl3 value is not in ADC counts but in actual Volts so do a conversion:
            readHV = int(4095.0 * xl3s.get(str(crate))["hv_voltage_read_value_a"] / 3000)
            dqcr_word |= (readHV << 16)
            # 11   CR_HV        or of bit 0 (SNO crate present) and bits 16-31 (HV bits).
            crate_hv = not((dqcr_word & 0x1) | readHV > 0)
            dqcr_word |= (crate_hv << 11)
            # Now time for DQCH = channel-dependent status word...
            # We can only get this info if the FEC card object exists
            for ch in range(0, 32):
                # Find out which DB this channel is on
                db_index = int(ch / 8)
                # Find out which channel this is on the DB in question
                db_channel = ch % 8
                if len(fecs.get(str(crate))[str(card)]) > 0:
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
                    # n100 = not( int(fecCards.get(str(crate))[str(card)]["mother_board"]["trigger_100ns_mask"]) >> ch) & 0x1;
                    n100 = 0
                    dqch_word |= (n100 << 3)
                    # 4: N20 enabled
                    # FIXME (Freija) This seems to be always 1 (disabled).. will set to 0 by default for now.
                    # Uncomment the next line when this is fixed...
                    # n20 = not(int(fecs.get(str(crate))[str(card)]["mother_board"]["trigger_100ns_mask"]) >> ch) & 0x1;
                    n20 = 0
                    dqch_word |= (n20 << 4)
                    # 10: Bad (or of bits 0-9)
                    bad = ((dqch_word & 0x511) > 0)
                    dqch_word |= (bad << 10)
                    # 16-23: vthr
                    vthr = int(fecs.get(str(crate))[str(card)]["daughter_board"][str(db_index)]["vt"][str(db_channel)])
                    dqch_word |= ((vthr & 0xff) << 16)
                    # 24-31: vthr zero
                    vthr_zero = int(fecs.get(str(crate))[str(card)]["daughter_board"][str(db_index)]["vt_zero"][str(db_channel)])
                    dqch_word |= ((vthr_zero & 0xff) << 24)
                else:
                    dqch_word = 0x0
                dqch[(crate * 16 * 32) + (card * 32) + ch] = dqch_word
            dqcr[(crate * 16) + card] = dqcr_word
    return dqcr, dqch, dqid


def dqxx_write_to_file(dqcr, dqch, dqid, runnumber, outfilename):
    """Function that writes out the SNO-style DQXX file.
    :param: dqcr: A list of 304 DQCR words (one per FEC card).
    :param: dqch: A list of 9728 DQCH words (one per channel).
    :param: dqid: A list of 1824 DQID words (6 per FEC card).
    :param: The run-number.
    :returns: None.
    """
    # RAT has an issue with reading in the dqch integer array,
    # therefore, we are manually writing out the file for now:
    runrange = "run_range: [%i, 100000]," % (runnumber)
    f = open(outfilename, 'w')
    f.write(' {\n name: "PMT_DQXX",\n ')
    f.write( runrange )
    f.write('\n pass: 0,\n')
    f.write(' comment: "",\n')
    f.write(' production: 1,\n')
    # The following variables are zero by default for now? (Freija)
    f.write(' cratestatus_n100: 0,\n cratestatus_n20: 0, \n cratestatus_esumL: 0, ')
    f.write(' \n cratestatus_esumH: 0,\n cratestatus_owlN: 0, \n cratestatus_owlEL: 0, ')
    f.write(' \n cratestatus_owlEH: 0,')
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
    for x in range(0, 19 * 16):
        f.write(str(hex(dqcr[x])))
        f.write(', ')
    f.write('],\n }')
