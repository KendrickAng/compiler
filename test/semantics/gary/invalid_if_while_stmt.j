class Main {

    Void main(){
        Int i;
        Bool b;
        String s;

        i = 2;
        b = true;
        while (2 + 3 + 5) {
            s = new Clone().methodA();
            (((new Clone()))).methodB();
        }
    }
}

class Clone {
    Bool b;
    String methodA() {
        String s;
        s = "HAHAHA";
        if (methodB()) {
            b = true;
            return s + "1";
        } else {
            this.methodB();
            return b;
        }
    }
    String methodB() {
        return null;
    }
}