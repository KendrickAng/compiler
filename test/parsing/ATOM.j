class Atom {

    Void main(Int a){
        Object obj;
        
        this();
        this.val = 2;
        this.toString();
        this.toAdd(1,1,1);

        obj();
        obj.val = 2;
        obj.toString();
        obj.toAdd(1,1,1);

        new Object()();
        new Object().val = 2;
        new Object().toString();
        new Object().toAdd(1,1,1);

        null();
        null.val = 2;
        null.toString();
        null.toAdd(1,1,1);

        (obj.toString())();
        (obj.toString()).val = 2;
        (obj.toString()).toString();
        (obj.toString()).toAdd(1,1,1);

        (obj.toAdd)(1, 1, 1);
        (obj.toString)();

        (obj.val.toAdd)(1, 1, 1);
        (obj.val.toString)();
        (obj.val.toString)().val = new Object();

        return;
   }
}
