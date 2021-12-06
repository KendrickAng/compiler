class Main {
    Void main() {
        Person person;
        person = new Person();
        person.age = 24;
        person.isTired = true;
        println(person.age);
        println(person.isTired);
    }
}

class Person {
    Int age;
    Bool isTired;
}