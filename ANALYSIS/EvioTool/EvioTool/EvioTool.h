/*
 *  EvioTool.h
 *  EvioTool
 *
 *  Created by Maurik Holtrop on 4/19/14.
 *  Copyright (c) 2014 UNH. All rights reserved.
 *
 */

#ifndef EvioTool_
#define EvioTool_

// #define EVIO_V4_0

/* The classes below are exported */
#pragma GCC visibility push(default)

#ifndef __clang__
#define nullptr  NULL
#endif

// -- Include the EVIO headers -- //
#ifndef __CINT__                  // CINT is not able to parse the horrible EVIO gobledigook.

#include <stdio.h>
#include <string.h>

#include <iostream>
#include <fstream>
#include <stdint.h>
#include "evio.h"
#include "evioUtil.hxx"
#include "evioFileChannel.hxx"
#include "evioDictionary.hxx"
using namespace evio;
#endif

#include <vector>
using namespace std;

#include "EvioEvent.h"

#ifndef __CINT__
#include "et.h"
#endif

class EvioTool
{
public:
  int fDebug;
  int MaxBuff;    // Size of the evioFileChannel buffer. Must contain entire event.
  
public:
  EvioTool(const char *filename=nullptr, const char *dict_filename=nullptr);
  ~EvioTool();
  void init(void);
  const unsigned int *getBuffer(void);
  int  getBufSize(void);
  void open(const char *filename, const char *dict_filename=nullptr);
  int openEv(char *filename);
#ifdef EVIO_V4_0
  int ReadNoCopy(int handle,const unsigned int **buffer,int *buflen);
#else
  int ReadNoCopy(int handle,const unsigned int **buffer,unsigned int *buflen);
#endif
  int  openEt(const char *et_file_name="",int port=0,int prescale=1);
  int  parse(EVIO_Event_t *evt,const unsigned int *buff=nullptr);
  void parseDictionary(const char *dictf);
  void printDictionary(void);
  bool read();
  
public:
  int run_number;
  int start_time;
  int file_number;

  string et_station_name;
  string et_host_name;
  int    et_port;
  string et_file_name;
  bool   et_is_blocking;
  int    et_mode;  // ET_HOST_AS_LOCAL(1) or ET_HOST_AS_REMOTE(0) - set the mode behavior.
  int    et_que_size;
  int    et_pre_scale;
  int    et_receive_buffer_size;
  int    et_send_buffer_size;
  int    et_nodelay;
  int    et_events_chunk;
  unsigned int *et_data;
  size_t et_data_len;

  static const int EVENT_PRESTART=17;
  static const int EVENT_GO=18;

  static const int ECAL_FADC_MASTER=46;
  static const int ECAL_FADC_CRATE1=37;
  static const int ECAL_FADC_CRATE2=39;
  static const int ECAL_FADC_GTP1=38;
  static const int ECAL_FADC_GTP2=40;
  static const int EVENT_HEADER=49152;
  static const int ECAL_INTEGRAL_MODE=57603;
  static const int ECAL_HIGHRES_MODE=57602;
  static const int ECAL_RAW_MODE=57601;
  static const int TRIGGER_BANK_OLD=57606;
  static const int SSP_BANK=57612;
  static const int TRIGGER_BANK=57610;
  static const int SVT_CRATE_3=3;

  static const int DAQCONFIG_BANK=57614;

  static const int COSMIC_CRATE=39;
  static const int COSMIC_SLOT=20;
  #define COSMIC_CHAN {13,14,15}

  static const int N_FADC_SLOTS=20;
  static const int N_FADC_CHANS=16;

  bool fIgnoreFADC;

private:


  bool   get_events_from_et;
  bool   et_events_need_put;
  int    et_num_read;
  int    et_events_remaining;

#ifndef __CINT__                  // CINT is not able to parse the horrible EVIO gobledigook.
  // We thus hide all the EVIO components from CINT.
  evioFileChannel *EvioChan;
  evioDOMTree     *ETree;
  evioDictionary  *Dictionary;
  et_sys_id       et_id;
  et_stat_id      et_stat;
  et_att_id       et_attach;
  et_event        **et_evt_ptr;
#endif

};

#pragma GCC visibility pop
#endif
