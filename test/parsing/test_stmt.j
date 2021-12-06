class TestStmt {
    Void main() {
        TestStmt t1;
        TestStmt t2;

        // if-else
        if (true) {
            a = 1 + 2;
        } else {
            b = 1 * 2;
        }

        if (t1.test().node.test().test(t2.test().node.test()).a + t2.a > 0) {
            println(a);
            readln(a);
            return;
        }  else {
            return;
        }

        // while
        while (true) {
        }

        while (t1.test().node.test().test(t2.test().node.test()).a + t2.a > 0) {
            return;
        }

        // readln
        readln(a);

        // println
        println(true || false);
        println("hello" + "world");
        println(1 + 2 - 3 * 4 / 5);

        // id = Exp;
        x = 1 + 2 - 3 * 4 / 5;
        x = "hello" + "world";
        x = true || false;

        // Atom.id = Exp;
        this.x = 1 + 2 - 3 * 4 / 5;
        this.x = "hello" + "world";
        this.x = true || false;
        (null).x = 1 + 2 - 3 * 4 / 5;
        (null).x = "hello" + "world";
        (null).x = true || false;

        // Atom(ExpList);
        this(1,true,"c",t1.id);
        t1(1,true,"c",t1.id);

        // Atom();
        this();
        t1();

        // return Exp;
        return 1 + 2 - 3 * 4 / 5;
        return "hello" + "world";
        return true || false;

        // return;
        return ;
    }
}