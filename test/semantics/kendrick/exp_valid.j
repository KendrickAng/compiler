class TestAExp {
    Void main() {
        Int t;
        t = 1 + -2;
        t = 1 - -2;
        t = 1 + -2 - 3 * -4 / 5;
        t = t + t + t / t + t - 1 * 2;
    }
}

class TestBExp {
    Bool a;
    Bool b;

    Void main() {
        Bool c;
        Bool d;
        Bool t;
        t = true;
        t = false;
        t = true || false;
        t = true && false;
        t = !a && !b || !c && !d;
        t = 1 > 2;
        t = 1 < 2;
        t = 1 >= 2;
        t = 1 <= 2;
        t = 1 != 2;
        t = 1 == 2;
    }
}

class TestSExp {
    String id;

    Void main() {
        String t;
        t = "hi";
        t = "hi" + "world";
        t = t + "hi";
        t = this.id + "hi";
        t = (this.id) + "hi";
        t = null + "hi";
        t = (null) + "hi";
        t = "I hate " + "this assignment " + "why can't we use " + " parser generators ? ";
    }
}
