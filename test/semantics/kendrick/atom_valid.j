class TestAtom {
    Void main() {
        return;
    }
}

class Actual {
    Int a;

    String toString(Int a, Bool b, String c) {
        return c;
    }

    Void actual() {
        Actual t;

        // this
        this.a = 1;
        this.toString(1,true,null);

        // id
        actual();
        t.a = 1;
        t.toString(1,true,"c");

        // new cname()
        new Actual().a = 1;
        new Actual().toString(1,true,"c");

        // ( Exp )
        (new Actual()).a = 1;
        (new Actual()).toString(1,true,"c");

        (this.a) = 1;
        (this).toString(1,true,"c");

        (t.toString)(1,true,"c");

        return;
    }
}