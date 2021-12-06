class BoolOpsMain {

	Void main () {

		Int a;

		Int b;

		Bool b1;

		Bool b2;

		Bool b3;

		a= 4;

		b = 5;

		b1 = true;

		b2 = false;

		b3 = (b1 && b2) || b2 

			|| (b1 || b2); // should be true
	
        b1 = (a < b) && b3 ; 
		if ( (a < b) && b3 ) { // should be true

			println ("true");

		}

		else{ 

			println ("false");

		}

		

		if  ( b3 || (a > b)) { // should be true

			println ("true");

		}

		else{ 

			println ("false");

		}

	}

}



class BoolOps{ 

	Int a;

	

	Int func (Int x) {

	 return (6 + x);

	}

}

