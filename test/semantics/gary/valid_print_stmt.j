class Main {

    Void main(){
        Clone c;
        Int i;
        c = new Clone();
        i = 2;
        println(i);
        println("2");
        println(c.methodA());
    }
}

class Clone {
    Bool methodA() {
        return true;
    }
}