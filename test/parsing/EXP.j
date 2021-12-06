class Main {

    Void main(){
        String s;
        Clone h;
        h = new Clone();
        h.val = 1;
        h.parent = null;
        g = h;
        f = g.copy().diff(h.copy());
        println(3 > -2 / ------1 && false || true || h.copy().copy().copy().parent.copy().val == -1 && !true && !!false || !f.getTrue(!false));
        if (g.copy().parent.copy().parent().copy().diff(g.copy().parent).val + g.val + h.val + f.val > 0) {
            readln(s);
            g.val = g.val + f.val + f.parent.val;
            s = g.copy().parent.toString() + f.toString() + g.toString();
            s = s + s + j.toString() + "cbparser";
        } else {
            s = "Nothing\n";
        }
        return;
    }
}

class Clone {
    Int val;
    Clone parent;

    Clone copy() {
        Clone c;
        c = new Clone();
        c.val = this.val;
        c.parent = this;
        return c;
    }

    Clone diff(Clone c) {
        
        // b is just a negation of a
        Bool a;
        Bool b;
        Clone res;
        Int x;

        a = this.val > c.val;
        b = c.val + c.val + c.val + this.val - 2 * c.val - 1 * this.val >= this.val + 0 || !a || false && 2 > 1;
        
        res = new Clone();
        res.val = this.val - a.val;
        res.parent = c;

        x = 2;
        while (x > 0 && a) {
            x = x - 1;
            res = res.copy();
        }
        while (x > 0 && b) {
            res = res.copy();
            x = x + x + x + x / x - 1 - x * 2;
        }
        res.copy();
        return res.parent;
    }

    Bool getTrue(Bool x) {
        return x || true;
    }

    String toString() {
        return "c ";
    }

}