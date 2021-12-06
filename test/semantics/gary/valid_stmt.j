class Main {

    Void main(){
        String s;
        Clone c;
        Int x;
        x = 2;
        c = new Clone();
        c.val = x;
        c.copy();
        c.copy().parent = c;
        c = c.copy();
        if (x == 0) {
            x = 2;
        } else {
            s = "hello world";
            s = s + s;
        }
        while (x > 0 || x != 0-1*2 && 0 < x || true && false || !!!!!c.bl) {
            x = x - ----1;
            readln(x);
            println(c.copy().val);
            ((c.copy())).copy();
            (((c))).copy();
        }
        return;
    }
}

class Clone {
    Int val;
    Clone parent;
    Bool bl;

    Clone copy() {
        Clone c;
        doNothing(c);
        c = new Clone();
        c.val = this.val;
        c.parent = this;
        return c;
    }
    Void doNothing(Clone c) {
        return;
    }
}