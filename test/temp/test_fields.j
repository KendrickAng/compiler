class FieldAccessMain {

	Void main () {

		Int a;

		Int b;

		Int temp;

		

		FieldAccess f;

		f = new FieldAccess();

		

		b = f.func(5); // Function call. Result should be 11

		

		f.a = 7;  // Field write

		

		temp = (f.a + b) *2; // Field read. Result should be (11 + 7) *2 = 36

		

		println (temp); // Should output 36

	}

}



class FieldAccess{ 

	Int a;

	Int func (Int x) {

		return (6 + x);

    }

}



