/**
 *	@section purpose: 
 *	@author: Omar Moreno <omoreno1@ucsc.edu>
 *			 Santa Cruz Institute for Particle Physics
 *			 University of California, Santa Cruz
 *	@date: January 6, 2014
 *	@version: 1.0
 *
 */

#ifndef __EVENT_BUILDER_H__
#define __EVENT_BUILDER_H__

//--- HPS Event ---//
//-----------------//
#include <HpsEvent.h>

//--- LCIO ---//
//------------//
#include <EVENT/LCEvent.h>

class EventBuilder { 

	public: 
		
		//
		virtual ~EventBuilder(){}; 

		//
		virtual void makeHpsEvent(EVENT::LCEvent*, HpsEvent*) = 0;  
};

#endif // __EVENT_BUILDER_H__
