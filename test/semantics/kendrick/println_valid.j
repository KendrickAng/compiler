class Main {

    Void main(){
        Print print;
        Int i;

        print = new Print();
        i = 10;
        println(i);
        println("2");
        println(print.toString());
        println("1" + "2");
        println(true || false && true);
    }
}

class Print {
    String toString() {
        return "string";
    }
}