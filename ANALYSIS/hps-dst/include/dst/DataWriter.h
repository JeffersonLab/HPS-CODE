/**
 *	@section purpose: 
 *	@author: Omar Moreno <omoreno1@ucsc.edu>
 *			 Santa Cruz Institute for Particle Physics
 *			 University of California, Santa Cruz
 *	@date: January 2, 2013
 *	@version: 1.0
 *
 */

#ifndef __DATA_WRITER_H__
#define __DATA_WRITER_H__

//--- LCIO ---//
//------------//
#include <EVENT/LCEvent.h>

//--- HPS Event ---//
//-----------------//
#include <HpsEvent.h>

class DataWriter { 
	
	public: 
	
		virtual ~DataWriter(){}; 

		//
		virtual void writeData(EVENT::LCEvent*, HpsEvent*) = 0;
};

#endif // __DATA_WRITER_H__
