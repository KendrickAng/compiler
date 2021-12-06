class Atom {

    Void main(Int a){
        Object obj;
        Atom atom;

        obj = new Object();
        atom = new Atom();

        atom.main(2);
        obj.val = obj;
        obj.toString();
        obj.toAdd(1,1,1);

        new Object().val = new Object();
        new Object().toString();
        new Object().toAdd(1,1,1);
/*
        null.val = 2;
        null.toString();
        null.toAdd(1,1,1);
*/
        obj.toString();
        (obj.toString()).val2 = 2;
        (obj.toString()).toString();
        (obj.toString()).toAdd(1,1,1);


        obj.toAdd(1, 1, 1);
        (obj).toString();
    
        obj.val = null;
        obj.val.toAdd(1, 1, 1);
        (obj.val).toString();
        (obj.val.toString()).val = new Object();
        obj = null;
        
        return;
   }

}

class Object {
    Object val;
    Int val2;
    Object toString() {
        return this.val.val.val;
    }
    Void toAdd(Int a, Int b, Int c) {
        return;
    }
}
