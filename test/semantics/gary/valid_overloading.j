class Main {
    Void main(){
        Clone c;
        String s;
        c.a(1);
        c.a(false);
        s = c.a(5, new Clone());
        println( s );
    }
}

class Clone {
    Clone other;
    Void a(Int x) {
        other = new Clone();
        return;
    }
    Void a(Bool y) {
        return;
    }
    String a(Int x, Clone c) {
        String s;
        this.other = c;
        s = "cbty";
        while (x >= 0) {
             s = s + "peche";
             x = x - 1;
             s = s + "ckercbty";
        }
        s = s + "cker";
        return s;
    }
}