class Main {

    Void main(){
        Int i;
        Bool b;
        String s;

        i = 2;
        b = true;
        while (i > 2 || i <= 1 || i == 2 && b) {
            s = new Clone().methodA();
        }
    }
}

class Clone {
    Bool b;
    String methodA() {
        String s;
        s = "HAHAHA";
        if (!!b && false || true) {
            b = true;
            return s + "1";
        } else {
            this.methodB();
        }
    }
    String methodB() {
        return null;
    }
}