class Main {

    Void main(){
        Clone c;
        Int i;
        c = new Clone();
        i = 2;
        println(c);
        println(c.methodA());
    }
}

class Clone {
    Void methodA() {
        return;
    }
}