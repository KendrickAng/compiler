class TestAtom {
    Void main() {
        TestAtom t;

        // this
        this();
        this.a = 1;
        this.toString();
        this.toString(1,true,"c");

        // id
        id();
        id.a = 1;
        id.toString();
        id.toString(1,true,"c");

        // null
        null();
        null.a = 1;
        null.toString();
        null.toString(1,true,"c");

        // new cname()
        new TestAtom()();
        new TestAtom().a = 1;
        new TestAtom().toString();
        new TestAtom().toString(1,true,"c");

        // ( Exp )
        (new TestAtom())();
        (new TestAtom()).a = 1;
        (new TestAtom()).toString();
        (new TestAtom()).toString(1,true,"c");

        (null)();
        (null).a = 1;
        (null).toString();
        (null).toString(1,true,"c");

        (this.a.b)();
        (this.a.b).a = 1;
        (this.a.b).toString();
        (this.a.b).toString(1,true,"c");

        (t.a.toString)(1,1,1);
        (t.a.toString)();
        (t.a.toString)().a = new TestAtom();

    }
}