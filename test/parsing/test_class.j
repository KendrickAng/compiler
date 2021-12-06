class TestClass {
    Void main(Int a, Bool b, String s, Void v, TestClass t) {
        return "hello world";
    }
}

// THIS IS A COMMENT!
// This is another // comment /* that should */ still work // here
/* this should also
    // single line comment
    /* work here
*/
class TestClass1 {
    Dummy j;
    Int dummy() {
        Bool i;
        Bool j;
        return i ;
    }
}

/*  Mainly test multiple cl//ass (defined later but referenced first),
    Variable shadowing //in Dummy class,
    chained field access expressions,
    e.g. this.getCompute().square(-3);
    Test combination of "if .. else .." "return" and "while"
*/
class TestClass2 {
    Void main(Int i, Int a, Int b,Int d){
        Int t1;
        Int t2;
        Compute help;
        /*
        help = new Compute();
        help.chachedValue = t1 * 3;
        5
        t1 = help.addSquares(a,b) + help.square(i);
        t2 = help.square(d);
        if(t2>t1){
            println("Square of d larger than sum of squares");
        }
        else{
            println("Square of d larger than sum of squares");
        }
        */

        while(true){
            // t1 = 1*2;
            t1 = t2 ;
        }
    }
}

class TestClass3 {
    Compute c;
    Int i;
    Dummy j;
    Int dummy() {
        Bool i;
        Bool j;
        if (i || j) {
            return 1;
        }
        else {
            while(i) {
                i = !j;
            }
            c = this.getCompute();
        }
        return this.getCompute().square(-3);
        return i ;
    }
    Compute getCompute() {
        // c = new Compute();
        return c;
    }
}

class TestClass4 {
    // No body
}

class TestClass5 {
    Int i;
    Bool b;
    String s;
    Void v;
    Fruit f;
    String toString(Int i) {
        return "testclass";
    }
    Bool canPass() {
        return false;
    }
    Void hello() {
        if (true || false) {
            return true;
        } else {
            return false;
        }
        while (true) {
        }
        a = new Dummy();
        a.aa = 1;
        readln(s);
        println(1+2);
        return this.a.b().c(1,2).toString(this.color.method(!true));
    }
}
