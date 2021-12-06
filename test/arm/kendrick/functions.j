class Main {
    Void main() {
        Int a;
        Person person;
        person = new Person();
        a = person.greet(4212, "Good riddance 4212!");
        println(a);
    }
}

class Person {
    Int greet(Int a, String b) {
        println(a);
        println(b);
        return 4212;
    }
}